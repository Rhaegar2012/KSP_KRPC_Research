import math

class PhysicsComputer():
    
    #TODO Identify the functions I need to perform to put a body 
    # in orbit from rest in the ground
    
    def __init__(self,gravitational_parameter):
        self.gravitational_parameter=gravitational_parameter
        self.specific_mechanical_energy         =0
        self.semimajor_axis                     =0
        self.eccentricity_vector                =[]
        self.right_ascension_of_ascending_node  =[]
        self.argument_of_perigee                =0
        self.true_anomaly                       =0
        self.unit_vector_k                      =[0,0,1] #Unit vector through the north pole
        self.unit_vector_i                      =[1,0,0] #Unit vector through principal direction
        self.inclination                        =0
        self.apoapsis                           =0
        self.periapsis                          =0
        self.remaining_fuel                     =0
        self.rate_of_fuel_consumptuion          =0
        
    
    def calculate_vector_magnitude(self,vector):
        square_sum=0
        if len(vector) ==0 or vector is None:
            return 0
        else:
            square_sum += [x^2 for x in vector]
            return math.sqrt(square_sum)
        
    def calculate_dot_product(self,vector_a,vector_b):
        dot_product=0
        if len(vector_a) != len(vector_b):
            print("vectors are of different size , can't compute dot product")
            return 0
        else:
            i=0
            for i in range(len(vector_a)-1):
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
    
    
    def calculate_specific_mechanical_energy(self,velocity_vector,position_vector):
        
        if velocity_vector is None or position_vector is None: 
            print ("empty velocity or position vector")
            return 0
        else:
            magnitude_of_velocity_vector=self.calculate_vector_magnitude(velocity_vector)
            magnitude_of_position_vector=self.calculate_vector_magnitude(position_vector)
            self.specific_mechanical_energy= (magnitude_of_velocity_vector^2)/2-(self.gravitational_parameter/magnitude_of_position_vector)
        
    
    def calculate_semimajor_axis(self):
        if(self.specific_mechanical_energy!=0):
            self.semimajor_axis=-(self.gravitational_parameter/(2*self.specific_mechanical_energy))
        else:
            return 0
            
    
    def calculate_eccentricity_vector(self,velocity_vector,position_vector):
        if velocity_vector is None or position_vector is None:
            print("empty velocity or position vector")
            return 0
        else:
            first_term  =(self.calculate_vector_magnitude(velocity_vector)-(self.gravitational_parameter/self.calculate_vector_magnitude(position_vector)))*position_vector
            second_term =(self.calculate_dot_product(position_vector,velocity_vector))*velocity_vector
            self.eccentricity=(1/self.gravitational_parameter)*(self.calculate_vector_substraction(first_term,second_term))
        
    
    def calculate_orbital_inclination(self,specific_angular_momentum_vector):
        if len(specific_angular_momentum_vector)<3 or specific_angular_momentum_vector is None: 
            print("invalid angular momentum vector")
            return 0
        else:
            numerator=self.calculate_dot_product(self.unit_vector_k,specific_angular_momentum_vector)
            denominator= self.calculate_vector_magnitude(self.unit_vector_k)*self.calculate_vector_magnitude(specific_angular_momentum_vector)
            self.inclination=math.acos(numerator/denominator) 
        
    
    def calculate_right_ascension_of_ascending_node(self,ascending_node_vector):
        if len(ascending_node_vector)<3 or ascending_node_vector is None: 
            print("invalid ascending node")
            return 0
        else:
            numerator= self.calculate_dot_product(self.unit_vector_i,ascending_node_vector)
            denominator= self.calculate_vector_magnitude(self.unit_vector_i)*self.calculate_vector_magnitude(ascending_node_vector)
            self.right_ascension_of_ascending_node=math.acos(numerator/denominator)

    
    def calculate_argument_of_perigee(self,ascending_node_vector):
        if len(ascending_node_vector)<3 or ascending_node_vector is None:
            print("invalid ascending node vector")
            return 0
        else:
            numerator=self.calculate_dot_product(ascending_node_vector,self.eccentricity_vector)
            denominator=(self.calculate_vector_magnitude(ascending_node_vector))*(self.calculate_vector_magnitude(self.eccentricity_vector))
            self.argument_of_perigee=math.acos(numerator/denominator)
    
    
    def calculate_true_anomaly(self,position_vector):
        if len(position_vector)<3 or position_vector is None:
            print("invalid position vector")
            return 0
        else:
            numerator=self.calculate_dot_product(self.eccentricity_vector,position_vector)
            denominator =self.calculate_vector_magnitude(self.eccentricity_vector)*self.calculate_vector_magnitude(position_vector)
            self.true_anomaly=math.acos(numerator/denominator)
    
    def calculate_current_apoapsis_periapsis(self):
        self.periapsis=self.semimajor_axis*(1-self.calculate_vector_magnitude(self.eccentricity_vector))
        self.apoapsis =self.semimajor_axis*(1+self.calculate_vector_magnitude(self.eccentricity_vector))
    
    #This function will calculate the orbital parameters for every tick of the physics simulation
    def calculate_instant_COE(self):
        self.calculate_specific_mechanical_energy()
        self.calculate_semimajor_axis()
        self.calculate_eccentricity_vector()
        self.calculate_orbital_inclination()
        self.calculate_right_ascension_of_ascending_node()
        self.calculate_argument_of_perigee()
        self.calculate_true_anomaly()
        self.calculate_current_apoapsis_periapsis()
    
    def set_initial_conditions(self,remaining_fuel,rate_of_consumption):
        self.remaining_fuel=remaining_fuel
        self.rate_of_fuel_consumptuion=rate_of_consumption 
    
    
    #Project telemetry data in future
    #need a way to calculate fuel consumption rate
    #need a way to transmit initial conditions. Should I start the simulation from telemetry or from derivation?
    def calculate_current_trajectory():
        pass
        
    
    
    