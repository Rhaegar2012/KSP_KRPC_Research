class KG_Edge():
    
    def __init__(self,origin_node,target_node):
        self.origin_node = origin_node
        self.target_node = target_node
        
    
    def get_endpoints(self):
        return (self.origin_node,self.target_node)
    
    def get_opposite(self,test_node):
        if(test_node in [self.origin_node,self.target_node]):
            if test_node == self.origin_node:
                return self.target_node
            else:
                return self.origin_node
        else:
            return None
        
        
        
    
    