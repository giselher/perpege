"""
@author Alexander Preisinger


"""

class Log(object):
    
    def __init__(self):
        self.__logfile = open("log.txt", "a")
        self.__func = None
        
    def __call__(self, obj):
        self.__func = obj
        self.__logfile.write(str(obj)+":")
        return self.__writeArgs
    
    def __writeArgs(self, *args):
        self.__logfile.write(str(*args)+"\n")
        return self.__func
    
    def __del__(self):
        self.__logfile.close()

class Cache(object):
    
    def __init__(self):
        self.__cache = {}
        self.__func = None
        
    def __cachedFunc(self, *args):
        _args = repr(args)
        if _args not in self.__cache:
            self.__cache[_args] = self.func(*args)
        return self.__cache[_args]
    
    def __call__(self, func):
        self.func = func
        return self.__cachedFunc
    