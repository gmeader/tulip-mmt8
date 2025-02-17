class Track:
    def __init__(self,number):
        self.number = number
        self.status = False
        self.midi_data = []
    def set_status(self,boolean):
        self.status = boolean    

class Song:
    def __init__(self,number):
        self.number = number
        self.name =''
        self.parts=[]

    def set_name(self, name):
        self.name = name
 
    def add_part(self,part_number):
        self.parts.append(part_number) 

class Part:
    def __init__(self,number):
        self.number = number
        self.name = ''
        self.tracks = []

    def set_name(self,name):
        self.name = name

    def add_track(self,track):
        self.tracks.append(track)


