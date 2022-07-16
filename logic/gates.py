from .settings import *
class Gate:
    def __init__(self, surface, pos, scale=1, color=(255, 255, 255)):
        self.surface = surface
        self.pos = pos
        self.scale = scale
        self.normal_color = self.color = color
        self.thickness=1
        self.length = 30*self.scale
        self.is_deleted = False
        self.selection_color = (0,0,255)
        self.selected_color = (0,255,0)
        self.arc_width = 35*scale
        self.mouse = Mouse(2)
        self.clicked=False # this variable turns True only when mouse is get clicked on the gate
        self.gate_selected = True # this variable turns on when ever the mouse is on the the gate and not clicked
        self.ym = None
        self.xm = None
        self.node1 = Node(self.surface,(self.pos[0]-self.length/2, self.pos[1]+ self.length/4))
        self.node2 = Node(self.surface,(self.pos[0]-self.length/2, self.pos[1]+ self.length*0.75))
        self.out_put = Node(self.surface, (self.pos[0]+self.length/2+self.arc_width*2/3,self.pos[1]+self.length/2 ))
        self.node1.movable = False
        self.node2.movable = False
        self.out_put.movable = False
        self.circle_divisor = 2 # this variable made specified for not gate which its selection circle is smaller than other gates
    def _edit_pos(self):
        self.color = self.normal_color
        x,y = pygame.mouse.get_pos()
        center = (self.pos[0]+self.length/4+self.arc_width/4, self.pos[1]+self.length/2 )
        dist= ((center[0]-x )**2+(center[1]-y )**2)**0.5
        if  not pygame.mouse.get_pressed()[2] and dist<=self.length/2:
            self.color = self.selection_color
            pygame.draw.circle(self.surface, self.selection_color, center, self.length/4 )
        if self.mouse.is_clicked() and dist<=self.length/2:
            self.xm,self.ym = pygame.mouse.get_pos()
            self.xm -=self.pos[0]
            self.ym -=self.pos[1]
            self.clicked = True
        elif not pygame.mouse.get_pressed()[2]:
            self.clicked = False
        if self.clicked:
            if pygame.key.get_pressed()[pygame.K_DELETE]:
                self.is_deleted = True
            x,y = pygame.mouse.get_pos()
            self.pos=(-self.xm + x, -self.ym + y)
            center = (self.pos[0]+self.length/4+self.arc_width/4, self.pos[1]+self.length/2 )
            self.color = self.selected_color
            pygame.draw.circle(self.surface, self.selected_color, center, self.length/4 )
        self.node1.color = self.color
        self.node2.color = self.color
        self.out_put.color = self.color
        self.node1.pos = (self.pos[0]-self.length/2, self.pos[1]+ self.length/4)
        self.node2.pos = (self.pos[0]-self.length/2, self.pos[1]+ self.length*0.75)
        self.out_put.pos = (self.pos[0]+self.length/2+self.arc_width*2/3,self.pos[1]+self.length/2 )

class AndGate(Gate):
    def __init__(self, surface, pos, scale=1, color=(255, 255, 255)):
        super().__init__( surface, pos, scale=1, color=(255, 255, 255))

    def draw(self):
        self._edit_pos()
        self.out_put.active = self.node1.active and self.node2.active
        pygame.draw.line(self.surface, self.color, self.pos,(self.pos[0],self.pos[1]+self.length), self.thickness)
        pygame.draw.line(self.surface, self.color, self.pos,(self.pos[0]+self.length/2,self.pos[1]), self.thickness)
        pygame.draw.line(self.surface, self.color, (self.pos[0],self.pos[1]+self.length),(self.pos[0]+self.length/2,self.pos[1]+self.length), self.thickness)
        draw_arc(self.surface, self.color, (self.pos[0]+self.length/2,self.pos[1]), self.arc_width*self.scale, self.length)
        pygame.draw.line(self.surface, self.color, (self.pos[0], self.pos[1]+ self.length/4), (self.pos[0]-self.length/2, self.pos[1]+ self.length/4))
        pygame.draw.line(self.surface, self.color, (self.pos[0], self.pos[1]+ self.length*0.75), (self.pos[0]-self.length/2, self.pos[1]+ self.length*0.75))
        self.node1.draw()
        self.node2.draw()
        self.out_put.draw()

class OrGate(Gate):
    def __init__(self, surface, pos, scale=1, color=(255, 255, 255)):
        super().__init__( surface, pos, scale=1, color=(255, 255, 255))

    def draw(self):
        self._edit_pos()
        self.out_put.active = self.node1.active or self.node2.active
        draw_arc(self.surface, self.color, self.pos, self.arc_width*self.scale/2, self.length)
        self.node1.pos = (self.pos[0]-self.length/2, self.pos[1]+ self.length/4)
        self.node2.pos = (self.pos[0]-self.length/2, self.pos[1]+ self.length*0.75)
        self.out_put.pos = (self.pos[0]+self.length/2+self.arc_width*2/3,self.pos[1]+self.length/2 )
        pygame.draw.line(self.surface, self.color, self.pos,(self.pos[0]+self.length/2,self.pos[1]), self.thickness)
        pygame.draw.line(self.surface, self.color, (self.pos[0],self.pos[1]+self.length),(self.pos[0]+self.length/2,self.pos[1]+self.length), self.thickness)
        draw_arc(self.surface, self.color, (self.pos[0]+self.length/2,self.pos[1]), self.arc_width*self.scale, self.length)
        pygame.draw.line(self.surface, self.color, (self.pos[0], self.pos[1]+ self.length/4), (self.pos[0]-self.length/2, self.pos[1]+ self.length/4))
        pygame.draw.line(self.surface, self.color, (self.pos[0], self.pos[1]+ self.length*0.75), (self.pos[0]-self.length/2, self.pos[1]+ self.length*0.75))
        self.node1.draw()
        self.node2.draw()
        self.out_put.draw()


class NotGate(Gate):
    def __init__(self, surface, pos, scale=1, color=(255, 255, 255)):
        super().__init__( surface, pos, scale=1, color=(255, 255, 255))
        self.node1=self.node2 = Node(self.surface,(self.pos[0]-15, self.pos[1]+ self.length/2))
        self.out_put = Node(self.surface,(self.pos[0]+self.arc_width, self.pos[1]+ self.length/2))
        self.node1.movable = False
        self.node2.movable = False
        self.out_put.movable = False

    def draw(self):
        self._edit_pos()
        self.out_put.active = not(self.node1.active or self.node2.active)
        self.node1.pos = (self.pos[0]-15, self.pos[1]+ self.length/2)
        self.out_put.pos = (self.pos[0]+self.arc_width, self.pos[1]+ self.length/2)
        pygame.draw.line(self.surface, self.color, self.pos,(self.pos[0],self.pos[1]+self.length), self.thickness)
        pygame.draw.line(self.surface, self.color, self.pos,(self.pos[0]+self.arc_width, self.pos[1]+ self.length/2), self.thickness)
        pygame.draw.line(self.surface, self.color, (self.pos[0], self.pos[1]+self.length),(self.pos[0]+self.arc_width, self.pos[1]+ self.length/2), self.thickness)
        pygame.draw.line(self.surface, self.color, (self.pos[0], self.pos[1]+self.length/2),(self.pos[0]-15, self.pos[1]+ self.length/2), self.thickness)
        self.node1.draw()
        self.out_put.draw()

class AndButton(AndGate):
    def __init__(self, surface, pos, scale=1, color=(255, 255, 255)):
        super().__init__(surface, pos, scale=1, color=(255, 255, 255))
        self.static_pos = pos
        self.moved = False
    def check_moved(self):
        if self.pos !=self.static_pos and not self.moved:
            self.moved = True
            return 1
        elif self.pos ==self.static_pos:
            self.moved = False
            return 0
class OrButton(OrGate):
    def __init__(self, surface, pos, scale=1, color=(255, 255, 255)):
        super().__init__(surface, pos, scale=1, color=(255, 255, 255))
        self.static_pos = pos
        self.moved = False
    def check_moved(self):
        if self.pos !=self.static_pos and not self.moved:
            self.moved = True
            return 1
        elif self.pos ==self.static_pos:
            self.moved = False
            return 0
class NotButton(NotGate):
    def __init__(self, surface, pos, scale=1, color=(255, 255, 255)):
        super().__init__(surface, pos, scale=1, color=(255, 255, 255))
        self.static_pos = pos
        self.moved = False
    def check_moved(self):
        if self.pos !=self.static_pos and not self.moved:
            self.moved = True
            return 1
        elif self.pos ==self.static_pos:
            self.moved = False
            return 0


def convert_button_to_gate(button):
    if type(button) is AndButton:
        return AndGate(SURFACE, button.pos)
    elif type(button) is OrButton:
        return OrGate(SURFACE, button.pos)
    elif type(button) is NotButton:
        return NotGate(SURFACE, button.pos)

def class_name_gate(button):
    if type(button) is AndGate:
        return "AndGate"
    elif type(button) is OrGate:
        return "OrGate"
    elif type(button) is NotGate:
        return "NotGate"

def extract_gates_data(gates):
    new_gates = []
    for gate in gates:
        data = [gate.pos,class_name_gate(gate)]
        new_gates.append(data)
    return new_gates

def return_back_gates_after_saved(gates_dics):
    l_gates = []
    for gate in gates_dics:
        if gate[1]=="AndGate":
            l_gates.append(AndGate(SURFACE, gate[0]))
        elif gate[1]=="OrGate":
            l_gates.append(OrGate(SURFACE, gate[0]))
        elif gate[1]=="NotGate":
            l_gates.append(NotGate(SURFACE, gate[0]))
    return l_gates
