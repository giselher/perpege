# Attetion: Undocumented

# I hope that you will understand that i will never ever comment this, because i 
# have written this script in a night i was so tired that i even didn't know what 
# i am doing and i am happy that this damn script works as it should.

# for the python2.5 users
from __future__ import with_statement
import xml.etree.ElementTree as etree


class Reader(object):
    def __init__(self, main_path):
        self.path = (main_path if main_path[-1] == "/" else main_path+"/")
        self.readers = {'act' : self.__readActFile,
                        'map' : self.__readMapFile}
        
        self.content = {}
        self.counter = 0
        self.store = {}
        self.boolChoice = False
    
    def readFile(self, filename):
        with open(self.path+filename) as f:
            for reader in self.readers.keys():
                if filename.endswith(reader): 
                    data = self.readers[reader](f.readlines())
                    data["filename"] = filename
                    return data
                
    def __readMapFile(self, lines):
        mapdata = dict()
        lines = ''.join(lines).split(';')
        for line in lines:
            if line == '': continue
            line = line.strip() 
            if not line.startswith('#'):
                linedata = line.split('=')
                if len(linedata) == 2:
                    if linedata[1].startswith('[') or linedata[1].startswith('(') \
                            or linedata[1].startswith('"'):
                        mapdata[linedata[0]] = eval(linedata[1])
        return mapdata
    
    def __readActFile(self, lines):
        lists = ['dialogs']
        npcdata = dict()
        for line in lines:
            line = line.strip()
            if not line.startswith('#') and line != '' :
                linedata = line.split('=')
                _line0 = linedata[0]
                _line1 = linedata[1]
                if len(linedata) > 1:
                    if _line0 in lists:
                        if ',' in _line1: data =  _line1.split(',')
                        else: data = [_line1]
                        _data = []
                        for i in data:
                            if i != '':
                                _data.append(i.strip())
                        data = _data
                    else:
                        try:
                            data = int(linedata[1])
                        except ValueError:
                            data = linedata[1]
                    npcdata[linedata[0]] = data 
        return npcdata
        
    def readDlgFile(self, filename):
        with open(self.path+filename, "r") as f:
            data = {}
            txt = f.read()
            ft_txt = txt.replace("\n", "").replace("{", ":::").replace("}", ":::")
            parts = ft_txt.split(":::")
            for key in parts:
                if ";" in key or "" == key: continue 
            
                id = parts.index(key)
                value = parts[id+1]
                
                key = key.replace("=", "").strip()
                value = value.split(";")
                value.pop(-1)
                data[key] = value  
            
            return data
        
    def __readMapNode(self, element):
        type = element.get("type", "str")
        if type == "tuple": return eval("%s(%s)" % (type, element.text))
        else: return eval("%s('%s')" % (type, element.text))
        
    
        
    def readMapFile(self, filename):
        data = {"objects"   : [],
                "actors"    : []
                }
                
        tree = etree.parse(self.path+filename)
        root = tree.getroot()
        
        data["name"] = self.__readMapNode(root.find("name"))
        data["ground"] = self.__readMapNode(root.find("ground"))
        data["start_position"] = self.__readMapNode(root.find("player_start_position"))
        
        for child in root.getiterator("object"):
            filename = self.__readMapNode(child.find("filename"))
            position = self.__readMapNode(child.find("position"))
            data["objects"].append((filename, position)) 
            
        for child in root.getiterator("actor"):
            filename = self.__readMapNode(child.find("filename"))
            position = self.__readMapNode(child.find("position"))
            data["actors"].append((filename, position))
            
        return data       