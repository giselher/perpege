# Attetion: Undocumented
# If you need help to understand this script then please contact me (alexander.preisinger@gmail.com, Subject:The ultimate Reader :)) 

##Make an Configuration Reader, because the Panda3D Configuration Handler sucks :)

# for the python2.5 users
from __future__ import with_statement

class Reader(object):
    def __init__(self, main_path):
        self.path = (main_path if main_path[-1] == "/" else main_path+"/")
        self.readers = {'npc' : self.__readNpcFile,
                        'act' : self.__readNpcFile,
                        'dlg' : self.__readDlgFile,
                        'wpn' : self.__readWpnFile,
                        'map' : self.__readMapFile}
    
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
                    mapdata[linedata[0]] = eval(linedata[1])
        return mapdata
    
    def __readNpcFile(self, lines):
        npcdata = dict()
        for line in lines:
            line = line.strip()
            if not line.startswith('#'):
                linedata = line.split('=')
                if linedata[1].startswith(":"):
                    linedata[1] = linedata[1].replace(":", "")
                    data = linedata[1].split(',')
                    if '' in data: data.remove('')
                    x = 0
                    for d in data:                        
                        try:
                            data[x] = int(d)
                            x += 1
                        except ValueError:
                            pass
                    npcdata[linedata[0]] = data 
                else:
                    try:
                        data = int(linedata[1])
                    except ValueError:
                        data = linedata[1]
                    npcdata[linedata[0]] = data
        return npcdata

    def __readWpnFile(self, lines):
        weapondata = dict()
        for line in lines:
            line = line.strip()
            if not line.startswith('#'):
                linedata = line.split('=')
                if (linedata[0] == 'poscor') or (linedata[0] == 'oricor'): 
                    weapondata[linedata[0]] = eval(linedata[1])
                else:
                    weapondata[linedata[0]] = linedata[1]
        return weapondata
                
    def __readDlgFile(self, lines):
        dialog = dict()
        for line in lines: 
            if line.startswith('#'): lines.remove(line)
        content = ''.join(lines)
        counter = 1
        sentences = content.split(':')
        for line in sentences:
            linedata = line.split('=')               
            if not linedata[0].strip() == '': 
                dialog[counter] = linedata
                counter += 1
        return dialog
