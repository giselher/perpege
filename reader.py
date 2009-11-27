# Attetion: Undocumented

# I hope that you will understand that i will never ever comment this, because i 
# have written this script in a night i was so tired that i even didn't know what 
# i am doing and i am happy that this damn script works as it should.

# for the python2.5 users
from __future__ import with_statement
import xml.etree.ElementTree as etree


class Reader(object):
    def __init__(self, main_path):
        self.path = (main_path if main_path[-1] == '/' else main_path+'/')
            
    def readActFile(self, filename):
        npcdata = {'filename':filename}
        
        with open(self.path+filename) as f:
            lines = f.readlines()
                
        lists = ['dialogs']
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
        with open(self.path+filename, 'r') as f:
            data = {}
            txt = f.read()
            
            # remove the comments
            uncomment = txt.split('\n')
            for line in uncomment:
                if line.strip().startswith('#'):
                    uncomment.pop(uncomment.index(line))
            txt = '\n'.join(uncomment)
            
            ft_txt = txt.replace('\n', '').replace('{', ':::').replace('}', ':::')
            parts = ft_txt.split(':::')
            for key in parts:
                if ';' in key or '' == key: continue 
            
                id = parts.index(key)
                value = parts[id+1]
                
                key = key.replace('=', '').strip()
                value = value.split(';')
                value.pop(-1)
                data[key] = value  
            
            return data
        
    def _readMapNode(self, element):
        type = element.get('type', 'str')
        if type == 'tuple': return eval('%s(%s)' % (type, element.text))
        else: return eval('%s("%s")' % (type, element.text))
        
    def readMapFile(self, filename):
        data = {'filename'  : filename,
                'objects'   : [],
                'actors'    : []
                }
                
        tree = etree.parse(self.path+filename)
        root = tree.getroot()
        
        data['name'] = self._readMapNode(root.find('name'))
        data['ground'] = self._readMapNode(root.find('ground'))
        data['start_position'] = self._readMapNode(root.find('player_start_position'))
        
        for child in root.getiterator('object'):
            filename = self._readMapNode(child.find('filename'))
            position = self._readMapNode(child.find('position'))
            data['objects'].append((filename, position)) 
            
        for child in root.getiterator('actor'):
            filename = self._readMapNode(child.find('filename'))
            position = self._readMapNode(child.find('position'))
            data['actors'].append((filename, position))
            
        return data       