from .settings import *
from .gates import *
from .buttons import *
class Screen:
    def __init__(self,surface):
        self.surface = surface
        self.wires    =[]
        self.gates    =[]
        self.buttons  =[]
        self.gate_buttons = []
        self.offset_bar_buttons=(WIDTH-350)/2
        self.gate_buttons.append(AndButton(self.surface, (30+self.offset_bar_buttons,HEIGHT-35)))
        self.gate_buttons.append(OrButton(self.surface, (100+self.offset_bar_buttons,HEIGHT-35)))
        self.gate_buttons.append(NotButton(self.surface, (170+self.offset_bar_buttons,HEIGHT-35)))
        self.static_buttons = []
        self.static_buttons.append(StaticButton(self.surface, (220+self.offset_bar_buttons,HEIGHT-30)))
        self.static_buttons.append(StaticSwitch(self.surface, (273+self.offset_bar_buttons,HEIGHT-20)))
        self.static_buttons.append(StaticBulb(self.surface, (325+self.offset_bar_buttons,HEIGHT-20)))
        self.static_buttons.append(TextButton(self.surface, (WIDTH-50,HEIGHT-30),"Save") )
        self.static_buttons.append(TextButton(self.surface, (WIDTH-100,HEIGHT-30),"Load") )
        self.offset_x = 0
        self.offset_y = 0
        self.drawing = False
        self.xm,self.ym = None,None
        self.saver = SaveLoad()

    def draw(self):
        self.add_wire()
        self._reduce_nodes()
        normal_wires = []
        coor_wires = {}
        for wire in self.wires:
            coor_wires[(wire.start)]=0
            coor_wires[(wire.end)]=0
        for wire in self.wires:
            dist = ((wire.start.pos[0] - wire.end.pos[0])**2+ (wire.start.pos[1]-wire.end.pos[1])**2)**0.5
            if dist>20:
                normal_wires.append(wire)
                coor_wires[wire.start]+=1
                coor_wires[wire.end]+=1

        self.wires = normal_wires
        for wire in self.wires:
            off_xy_start_divisor=coor_wires[wire.start]
            off_xy_end_divisor=coor_wires.get(wire.end,1)
            wire.start.pos = (wire.start.pos[0]+self.offset_x/off_xy_start_divisor, wire.start.pos[1]+self.offset_y/off_xy_start_divisor)
            wire.end.pos = (wire.end.pos[0]+self.offset_x/off_xy_end_divisor, wire.end.pos[1]+self.offset_y/off_xy_end_divisor)
            wire.draw()
        self.gates = self._remove_is_deleted_objects(self.gates)
        for gate in self.gates:
            gate.pos = (gate.pos[0]+self.offset_x, gate.pos[1]+self.offset_y)
            gate.draw()
        self.buttons = self._remove_is_deleted_objects(self.buttons)
        for button in self.buttons:
            button.pos = (button.pos[0]+self.offset_x, button.pos[1]+self.offset_y)
            button.draw()
        pygame.draw.rect(SURFACE, (10,10,10), (0,HEIGHT-50,WIDTH,50)) # this the place at which all gate buttons are displayed

        for gate_button in self.gate_buttons:
            if gate_button.check_moved():
                self.gates.append(convert_button_to_gate(gate_button))
            gate_button.pos=gate_button.static_pos
            gate_button.draw()

        for static_button in self.static_buttons:
            if static_button.check_moved():
                self.buttons.append(convert_static_to_normal_button(static_button))
            static_button.pos=static_button.static_pos
            static_button.draw()

        if self.static_buttons[-2].pressed: #Save button click check
            if self.saver.file_name is None or self.saver.file_name =="":
                self.saver.create()
            if self.saver.file_name is None:
                return
            gates = extract_gates_data(self.gates)
            buttons = extract_buttons_data(self.buttons)
            wires = ectract_wires_date(self.wires)
            data = {"gates":gates, "buttons":buttons, "wires":wires}
            self.saver.save_data(data)

        if self.static_buttons[-1].pressed: #Load button click check
            self.saver.load_file()
            if self.saver.file_name is None:
                return
            data = self.saver.read_data()
            self.gates = return_back_gates_after_saved(data["gates"])
            self.buttons = return_back_buttons_after_saved(data["buttons"])
            self.wires = return_wires_back_to_object(data["wires"])

    def move_screen(self):
        """
            Here we check if any arrow input is needed to move the screen camera
        """
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.offset_x =-2
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            self.offset_x =2
        elif pygame.key.get_pressed()[pygame.K_UP]:
            self.offset_y =2
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            self.offset_y =-2
        else:
            self.offset_x =0
            self.offset_y =0
    def add_wire(self):
        if pygame.mouse.get_pressed()[0] and not self.drawing and pygame.mouse.get_pos()[1]<HEIGHT-50:
            self.xm,self.ym = pygame.mouse.get_pos()
            self.drawing  = True
        if self.drawing:
            x,y = pygame.mouse.get_pos()
            pygame.draw.line(SURFACE, (0,255,255), (self.xm,self.ym), (x,y))
        if not pygame.mouse.get_pressed()[0] and self.drawing:
            self.drawing = False
            self.wires.append(Wire(SURFACE, (self.xm,self.ym), (x,y)))
            self.xm,self.ym = None,None
    def _remove_is_deleted_objects(self, objects_list):
        none_deleted_elements = []
        for obj in objects_list:
            if not obj.is_deleted:
                none_deleted_elements.append(obj)
        return none_deleted_elements

    def _reduce_nodes(self): # this function reduces number of nodes if any two or more nodes have small distance between each other
        for gate in self.gates:
            for wire in self.wires:
                if self.distance_between_two_nodes(gate.node1, wire.start)<10:
                    wire.start = gate.node1
                elif self.distance_between_two_nodes(gate.node1, wire.end)<10:
                    wire.end = gate.node1
                if self.distance_between_two_nodes(gate.node2, wire.start)<10:
                    wire.start = gate.node2
                elif self.distance_between_two_nodes(gate.node2, wire.end)<10:
                    wire.end = gate.node2
                if self.distance_between_two_nodes(gate.out_put, wire.start)<10:
                    wire.start = gate.out_put
                elif self.distance_between_two_nodes(gate.out_put, wire.end)<10:
                    wire.end = gate.out_put

        for button in self.buttons:
            for wire in self.wires:
                if self.distance_between_two_nodes(wire.start, button.node)<10 and type(button) is not Bulb:
                    wire.start = button.node
                elif self.distance_between_two_nodes(wire.end, button.node)<10 and type(button) is Bulb:
                    wire.end = button.node
        for i in range(len(self.wires)-1):
            for j in range(i+1,len(self.wires)):
                if self.distance_between_two_nodes(self.wires[i].start, self.wires[j].end)<10:
                    self.wires[i].start = self.wires[j].end
                elif self.distance_between_two_nodes(self.wires[j].start, self.wires[i].end)<10:
                    self.wires[j].start = self.wires[i].end

    def distance_between_two_nodes(self, node1, node2):
        x1,y1,x2,y2 = node1.pos[0],node1.pos[1],node2.pos[0],node2.pos[1]
        return ((x2-x1)**2 + (y2-y1)**2)**0.5
