import sys, os, soya, random

soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

scene = soya.World()



class Head(soya.Body):
    
    def __init__(self, parent):
        soya.Body.__init__(self, parent, soya.Model.get("caterpillar_head"))
        self.speed = soya.Vector(self, 0.0, 0.0, -0.2)
        self.rotation_speed = 0.0
    
    def begin_round(self):
        soya.Body.begin_round(self)
        self.rotation_speed = random.uniform(-25.0, 25.0)
    
    def advance_time(self, proportion):
        soya.Body.advance_time(self, proportion)
        self.rotate_y(proportion * self.rotation_speed)
        self.add_mul_vector(proportion, self.speed)

head = Head(scene)

light = soya.Light(scene)
light.set_xyz(2.0, 5.0, 0.0)

camera = soya.Camera(scene)
soya.set_root_widget(camera)
camera.set_xyz(0.0, 15.0, 15.0)
camera.look_at(head)

soya.MainLoop(scene).main_loop()