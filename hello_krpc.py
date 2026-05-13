import krpc
import pandas as pd
import time

#TODO RECORD DATA DURING MANUAL FLIGHT
#TODO CREATE SCRIPT OF AUTOMATED FLIGHT CONTROL

flight_data={'Altitude':[],'Fuel Amount':[]}

def launch_flight(vessel):
    vessel.auto_pilot.target_pitch_and_heading(90,90)
    vessel.auto_pilot.engage()
    vessel.control.throttle=1
    print('Launch Vessel')
    time.sleep(1)#wait for 1 second before launching
    vessel.control.activate_next_stage()




def stream_flight_data(vessel):
    flight_info = vessel.flight()
    flight_altitude_stream=conn.add_stream(getattr,flight_info,'mean_altitude')
    fuel_stream = conn.add_stream(vessel.resources.amount, 'SolidFuel') #to open the connection pass the function callback 
    record_data=True
    #to do stop recording data with a condition is met , mission accomplished , failed or delta_v
    while record_data:
        time.sleep(0.1)#take a data snapshot after a set time interval
        flight_data['Altitude'].append(flight_altitude_stream())#append data
        flight_data['Fuel Amount'].append(fuel_stream())
        if fuel_stream()<0.1:#terminate stream recording
            record_data=False
    flight_altitude_stream.remove()
    fuel_stream.remove()
    




if __name__ == "__main__":
    print("initiate krpc client")
    conn=krpc.connect(name='Hello World')
    vessel=conn.space_center.active_vessel
    print(vessel.name)
    launch_flight(vessel)
    stream_flight_data(vessel)
    flight_data_df=pd.DataFrame(flight_data)
    flight_data_df.to_csv('flight_data.csv')