class info:
    def __init__(self,data:list):
        self.data = data
        
class addup:
    
    def __init__(self,var:info):
        var.data += [4]
        
class ppopop:
    def __init__(self,var:info):
        var.data += [4]
             
data = [1,2,3,4,5]

var=info(data)

lol = addup(var)
lol = ppopop(var)

print(var.data)
print(data)