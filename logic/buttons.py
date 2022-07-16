from .settings import *
class Clicker:
    def __init__(self, surface, pos, color=(255,255,255)):
        self.surface = surface
        self.pos = pos
        self.outer_color = color
        self.color = (0,0,0) # this color is the normal start color and the color if the switch or bulb is in active
        self.active_color = (255,0,0) # this color is color generated when the object emites electricity or gets electricity
        self.selection_color = (0,0,255) # this color is displayed when the cursor is on the object
        self.selected_color=(0,255,0) # this color is displayed when the left mouse button is pressed to drag the object
        self.width = 15
        self.height = 20
        self.is_deleted = False
        self.node = Node(self.surface, (self.pos[0]+self.width+5, self.pos[1]+self.height/2))
        self.node.movable = False
        self.mouseR = Mouse(2)
        self.mouseL = Mouse(0)
        self.xm,self.ym = None,None
        self.clicked = False
    def _edit_pos(self):
        x,y = pygame.mouse.get_pos()
        is_inside = ((x-self.pos[0] )**2+(y-self.pos[1] )**2)**0.5 < self.width
        if self.mouseR.is_clicked() and is_inside:
            self.xm,self.ym = pygame.mouse.get_pos()
            self.xm -=self.pos[0]
            self.ym -=self.pos[1]
            self.clicked = True
            self.color = self.selection_color
        elif not pygame.mouse.get_pressed()[2]:
            self.clicked = False
        if self.clicked:
            if pygame.key.get_pressed()[pygame.K_DELETE]:
                self.is_deleted = True
            x,y = pygame.mouse.get_pos()
            self.pos=(-self.xm + x, -self.ym + y)

class Button(Clicker):
    def __init__(self, surface, pos, color=(255,255,255)):
        super().__init__(surface, pos, color=(255,255,255))
        self.width = 20

    def draw(self):
        self._edit_pos()
        x,y = pygame.mouse.get_pos()
        is_inside = x>=self.pos[0] and x<=self.pos[0]+ self.width and y>=self.pos[1] and y<= self.pos[1]+self.height
        self.color = (0,0,0)
        self.node.active = False
        if is_inside and not pygame.mouse.get_pressed()[2]:
            self.color = self.selection_color
            if pygame.mouse.get_pressed()[0]:
                self.color = self.active_color
                self.node.active = True
        if self.clicked:
            self.color = self.selected_color
        self.node.pos =(self.pos[0]+self.width+5, self.pos[1]+self.height/2)
        pygame.draw.rect(self.surface, self.outer_color, (self.pos[0], self.pos[1], self.width, self.height),3)
        pygame.draw.rect(self.surface, self.color, (self.pos[0]+5, self.pos[1]+5, self.width-10, self.height-10))
        self.node.draw()

class Switch(Clicker):
    def __init__(self, surface, pos, color=(255,255,255)):
        super().__init__(surface, pos, color=(255,255,255))

    def draw(self):
        self._edit_pos()
        x,y = pygame.mouse.get_pos()
        is_inside = ((x-self.pos[0] )**2+(y-self.pos[1] )**2)**0.5 < self.width
        if is_inside and self.mouseL.is_clicked():
            if self.node.active:
                self.node.active = False
                self.color = (0,0,0)
            elif not self.node.active:
                self.node.active = True
                self.color = self.active_color
        if self.node.active:
            self.color = self.active_color
        else:
            self.color = (0,0,0)
        if is_inside and not pygame.mouse.get_pressed()[2]:
            self.color = self.selection_color
        if self.clicked:
            self.color = self.selected_color
        self.node.pos =(self.pos[0]+self.width/2+10, self.pos[1])
        pygame.draw.circle(self.surface, self.outer_color, (self.pos[0], self.pos[1]),self.width,2)
        pygame.draw.circle(self.surface, self.color, (self.pos[0], self.pos[1]),self.width-3)
        self.node.draw()

class Bulb(Clicker):
    def __init__(self, surface, pos, color=(255,255,255)):
        super().__init__(surface, pos, color=(255,255,255))
        self.node = Node(surface, (self.pos[0]-self.width/2-10, self.pos[1]))
        self.node.movable = False
    def draw(self):
        self._edit_pos()
        x,y = pygame.mouse.get_pos()
        is_inside = ((x-self.pos[0] )**2+(y-self.pos[1] )**2)**0.5 < self.width
        if self.clicked:
            self.color = self.selected_color
        elif is_inside and not pygame.mouse.get_pressed()[2]:
            self.color = self.selection_color
        elif self.node.active:
            self.color = self.active_color
        else:
            self.color = (0,0,0)

        self.node.pos =(self.pos[0]-self.width/2-10, self.pos[1])
        pygame.draw.circle(self.surface, self.outer_color, (self.pos[0], self.pos[1]),self.width,2)
        pygame.draw.circle(self.surface, self.color, (self.pos[0], self.pos[1]),self.width-3)
        self.node.draw()

class StaticButton(Button):
    def __init__(self,surface, pos, color=(255,255,255)):
        super().__init__(surface, pos, color=(255,255,255))
        self.static_pos = pos
        self.moved = False
    def check_moved(self):
        if self.pos !=self.static_pos and not self.moved:
            self.moved = True
            return 1
        elif self.pos ==self.static_pos:
            self.moved = False
            return 0
class StaticSwitch(Switch):
    def __init__(self,surface, pos, color=(255,255,255)):
        super().__init__(surface, pos, color)
        self.static_pos = pos
        self.moved = False
    def check_moved(self):
        if self.pos !=self.static_pos and not self.moved:
            self.moved = True
            return 1
        elif self.pos ==self.static_pos:
            self.moved = False
            return 0

class StaticBulb(Bulb):
    def __init__(self,surface, pos, color=(255,255,255)):
        super().__init__(surface, pos, color=(255,255,255))
        self.static_pos = pos
        self.moved = False
    def check_moved(self):
        if self.pos !=self.static_pos and not self.moved:
            self.moved = True
            return 1
        elif self.pos ==self.static_pos:
            self.moved = False
            return 0

class TextButton:
    def __init__(self, surface, pos, text):
        self.surface = surface
        self.pos = self.static_pos = pos
        self.text = text
        self.selection_color = (0,0,255)
        self.clicked_color = (0,255,0)
        self.color = (255,255,255)
        self.my_font = pygame.font.SysFont("HELVETICA",15)
        self.text_renderer = self.my_font.render(self.text,1,self.color)
        selfpos = [pos[0]-self.text_renderer.get_width()//2, pos[1]-self.text_renderer.get_height()//2]
        self.clicked = False
        self.pressed = False # this returns 1 after button is clicked imidiatly and then return to 0
    def draw(self):
        self._check_click()
        self.text_renderer = self.my_font.render(self.text,1,self.color)
        pygame.draw.rect(self.surface, self.color, (self.pos[0]-3, self.pos[1]-1, self.text_renderer.get_width()+6,self.text_renderer.get_height()+3),1)
        self.surface.blit(self.text_renderer,self.pos)
    def _check_click(self):
        x,y = pygame.mouse.get_pos()
        self.pressed = False
        if x>=self.pos[0]-3 and x<=self.pos[0]+self.text_renderer.get_width()+3 and y>=self.pos[1]-1 and y<= self.text_renderer.get_height()+2+self.pos[1]:
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.color = self.clicked_color
                self.clicked = True
                self.pressed = True

            elif not pygame.mouse.get_pressed()[0]:
                self.color = self.selection_color
                self.clicked = False
        else:
            self.color = (255,255,255)
            self.clicked = False
    def check_moved(self):
        return 0

def convert_static_to_normal_button(static_button):
    if type(static_button) is StaticButton:
        return Button(SURFACE, static_button.pos)
    elif type(static_button) is StaticSwitch:
        return Switch(SURFACE, static_button.pos)
    elif type(static_button) is StaticBulb:
        return Bulb(SURFACE, static_button.pos)

def class_name_button(button):
    if type(button) is Button:
        return "Button"
    elif type(button) is Switch:
        return "Switch"
    elif type(button) is Bulb:
        return "Bulb"

def extract_buttons_data(buttons):
    new_buttons = []
    for button in buttons:
        data = [button.pos,class_name_button(button)]
        new_buttons.append(data)
    return new_buttons

def return_back_buttons_after_saved(buttons_dics):
    l_buttons = []
    for button in buttons_dics:
        if button[1]=="Button":
            l_buttons.append(Button(SURFACE, button[0]))
        elif button[1]=="Switch":
            l_buttons.append(Switch(SURFACE, button[0]))
        elif button[1]=="Bulb":
            l_buttons.append(Bulb(SURFACE, button[0]))
    return l_buttons
