class KG_Graph():
    
    def __init__(self):
        self.num_nodes=0
        self.nodes=[]
        self.num_edges=0
        self.edges=[]
    
    def count_nodes(self):
        return len(self.nodes)
    
    def count_edges(self):
        return len(self.edges)
    
    def get_nodes(self):
        return self.nodes
    
    def get_edges(self):
        return self.edges
    
    def get_edge(self,origin_node,target_node):
        pass
    
    def get_degree(self, node,out=True):
        pass
    
    def incident_edges(self, node, out=True):
        pass
    
    def insert_node(self , node):
        pass
    
    def insert_edge(self, edge):
        pass
    
    def remove_node(self,node):
        pass
    
    def remove_edge(self,edge):
        pass 
    
    
    