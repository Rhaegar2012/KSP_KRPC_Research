class KG_Node(): 
    
    def __init__(self,node_type,node_element):
        self.node_type=node_type
        self.node_element=node_element
        
    def get_node_element(self):
        return self.node_element
    
    def get_node_type(self):
        return self.node_type
    
    # will allow node to be a map/set key
    def __hash__(self):
        return hash(id(self))



class KG_Edge():
    
    def __init__(self,origin_node,target_node,element):
        self.origin_node = origin_node
        self.target_node = target_node
        self.element     = element
        
    
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
        
    def get_element(self):
        return self.element
    
    # Allow each edge to be a map/set key
    
    def __hash__(self):
        return hash((self.origin_node,self.target_node))


class KG_Graph():
    
    def __init__(self,directed=False):
        self.num_nodes=0
        self.num_edges=0
        self.outgoing={}
        #Only create second map for directed graph; use alias for undirected
        self.incoming = { } if directed else self.outgoing
    
    
    def is_directed(self):
        return self.incoming is not self.outgoing
    
    #Number of nodes in the graph
    def count_nodes(self):
        self.num_nodes= len(self.outgoing)
        return len(self.num_nodes)
    
    def count_edges(self):
        total= sum(len(self.outgoing[n] for n in self.outgoing))
        return total if self.is_directed() else total//2
    
    def get_nodes(self):
        return self.outgoing.keys()
    
    def get_edges(self):
        result = set()
        for secondary_map in self.outgoing.values():
            result.update(secondary_map.values())
        return result
    
    def get_edge(self,origin_node,target_node):
        return self.outgoing[origin_node].get(target_node)
    
    def get_degree(self, node,outgoing=True):
        adjacent=self.outgoing if outgoing else self.incoming
        return len(adjacent[node])
    
    def incident_edges(self, node, outgoing=True):
        adjacent= self.outgoing if outgoing else self.incoming
        for edge in adjacent[node].values():
            yield edge
    
    def insert_node(self , node=None):
        new_node=KG_Node(node)
        self.outgoing[new_node]={}#Dictionary to store edge references
        if self.is_directed:
            self.incoming[new_node]={}#Need distinct map for incoming edges
    
    def insert_edge(self,origin_node,target_node,element):
        new_edge=self.Edge(origin_node,target_node,element)
        self.outgoing[origin_node][target_node]=new_edge
        self.incoming[target_node][origin_node]=new_edge
    
    def remove_node(self,node):
        pass
    
    def remove_edge(self,edge):
        pass 
    
    
    