class ambiguityResolver(goals):
    
    
    
    def findObject(self, objects, object):
        result = list()
        
        for allObjects in objects.values():
            for eachObject in allObjects.values():
                if ((eachObject["form"] == object["form"] or not object["form"]) and  
                    (eachObject["size"] == object["size"] or not object["size"]) and 
                    (eachObject["color"] == object["color"] or not object["color"])):
                        result.append(eachObject)
        
        return result