import math
import numpy as np
from Utils import Constants

class PhysicsComputer():
    
    #TODO Identify the functions I need to perform to put a body 
    #TODO Do I need to calculate so many orbital parameters? (refactor)
    # in orbit from rest in the ground
    
    def __init__(self,current_movement_vector,current_velocity_vector,current_fuel):
        self.gravitational_parameter            = Constants.KERBIN_GRAVITATIONAL_PARAMETER
        self.Isp                                = Constants.ISP
        self.thrust_force                       = Constants.F_THRUST
        self.fuel_consumption_rate              = Constants.FUEL_CONSUMPTION_RATE
        self.target_apoapsis                    =Constants.TARGET_APOAPSIS
        self.target_periapsis                   =Constants.TARGET_PERIAPSIS
        self.current_fuel                       = current_fuel
        self.current_position_vector            = current_movement_vector
        self.current_velocity_vector            = current_velocity_vector
        self.target_semimajor_axis              =0
        self.semi_latus_rectum                  =0
        self.orbital_angular_momentum           =0
        self.vis_viva_velocity                  =0
        self.target_eccentricity                =0
        self.delta_v                            =0
        self.right_ascension_of_ascending_node  =[]
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
    
    

    def calculate_semimajor_axis(self):
        if self.target_apoapsis !=0 and self.target_periapsis !=0:
            self.target_semimajor_axis=(self.target_periapsis+self.target_apoapsis)/2
        else:
            print("invalid target apoapsis or periapsis")
            
    def calculate_target_eccentricity(self):
        if self.target_apoapsis !=0 and self.target_periapsis !=0:
            self.target_eccentricity=(self.target_apoapsis-self.target_periapsis)/(self.target_apoapsis+self.target_periapsis)
        else:
            print("Invalid target apoapsis or periapsis")
        
    def required_delta_v(self):
        self.semi_latus_rectum=self.target_semimajor_axis*(1-self.target_eccentricity**2)
        self.orbital_angular_momentum=math.sqrt(self.gravitational_parameter*self.semi_latus_rectum)
        position_vector_magnitude=self.calculate_vector_magnitude(self.current_position_vector)
        velocity_vector_magnitude=self.calculate_vector_magnitude(self.current_velocity_vector)
        
        #Velocity magnitude required to achieve apoapsis through Vis Viva Equation
        self.vis_viva_velocity=math.sqrt(self.gravitational_parameter*((2/position_vector_magnitude)-(1/self.target_semimajor_axis)))
        
        #Burn Adjustment angle
        burn_adjustment_angle=math.acos(self.orbital_angular_momentum/(position_vector_magnitude*self.vis_viva_velocity))
        
        #Required velocity vector
        unit_r_hat_vector= [x/position_vector_magnitude for x in self.current_position_vector]
        
        angular_momentum_vector = np.cross(self.current_position_vector,self.current_velocity_vector)
        angular_momentum_magnitude = self.calculate_vector_magnitude(angular_momentum_vector)
        
        unit_t_hat_vector=[x/angular_momentum_magnitude for x in angular_momentum_vector]
        
        r_hat_vector = [self.vis_viva_velocity*math.sin(burn_adjustment_angle)*x for x in unit_r_hat_vector]
        t_hat_vector = [self.vis_viva_velocity*math.cos(burn_adjustment_angle)*x for x in unit_t_hat_vector]
        
        #Calculate delta v and delta v vector
        required_velocity_vector=[x+y for x,y in zip(r_hat_vector,t_hat_vector)]
        delta_v_vector=[x-y for x,y in zip(required_velocity_vector,self.current_velocity_vector)]
        self.delta_v = self.calculate_vector_magnitude(delta_v_vector)
        
    #TODO REFACTOR AND REVIEW IF NECESSARY
    def calculate_true_anomaly(self,position_vector):
        if len(position_vector)<3 or position_vector is None:
            print("invalid position vector")
            return 0
        else:
            numerator=self.calculate_dot_product(self.eccentricity_vector,position_vector)
            denominator =self.calculate_vector_magnitude(self.eccentricity_vector)*self.calculate_vector_magnitude(position_vector)
            self.true_anomaly=math.acos(numerator/denominator)
    
    
    
    #TODO REFACTOR TO CALCULATE NECESSARY DELTA_V
    #Project telemetry data in future
    #need a way to calculate fuel consumption rate
    #need a way to transmit initial conditions. Should I start the simulation from telemetry or from derivation?
    def simulate_projected_trajectory(self):
        time_to_fuel_depletion = self.remaining_fuel/self.fuel_consumption_rate
        simulation_time=0
        while simulation_time<time_to_fuel_depletion:
            self.calculate_instant_COE()
            simulation_time+=Constants.SIMULATION_STEP
        return self.orbital_parameters
            
        
        
    
    
    