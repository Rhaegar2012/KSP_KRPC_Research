class TelemetryManager():
    
    def __init__(self,active_vessel):
        self.vessel=active_vessel
        if self.vessel:
            self.reference_frame=self.vessel.reference_frame
            self.flight_info=self.vessel.flight(self.reference_frame)
            self.orbit=self.vessel.orbit
            self.resources=self.vessel.resources
            

        else:
            print("Vessel not found")
            return None
    
    def set_up_telemetry_streams(self):
        pass
    
    def stream_telemetry_data():
        pass