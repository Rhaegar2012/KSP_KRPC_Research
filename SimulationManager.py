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
telemetry_data_snapshot ={}
telemetry_data_record   =[]


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
        print(telemetry_data)
        telemetry_data_record.append(telemetry_data)
        if terminate_simulation(telemetry_data[2]):
            is_running_simulation=False
    time.sleep(1)
    flight_data     =pd.DataFrame(telemetry_data[0])
    orbit_data      =pd.DataFrame(telemetry_data[1])
    resource_data   =pd.DataFrame(telemetry_data[2])
        
    flight_data.to_csv('flight_data.csv')
    orbit_data.to_csv('orbit_data.csv')
    resource_data.to_csv('resource_data.csv')
    print("simulation finished")
    
    
 
def post_simulation_processing():
    pass


def terminate_simulation(resource_data):
    return resource_data['SolidFuel']==0


if __name__=="__main__":
    setup_simulation()
    run_simulation()
    post_simulation_processing()
    print("simulation finished")