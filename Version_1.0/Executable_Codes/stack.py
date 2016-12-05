class Stack:
    def __init__(self):
        self.items = []
        self.length = 0
        
    def push(self, val):
        self.items.append(val)
        self.length += 1
        
    def pop(self):
        if self.is_empty():
            return None
        self.length -= 1
        return self.items.pop()
        
    def size(self):
        return self.length
    
    def peek(self):
        if self.is_empty():
            return None
        return self.items[self.length - 1]
    
    def is_empty(self):
        return self.length == 0
    
    def __str__(self):
        return str(self.items)