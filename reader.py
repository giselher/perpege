# Attetion: Undocumented

# I hope that you will understand that i will never ever comment this, because i 
# have written this script in a night i was so tired that i even didn't know what 
# i am doing and i am happy that this damn script works as it should.

# for the python2.5 users
from __future__ import with_statement

class Reader(object):
    def __init__(self, main_path):
        self.path = (main_path if main_path[-1] == "/" else main_path+"/")
        self.readers = {'act' : self.__readActFile,
                        'dlg' : self.__readDlgFile,
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
                        if '' in data: data.remove('')
                    else:
                        try:
                            data = int(linedata[1])
                        except ValueError:
                            data = linedata[1]
                    npcdata[linedata[0]] = data 
        return npcdata

    def __readDlgFile(self, lines):
        dialog = {  'requirements': {},
                    'content': {}}      
        _content_adder = ContentAdder()
        counter = 0
        for line in lines: 
            line = line.strip() 
            if not line.startswith('#') or line != '':
                if line.startswith('if'):
                    line_data = line.split(' ')
                    _line1 = line_data[1]
                    if _line1.startswith('E_'): 
                        dialog['requirements'][_line1] = None
                    elif len(line_data) > 2:
                        try:
                            _line2 = int(line_data[2])
                        except ValueError:
                            _line2 = line_data[2]
                        dialog['requirements'][_line1] = _line2
                    elif _line1.startswith('EQ_'):
                        dialog['requirements'][_line1] = 'ACCEPTED'
                else:
    
                    if line.startswith('choice'):
                        choice = {}
                        line_data = line.split('=')
                        links = line_data[1].split(';')
                        for link in links:
                            link = link.strip()
                            link_data = link.split(':')
                            choice[link_data[0]] = link_data[1]
                        dialog['content']["%d-%s" % (counter, line_data[0])] = choice
                        _content_adder.addChoice()
                        counter += 1
                    elif line.startswith(':'):
                        _content_adder.storeLine(line)
                    elif line.startswith('self') or line.startswith('player'):
                        line_data = line.split('=')
                        dialog['content']['%d-%s' % (counter, line_data[0])] = line_data[1]
                        counter += 1
                    elif line.startswith('set'):
                        line_data = line.split(' ')
                        _line1 = line_data[1]
                        _set = '%d-set' % counter
                        if _line1.startswith('E_'): 
                            dialog['content'][_set] = _line1
                        elif len(line_data) > 2:
                            dialog['content'][_set]= line1 +"=="+_line2
                        elif _line1.startswith('EQ_'):
                            dialog['content'][_set] = '%s==ACCEPTED' % _line1
                    elif line.startswith('end'):
                        line = line.replace('end:', '')
                        line_data = line.split('=')
                        dialog['content']['end-%s' % line_data[0]] = line_data[1]
                        
       # _content_adder.solve(sefl__createDlgContent)
        print dialog  
        return dialog

            
    def __createDlgContent(sefl, line):
        dialog = {'content': {}}
        if line.startswith('choice'):
            choice = {}
            line_data = line.split('=')
            links = line_data[1].split(';')
            for link in links:
                link = link.strip()
                link_data = link.split(':')
                choice[link_data[0]] = link_data[1]
            dialog['content']["%d-%s" % (counter, line_data[0])] = choice
            _content_adder.addChoice()
            counter += 1
        elif line.startswith(':'):
            _content_adder.storeLine(line)
        elif line.startswith('self') or line.startswith('player'):
            line_data = line.split('=')
            dialog['content']['%d-%s' % (counter, line_data[0])] = line_data[1]
            counter += 1
        elif line.startswith('set'):
            line_data = line.split(' ')
            _line1 = line_data[1]
            _set = '%d-set' % counter
            if _line1.startswith('E_'): 
                dialog['content'][_set] = _line1
            elif len(line_data) > 2:
                dialog['content'][_set]= line1 +"=="+_line2
            elif _line1.startswith('EQ_'):
                dialog['content'][_set] = '%s==ACCEPTED' % _line1
        elif line.startswith('end'):
            line = line.replace('end:', '')
            line_data = line.split('=')
            dialog['content']['end-%s' % line_data[0]] = line_data[1]
        return dialog
        
class ContentAdder(object):
    
    def __init__(self):
        self.choice= 0
        self.content = {}
        
    def addChoice(self):
        self.choice += 1
        self.content[self.choice] = []
        
    def storeLine(self, line):
        self.content[self.choice].append(line)
        
    def solve(self, function):
        _dict = {}
        for choice in self.content:
            for line in choice:
                _dict.update(function(line))
        print _dict
                
    def prepare(self, link, dict):
        pass
                