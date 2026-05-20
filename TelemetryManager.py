from Utils import Collections as collections


class TelemetryManager():

    def __init__(self,active_vessel,krpc_connection):
        self.vessel=active_vessel
        self.conn=krpc_connection
        
        if self.vessel and self.conn:
            self.reference_frame=self.vessel.reference_frame
            self.flight_info=self.vessel.flight()
            self.orbit=self.vessel.orbit
            self.resources=self.vessel.resources
            self.available_resources=self.resources #list of stored resources
            self.flight_telemetry_callback={}
            self.orbit_telemetry_callback={}
            self.resource_telemetry_callback={}
            self.flight_telemetry_stream=None
            self.orbit_telemetry_stream=None
            self.resource_telemetry_stream=None
            
        else:
            print("Vessel not found")
            return None
    
    def set_up_telemetry_streams(self):
        #1.Create telemetry callback dictionaries for batch call from collections
        #Example: {'mean_altitude':(self.flight_info,'mean_altitude')}
        #Example: {'SolidFuel':(self.resources,'amount')}
        self.flight_telemetry_callback={collections.flight_telemetry_data[i]:(self.flight_info,collections.flight_telemetry_data[i]) 
                                      for i in range(len(collections.flight_telemetry_data))}
        
        self.orbit_telemetry_callback={collections.orbit_telemetry_data[i]:(self.orbit,collections.orbit_telemetry_data[i])
                                     for i in range(len(collections.orbit_telemetry_data))}
        
        self.resource_telemetry_callback={self.available_resources[i]:(self.resources,'amount',self.available_resources[i])
                                        for i in range(len(self.available_resources.names))}
        
        #2.Set up connection streams 
        
        self.flight_telemetry_stream={name:self.conn.add_stream(getattr,obj,attr) 
                                      for name,(obj,attr) in self.flight_telemetry_callback.items()}
        
        self.orbit_telemetry_stream={name:self.conn.add_stream(getattr,obj,attr) 
                                     for name,(obj,attr) in self.orbit_telemetry_callback.items()}
        
        self.resource_telemetry_stream={name:self.conn.add_stream(func,arg) 
                                     for name,(func,arg)in self.resource_telemetry_callback.items()}
        
    def stream_telemetry_data(self):
        telemetry_data=[{name:stream() for name,stream in self.flight_telemetry_stream.items()},
                        {name:stream() for name,stream in self.orbit_telemetry_stream.items()},
                        {name:stream() for name,stream in self.resource_telemetry_stream.items()}]
        return telemetry_data