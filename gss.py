# Sorry:This is an old script and the translations sucks, but it works :)

import os, pickle

class Saver(object):
    """Save Python Objects with an key to load it Later with the GSS Loader an 
    the used key.
    
    Creates the folders automaticly"""
    def __init__(self, path):
        self.saved = True
        self.path = ""
        self.setPath(path)
        self.savedictonary = {}
        
    def prepare(self, value, key):
        """Prepares the given Python Object for saving with the save method.
        
        An Python Object can be a list, tuple, dictonayr, string, integer, float 
        and so on. 
        It can not be an operater or something like this.
        """
        self.savedictonary[key] = value
        self.saved = False
        
    def save(self, filename):
        """return dict
        
        Saves all objects from the dictonary in the given file and clears
        the dictonary to use it for other objects.
        
        Creates the file automaticly.
        """
        if self.saved == False:
            savfile = open(self.path + filename, "wb")
            pickle.dump(self.savedictonary, savfile, 1)
            savfile.close()
            self.savedictonary = {}
            self.saved = True
        else:
            print "SaverError: You have to prepare values, before you can save them"
            
    def setPath(self, path):
        """Use it to set a new path for the Saver.
        
        Creates the folders automaticly."""
        self.path = (path if path[-1] == "/" else path+"/")
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        
class Loader(object):
    """Use it to load file, that was saved with the GSS Saver.
    
    Please use a path that realy exists."""
    def __init__(self, path):
        self.loaded = False
        self.path = "" 
        self.setPath(path)
        self.loaddictonary = {}
        
    def load(self, filename):
        """Load a dictonary from the given file to get the Python Object with the 
        get method.
        
        Please use a file that realy exists.
        """
        try:
            file = open(self.path + filename, "rb")
            ldict = pickle.load(file)
            file.close()
            self.loaddictonary.update(ldict)
            self.loaded = True
        except IOError:
            print "IOError: the file \"" + filename + "\" does not exists" 
        
    def get(self, key):
        """return Python Object
        
        returns the Python Object with the given key and remove it from the 
        dictonary. If the dictonary is empty, then you can load another dictonary."""
        if self.loaded == True:
            try:
                return self.loaddictonary.pop(key)
                if len(self.loaddictonary.keys()) == 0: self.loaded = False                
            except KeyError:
                print "KeyError: Key \"" + key + "\" does not exist"  
        else:
            print "LoaderError: You have to load a file, before you can use it \nor all values are removed from the dictonary"
            
    def setPath(self, path):
        """Set a new path for the Loader."""
        self.path = (path if path[-1] == "/" else path+"/")