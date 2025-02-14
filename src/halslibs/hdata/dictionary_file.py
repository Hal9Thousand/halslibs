import os, json

class dictionary_file: 
 
    def __init__(self, file_name: str, data: dict = None):
        """
                
        """
        self.file_name = file_name
        if data is not None:
            self.__cache = data
        else:
            if not os.path.exists(self.file_name):
                self.__cache = {}

    @property
    def __cache(self):
        if os.path.exists(self.file_name):  
            with open(self.file_name, 'r') as file: 
                return json.load(file) 

    @__cache.setter
    def __cache(self, value: dict): 
        with open(self.file_name, 'w') as file:
            file.write(json.dumps(value, indent=2)) 
    
    def get(self, key, default=None): 
        return self.__cache.get(key, default)
    
    def __getitem__(self, key):
        return self.__cache[key] if key in self.__cache else None

    def __setitem__(self, key, value):
        self.__cache = {**self.__cache, **{key:value}} 

    def __delitem__(self, key):
        if key in self.__cache:
            tmp___cache = self.__cache.copy()
            del tmp___cache[key]
            self.__cache = tmp___cache
 
    def __str__(self):
        return json.dumps(self.__cache)

    def __repr__(self):
        return f"__cacher({self.file_name}, {self.__cache})"
    
    def __iter__(self):  
        return iter(self.__cache.items())
    
    def items(self): 
        return iter(self.__cache.items())
    
    def keys(self): 
        return self.__cache.keys()
    
    def values(self): 
        return self.__cache.values()
    
    def __dict__(self): 
        return self.__cache
     