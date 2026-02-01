import os
import json

class CacheHandler :
    
    def __init__(self):
        self.cache_path = "cache/cache.json"
        
        self.default_cache = {"between" : "1", "and" : "2", "amount" : "2"}
    
        if os.path.exists(self.cache_path):
            with open(self.cache_path) as f:
                self.cache = json.load(f)
        
        if not os.path.exists(self.cache_path):
            with open(self.cache_path, "w+") as f:
                json.dump(self.default_cache, f, indent=4)
            with open(self.cache_path) as f:
                self.cache = json.load(f)
            