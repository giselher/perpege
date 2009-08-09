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
        
        self.store = {'link-content': '',
                      'linking': False}
        self.next_l = False
    
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

                    counter = self.__createDlgContent(counter, line, dialog['content'], 'link-content')
                    counter += 1
                    #print _dialog
                        
        #dialog.update(self._content_adder.solve(self.__createDlgContent))
        #print dialog
        return dialog
    
    def __createDlgContent(self, counter, line, dialog, link_name):
        content = {}
        splitted_line = line.split(':')
        try:
            _line0 = int(splitted_line[0])
            link = link_name + "-%d" % _line0
            _link_counter = link + "-counter"
            if self.store.has_key(link_name):
                if link != self.store[link_name]: 
                    self.store['counter'] = counter
                    counter = 0
                    self.store[_link_counter] = 0
                    dialog[link] = {}
                else:
                    counter = self.store[_link_counter]
            else:
                self.store['counter'] = counter
                counter = 0
                self.store[_link_counter] = 0
                dialog[link] = {}
                #counter = self.store[_link_counter]
            self.store[link_name] = link
            line = ':'.join(splitted_line)[2:]
            counter = self.__createDlgContent(counter, line, dialog[link], link)
            self.store[_link_counter] = counter + 1
            counter = self.store['counter']
        except ValueError:
            if line.startswith('choice'):
                choice = {}
                line_data = line.split('=')
                links = line_data[1].split(';')
                for link in links:
                    link = link.strip()
                    link_data = link.split(':')
                    choice[int(link_data[0])] = link_data[1]
                content["%d-%s" % (counter, line_data[0])] = choice
            elif line.startswith('self') or line.startswith('player'):
                line_data = line.split('=')
                if not line_data[1].startswith('"'): raise SyntaxError('No Text')
                content['%d-%s' % (counter, line_data[0])] = line_data[1]
            elif line.startswith('set'):
                line_data = line.split(' ')
                _line1 = line_data[1]
                _set = '%d-set' % counter
                if _line1.startswith('E_'): 
                    content[_set] = _line1
                elif len(line_data) > 2:
                    content[_set]= _line1 +"=="+ line_data[2]
                elif _line1.startswith('EQ_'):
                    content[_set] = '%s==ACCEPTED' % _line1
            else:
                counter -= 1
        dialog.update(content)
        return counter