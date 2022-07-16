import pygame, sys, math, json, os
from tkinter import filedialog as fd
import tkinter

WIDTH = 1366
HEIGHT = 768
# for i in range(len(all_nodes)-1):
#     for j in range(i+1,len(all_nodes)):
# WIDTH = 800
# HEIGHT = 600
pygame.init()
clock = pygame.time.Clock()
SURFACE = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)
pygame.display.set_caption("Logic Simulator")
def draw_arc(surface, color, pos, width, height, start_angle=math.pi*3/2, end_angle = math.pi/2):
    pygame.draw.arc(surface, color, (pos[0]-width/2,pos[1],width,height),start_angle,end_angle)

class Mouse:
    def __init__(self, index):
        self.index = index
        self.clicked = 0
        self.state = 0
    def is_clicked(self):
        if pygame.mouse.get_pressed()[self.index]:
            self.clicked = 1
        if self.clicked==1 and self.state==0:
            self.state=1
            return 1
        elif self.state==1 and pygame.mouse.get_pressed()[self.index]:
            return 0
        if not pygame.mouse.get_pressed()[self.index]:
            self.state=0
            self.clicked=0
class Node:
    def __init__(self, surface, pos, scale=1, color=(255, 255, 255)):
        self.class_self = self
        self.surface = surface
        self.pos = pos
        self.scale = scale
        self.active = False # active means electricity pass throygh this Node
        self.color = color
        self.selection_color = (0, 0, 255)
        self.active_color = (255, 0, 0)
        self.inactive_color = (0, 0, 0)
        self.selected = False
        self.radius=5
        self.clicked = 0
        self.mouseR = Mouse(2)
        self.xm = None
        self.ym = None
        self.movable = True

    def draw(self):
        self.selected = False
        if self.movable:
            self._edite_pos()
        x,y = pygame.mouse.get_pos()
        dist= ((x-self.pos[0] )**2+(y-self.pos[1] )**2)**0.5
        if dist<=self.radius:
            color = self.selection_color
            self.selected = True
        elif self.active:
            color = self.active_color
        else:
            color = self.inactive_color
            self.selected = False
        pygame.draw.circle(self.surface, self.color, self.pos, self.radius, 1)
        pygame.draw.circle(self.surface, color, self.pos, self.radius-3)

    def _edite_pos(self):
        x,y = pygame.mouse.get_pos()
        dist= ((x-self.pos[0] )**2+(y-self.pos[1] )**2)**0.5
        if self.mouseR.is_clicked() and dist<=self.radius+3:
            self.xm,self.ym = pygame.mouse.get_pos()
            self.xm -=self.pos[0]
            self.ym -=self.pos[1]
            self.clicked = True
        elif not pygame.mouse.get_pressed()[2]:
            self.clicked = False
        if self.clicked:
            x,y = pygame.mouse.get_pos()
            self.pos=(-self.xm + x, -self.ym + y)
class Wire:
    def __init__(self, surface, start, end, color = (255, 255, 255)): # start is Node object and also the end
        self.surface = surface
        self.start = Node(self.surface,start, color = (0,255,0))
        self.end = Node(self.surface,end, color = (255,255,0))
        self.thickness = 1
        self.color = color # normal color
        self.active_color = (255, 0, 0)

    def draw(self):
        if self.start is None or self.end is None:
            return 1
        if self.start.active:
            pygame.draw.line(self.surface, self.active_color, self.start.pos, self.end.pos, self.thickness)
            self.end.active = True
        else:
            pygame.draw.line(self.surface, self.color, self.start.pos, self.end.pos, self.thickness)
            self.end.active = False
        self.start.draw()
        self.end.draw()

class SaveLoad:
    def __init__(self):
        self.file_name = None

    def create(self): # Create a json file when name is None (on saving file and not found the file so we will create one)
        if self.file_name is None:
            filetypes = (('logic files', '*.json'),('All files', '*.*'))
            wind = tkinter.Tk()
            wind.geometry("1x1+100000+100000") # this to put the pop-up window very far
            file_name = fd.asksaveasfilename(title='Save As', defaultextension=".json" ,initialdir=os.getcwd(),filetypes=filetypes)
            if file_name =="":
                pass
            else:
                self.file_name = file_name
            wind.destroy()

    def load_file(self):
        filetypes = (('logic files', '*.json'),('All files', '*.*'))
        wind = tkinter.Tk()
        wind.geometry("1x1+100000+100000")
        file_name = fd.askopenfilename(title='Open files',initialdir=os.getcwd(),filetypes=filetypes)
        if file_name=="":
            pass
        else:
            self.file_name = file_name
        wind.destroy()
    def save_data(self,data):
        with open(f'{self.file_name}','w') as f:
            dic=json.dumps(data)
            f.write(dic)
            print("saved")
    def read_data(self):
        with open(f'{self.file_name}','r') as f:
            data=json.load(f)
            return data
    def __getitem__(self,key):
        with open(f'{self.file_name}','r') as f:
            data=json.load(f)
            return data.get(key)
    def __repr__(self):
        with open(f'{self.file_name}','r') as f:
            return str(json.load(f))

def ectract_wires_date(wires):
    l_wires = []
    for wire in wires:
        data = [wire.start.pos,wire.end.pos]
        l_wires.append(data)
    return l_wires
def return_wires_back_to_object(wires):
    l_wires = []
    for wire in wires:
        l_wires.append(Wire(SURFACE, wire[0], wire[1]))
    return l_wires

def distance_between_two_nodes(node1, node2):
    x1,y1,x2,y2 = node1.pos[0],node1.pos[1],node2.pos[0],node2.pos[1]
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

def reduce_nodes(gates, buttons, wires):
    all_nodes = []
    for gate in gates:
        all_nodes.append(gate.node1)
        all_nodes.append(gate.node2)
        all_nodes.append(gate.out_put)
    for wire in wires:
        all_nodes.append(wire.start)
        all_nodes.append(wire.end)
    for button in buttons:
        all_nodes.append(button.node)
    new_nodes = []
    for i in range(len(all_nodes)-1):
        for j in range(i+1,len(all_nodes)):
            node1 = all_nodes[i]
            node2 = all_nodes[j]
            if distance_between_two_nodes(node1,node2)<10:
                node1=node2
