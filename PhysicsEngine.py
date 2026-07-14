import sys
import math
import numpy as np
from Utils import Constants

class PhysicsComputer():
    
    #TODO Identify the functions I need to perform to put a body 
    #TODO Do I need to calculate so many orbital parameters? (refactor)
    # in orbit from rest in the ground
    
    def __init__(self,telemetry_position_vector,
                 current_velocity_vector,
                 telemetry_fuel,
                 telemetry_apoapsis,
                 telemetry_eccentricity,
                 telemetry_semi_major_axis):
        self.gravitational_parameter            = Constants.KERBIN_GRAVITATIONAL_PARAMETER
        self.Isp                                = Constants.ISP
        self.thrust_force                       = Constants.F_THRUST
        self.fuel_consumption_rate              = Constants.FUEL_CONSUMPTION_RATE
        self.target_apoapsis                    = Constants.TARGET_APOAPSIS
        self.target_periapsis                   = Constants.TARGET_PERIAPSIS
        self.telemetry_apoapsis                 = telemetry_apoapsis
        self.telemetry_fuel                     = telemetry_fuel
        self.telemetry_eccentricity             =telemetry_eccentricity
        self.telemetry_position_vector          = telemetry_position_vector #Cartesian coordinates body centered and non-rotating with origin at center of mass
        self.current_velocity_vector            = current_velocity_vector #Relative to orbiting body
        self.telemetry_semi_major_axis          = telemetry_semi_major_axis
        self.target_semimajor_axis              =(self.target_apoapsis+self.target_periapsis)/2
        self.target_eccentricity                =(self.target_apoapsis-self.target_periapsis)/(self.target_apoapsis+self.target_periapsis)
        self.semi_latus_rectum                  =0
        self.orbital_angular_momentum           =0
        self.vis_viva_velocity                  =0
        self.delta_v                            =0
        self.true_anomaly                       =0
        
    
        
        
    
    def calculate_vector_magnitude(self,vector):
        square_sum=0
        if vector is None or len(vector) ==0:
            return 0
        else:
            for x in vector:
                square_sum+=x**2
            return math.sqrt(square_sum)
        
    def calculate_dot_product(self,vector_a,vector_b):
        dot_product=0
        if len(vector_a) != len(vector_b):
            print("vectors are of different size , can't compute dot product")
            return 0
        else:
            i=0
            for i in range(len(vector_a)):
                dot_product+=vector_a[i]*vector_b[i]
            return dot_product
                
    def calculate_vector_substraction(self,vector_a,vector_b):
        vector_substraction=[]
        if len(vector_a) != len(vector_b):
            print("vectors are of different size, can't compute substraction")
            return 0
        else:
            i=0
            for i in range(len(vector_a)):
                vector_substraction.append(vector_a[i]-vector_b[i])
            return vector_substraction
    
     
    #pass position_vector from sweep on true anomaly , not self.current_position_vector read from telemetry   
    def calculate_vis_viva(self,position_magnitude,semimajor_axis):
        
        #Velocity magnitude required to achieve apoapsis through Vis Viva Equation
        vis_viva_velocity=math.sqrt(self.gravitational_parameter*((2/position_magnitude)-(1/semimajor_axis)))
        
        return vis_viva_velocity
        
    #Find cheapest correction burn 
    def find_correction_burn(self):
        '''
        1. Calculate current semi-latus rectum p_0=a_0(1-e_0**2) read from telemetry on every tick
        2. Loop true anomaly (v) from 0 (periapsis) to 180 (apoapsis)
           2.1 Calculate R(v) from true anomaly sweep from 0 (periapsis) to 180 (apoapsis)
           2.2 Calculate current vis_viva velocity with R(v)
           2.3 Calculate current flight path angle with current true anomaly as gamma (v)=e_0*sin(v)/(1+e_0*cos(v))
           2.4 Calculate new  vis_viva velocity for target apoapsis
           2.5 Calculate new flight path angle with current true anomaly but angular momentum for target apoapsis semi-latus rectm
           2.6 Calculate required delta_v using the position vector R(v) and the target angular momentum
           2.7 if cost<minimum cost save minimum cost
        3. Return R(v) and V (correction to prograde) 
        '''
        telemetry_semi_latus_rectum =self.telemetry_semi_major_axis*(1-self.telemetry_eccentricity**2)
        target_semi_latus_rectum    =self.target_semimajor_axis*(1-self.target_eccentricity**2)
        true_anomaly=0
        min_delta_v= sys.float_info.max
        min_true_anomaly=[]
        min_position=[]
        while true_anomaly<Constants.SIMULATION_TRUE_ANOMALY_AT_APOAPSIS:
            
            position_at_anomaly=telemetry_semi_latus_rectum/(1+self.telemetry_eccentricity*math.cos(true_anomaly))#Change apoapsis for semimajor axis
            
            if self.target_periapsis<=position_at_anomaly<=self.target_apoapsis:
                #Current velocity (prograde) at anomaly
                vis_viva_at_anomaly=self.calculate_vis_viva(position_at_anomaly,self.telemetry_semi_major_axis)
                flight_path_angle_at_anomaly=math.atan(self.telemetry_eccentricity*math.sin(true_anomaly)/(1+self.telemetry_eccentricity*math.cos(true_anomaly)))
                #Target velocity (prograde)
                target_vis_viva=self.calculate_vis_viva(position_at_anomaly,self.target_semimajor_axis)
                flight_path_angle_at_target=math.acos((math.sqrt(self.gravitational_parameter*target_semi_latus_rectum)/(position_at_anomaly*target_vis_viva)))
            
                required_delta_v=math.sqrt(target_vis_viva**2+vis_viva_at_anomaly**2-2*target_vis_viva*vis_viva_at_anomaly*math.cos(flight_path_angle_at_target-flight_path_angle_at_anomaly))

                #Update min delta v
                if required_delta_v<min_delta_v:
                    min_delta_v=required_delta_v
                    min_true_anomaly=true_anomaly
                    min_position=position_at_anomaly
            
            true_anomaly+=Constants.SIMULATION_TRUE_ANOMALY_STEP
        
        if min_delta_v <sys.float_info.max:
            Prograde_Correction=
            return (min_delta_v,min_position,Prograde_Correction
        else:
            return 0
        
        
            
        
        
    
    
    