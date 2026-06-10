import krpc 
import pandas as pd
import time
from Utils import Constants as const
from TelemetryManager import TelemetryManager
from VesselController import VesselController
from PhysicsEngine import PhysicsComputer
from KnowledgeModel.KG_Graph import KG_Graph
from KnowledgeModel.KG_Graph import KG_Node
from KnowledgeModel.KG_Graph import KG_Edge
from KnowledgeModel.KG_Stack import KG_Stack
from Utils.Enums import KG_Node_Enum as Enums
from Utils import Collections as collections


#State variables
krpc_connection         = None
space_center            = None
active_vessel           = None
telemetry_manager       = None
vessel_controller       = None
simulation_controller   = None


#Telemetry Data
telemetry_data_snapshot     ={}
simulation_telemetry_data   =[]

#Knowledge model 
simulation_kg               = None
telemetry_snapshot_stack    = None



def setup_simulation():
    #connection to krpc 
    global krpc_connection, space_center, active_vessel, telemetry_manager, vessel_controller, simulation_controller , simulation_kg , telemetry_snapshot_stack
    print("initiate krpc client")
    try:
        krpc_connection=krpc.connect(name="simulation")
        active_vessel  =krpc_connection.space_center.active_vessel
        space_center   =krpc_connection.space_center
        active_vessel.auto_pilot.target_pitch_and_heading(const.INITIAL_PTCH,const.INITIAL_HEADING)
        active_vessel.control.throttle=const.INITIAL_THROTTLE
        active_vessel.control.sas=True
        active_vessel.control.rcs=False
        
        
    except Exception as e:
        print(f'krpc connection failed: {e}')
        return False
    time.sleep(1)
    print("krpc connection successful")
    #setup simulation functions
    try:
        simulation_kg = KG_Graph()
        telemetry_snapshot_stack=KG_Stack()
        telemetry_manager= TelemetryManager(active_vessel,krpc_connection)
        telemetry_manager.set_up_telemetry_streams()
        vessel_controller=VesselController()
        simulation_controller=PhysicsComputer()
        
    except Exception as e:
        print(f'simulation functions setup failed :{e}')
        return False
    time.sleep(1)
    print("simulation functions setup successful") 

def run_simulation():
    print("begin simulation")
    is_running_simulation   = True
    time.sleep(1)
    while is_running_simulation:
        time.sleep(const.SIMULATION_SLEEP)
        telemetry_data=telemetry_manager.stream_telemetry_data()
        
        #create time event graph node
        create_event_graph_node(telemetry_data) 
        simulation_telemetry_data.append(telemetry_data)
        if terminate_simulation(telemetry_data[2]):
            is_running_simulation=False
    
    time.sleep(1)
    
    
    dataframe_list = post_simulation_processing(simulation_telemetry_data)
    processed_flight_data=pd.DataFrame(dataframe_list[0])
    processed_orbit_data =pd.DataFrame(dataframe_list[1])
    processed_resource_data= pd.DataFrame(dataframe_list[2])
    
    #Export data to csv for observation
    flight_data_export=processed_flight_data.to_csv('flight_data.csv')
    orbit_data_export =processed_orbit_data.to_csv('orbit_data.csv')
    resource_data_export=processed_resource_data.to_csv('resource_data.csv')
    print("simulation finished")
    
def create_event_graph_node(data_stream):
    
    #Create a new node and link it to an existing node , if it exists
    previous_stream_node= telemetry_snapshot_stack.stack_peek()
    new_stream_node=KG_Node(Enums.READING_SNAPSHOT,"Snapshot")
    if previous_stream_node is None:
        
        telemetry_snapshot_stack.push(new_stream_node)
    else:
        new_stream_edge=KG_Edge(previous_stream_node,new_stream_node,Enums.READING_SNAPSHOT)
        telemetry_snapshot_stack.push(new_stream_node)
        simulation_kg.insert_edge(new_stream_edge)

    #Insert new telemetry node into the graph
    simulation_kg.insert_node(new_stream_node)
    #Loop through data stream and insert each telemetry reading node
    for reading in data_stream:
        #read node type based on data type
        node_type = determine_node_type(reading.keys())
        if node_type:
            new_reading_node=KG_Node(node_type,reading)
            simulation_kg.insert_node(new_reading_node)
            simulation_kg.insert_edge(new_stream_node,new_reading_node,node_type) 
        else:
            continue
       
def determine_node_type(data_stream_keys):
         if data_stream_keys==collections.flight_telemetry_data:
             return Enums.MOVEMENT_STATE
         elif data_stream_keys==collections.orbit_telemetry_data:
             return Enums.ORBIT_STATE
         elif data_stream_keys==telemetry_manager.available_resources.names:
             return Enums.VESSEL_STATE
         else:
             return None
    
    
    
 
def post_simulation_processing(raw_telemetry_data):
    ### Notes it seems it may be better to have the data split in 3 distinct datasets, let's try that
    sorted_list=[]
    result_list=[]
    loop=0
    #1. unpack dictionaries from containing list  [[{},{},{}],[{},{},{}]]-> [[{Flight Data}],[{Orbit Data}],[{Resource Data}]]
    #Assume all the interior lists are of equal length
    while loop<len(raw_telemetry_data[0]):
        temp_list=[]
        for i in range(len(raw_telemetry_data)):
            temp_list.append(raw_telemetry_data[i][loop])
        loop+=1
        sorted_list.append(temp_list)

    #2. Use dictionary comprehension to unpack dictionary collection into dataframe_dictionary
    #[{},{},{}]-> {} in the result list for each list we have in the sorted list
    for i in range(len(sorted_list)):
        dict_list=sorted_list[i]
        result_list.append({key:[data_dictionary.get(key) for data_dictionary in dict_list]
                            for key in set().union(*dict_list)})
    
    return result_list


def terminate_simulation(resource_data):
    return resource_data['SolidFuel']==0


if __name__=="__main__":
    setup_simulation()
    run_simulation()
    print("simulation finished")