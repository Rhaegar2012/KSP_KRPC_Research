import math
import numpy as np
from Utils import Constants

class PhysicsComputer():
    
    #TODO Identify the functions I need to perform to put a body 
    #TODO Do I need to calculate so many orbital parameters? (refactor)
    # in orbit from rest in the ground
    
    def __init__(self,current_position_vector,current_velocity_vector,current_fuel):
        self.gravitational_parameter            = Constants.KERBIN_GRAVITATIONAL_PARAMETER
        self.Isp                                = Constants.ISP
        self.thrust_force                       = Constants.F_THRUST
        self.fuel_consumption_rate              = Constants.FUEL_CONSUMPTION_RATE
        self.target_apoapsis                    = Constants.TARGET_APOAPSIS
        self.target_periapsis                   = Constants.TARGET_PERIAPSIS
        self.current_fuel                       = current_fuel
        self.current_position_vector            = current_position_vector #Cartesian coordinates body centered and non-rotating with origin at center of mass
        self.current_velocity_vector            = current_velocity_vector #Relative to orbiting body
        self.target_semimajor_axis              =0
        self.semi_latus_rectum                  =0
        self.orbital_angular_momentum           =0
        self.vis_viva_velocity                  =0
        self.target_eccentricity                =0
        self.delta_v                            =0
        self.current_eccentricity_vector        =0  
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
    
    

    def calculate_target_semimajor_axis(self):
        if self.target_apoapsis !=0 and self.target_periapsis !=0:
            self.target_semimajor_axis=(self.target_periapsis+self.target_apoapsis)/2
        else:
            print("invalid target apoapsis or periapsis")
            
    def calculate_target_eccentricity(self):
        if self.target_apoapsis !=0 and self.target_periapsis !=0:
            self.target_eccentricity=(self.target_apoapsis-self.target_periapsis)/(self.target_apoapsis+self.target_periapsis)
        else:
            print("Invalid target apoapsis or periapsis")
     
    #pass position_vector from sweep on true anomaly , not self.current_position_vector read from telemetry   
    def required_delta_v(self):
        self.semi_latus_rectum=self.target_semimajor_axis*(1-self.target_eccentricity**2)
        self.orbital_angular_momentum=math.sqrt(self.gravitational_parameter*self.semi_latus_rectum)
        position_vector_magnitude=self.calculate_vector_magnitude(self.current_position_vector)
        
        #Velocity magnitude required to achieve apoapsis through Vis Viva Equation
        self.vis_viva_velocity=math.sqrt(self.gravitational_parameter*((2/position_vector_magnitude)-(1/self.target_semimajor_axis)))
        
        #Burn Adjustment angle
        burn_adjustment_angle=math.acos(self.orbital_angular_momentum/(position_vector_magnitude*self.vis_viva_velocity))
        
        #Required velocity vector
        unit_r_hat_vector= [x/position_vector_magnitude for x in self.current_position_vector]
        angular_momentum_vector = np.cross(self.current_position_vector,self.current_velocity_vector)
        t_hat_unnormalized=np.cross(angular_momentum_vector,self.current_position_vector)
        t_hat_magnitude=self.calculate_vector_magnitude(t_hat_unnormalized)
        unit_t_hat_vector=[x/t_hat_magnitude for x in t_hat_unnormalized]
        
        r_hat_vector = [self.vis_viva_velocity*math.sin(burn_adjustment_angle)*x for x in unit_r_hat_vector]
        t_hat_vector = [self.vis_viva_velocity*math.cos(burn_adjustment_angle)*x for x in unit_t_hat_vector]
        
        #Calculate delta v and delta v vector
        required_velocity_vector=[x+y for x,y in zip(r_hat_vector,t_hat_vector)]
        delta_v_vector=[x-y for x,y in zip(required_velocity_vector,self.current_velocity_vector)]
        self.delta_v = self.calculate_vector_magnitude(delta_v_vector)
        
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
        pass
            
        
        
    
    
    