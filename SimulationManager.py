import krpc 
import pandas as pd
import time
from Utils import Constants as const
from TelemetryManager import TelemetryManager
from VesselController import VesselController
from SimulationController import SimulationController




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


def setup_simulation():
    #connection to krpc 
    global krpc_connection, space_center, active_vessel, telemetry_manager, vessel_controller, simulation_controller
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
        telemetry_manager= TelemetryManager(active_vessel,krpc_connection)
        telemetry_manager.set_up_telemetry_streams()
        vessel_controller=VesselController()
        simulation_controller=SimulationController()
        
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
        simulation_telemetry_data.append(telemetry_data)
        if terminate_simulation(telemetry_data[2]):
            is_running_simulation=False
    
    time.sleep(1)
    
    dataframe_list = post_simulation_processing(simulation_telemetry_data)
    processed_flight_data=pd.DataFrame(dataframe_list[0])
    processed_orbit_data =pd.DataFrame(dataframe_list[1])
    processed_resource_data= pd.DataFrame(dataframe_list[2])
    flight_data_export=processed_flight_data.to_csv('flight_data.csv')
    orbit_data_export =processed_orbit_data.to_csv('orbit_data.csv')
    resource_data_export=processed_resource_data.to_csv('resource_data.csv')
    print("simulation finished")
    
    
 
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