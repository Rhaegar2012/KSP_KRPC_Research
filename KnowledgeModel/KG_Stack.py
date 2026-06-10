class KG_Stack():
    
    def __init__(self):
        self.stack=[]
        self.stack_size=len(self.stack)
    
    def push(self,item):
        self.stack.append(item)
        self.stack_size+=1
    
    def pop(self):
        if self.stack_size == 0:
            return None
        else:
            self.stack_size -=1
            return self.stack.pop()
        
    def stack_peek(self):
        if self.stack_size==0:
            return None
        else: 
            return self.stack[self.stack_size-1]
         
    