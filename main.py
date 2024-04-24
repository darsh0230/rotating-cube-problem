import math
import pygame
import sys, time
import random


angle = 0.005
factor = 100
frame_rate = 30
cube_pos = [[400, 300]]


class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"3D({self.x:>2}, {self.y:>2}, {self.z:>2})"

    def scale(self, factor):
        return Point3D(self.x * factor, self.y * factor, self.z * factor)

    def translate(self, x, y, z):
        return Point3D(self.x+x, self.y+y, self.z+z)

    def rotate(self, ax1, ax2, angle):
        return (
            ax1 * math.cos(angle) - ax2 * math.sin(angle),
            ax2 * math.cos(angle) + ax1 * math.sin(angle)
        )

    def rotateZ(self, angle):
        (x1, y1) = self.rotate(self.x, self.y, angle)
        return Point3D(x1, y1, self.z)

    def rotateX(self, angle):
        (y1, z1) = self.rotate(self.y, self.z, angle)
        return Point3D(self.x, y1, z1)

    def rotateY(self, angle):
        (x1, z1) = self.rotate(self.x, self.z, angle)
        return Point3D(x1, self.y, z1)

class Button:
    def __init__(self, size, text, pos, bgColor=(255, 255, 255), textColor=(0, 0, 0)):
        self.pos  = pos
        self.size = size
        self.text = text
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.textSurf = self.font.render(f"{text}", True, textColor)
        self.button = pygame.Surface((size[0], size[1])).convert()
        self.button.fill(bgColor)

    def render(self, window):
        window.blit(self.button, (self.pos[0], self.pos[1]))
        window.blit(self.textSurf, (self.pos[0]+5, self.pos[1]+15))

    def clicked(self, events):
        mousePos = pygame.mouse.get_pos()#  get the mouse position
        for event in events:
            if self.button.get_rect(topleft=self.pos).collidepoint(mousePos[0], mousePos[1]):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True
        return False
    

vertices = [Point3D(-1, 1, -1),
            Point3D(1, 1, -1),
            Point3D(1, 1, 1),
            Point3D(-1, 1, 1),
            Point3D(-1, -1, -1),
            Point3D(1, -1, -1),
            Point3D(1, -1, 1),
            Point3D(-1, -1, 1)
            ]

lines = [(0, 1),
         (1, 2),
         (2, 3),
         (3, 0),
         (4, 5),
         (5, 6),
         (6, 7),
         (7, 4),
         (0, 4),
         (3, 7),
         (1, 5),
         (2, 6)
         ]


def rotate():
    global vertices
    new_vertices = []
    for v in vertices:
        new_vertices.append(v.rotateX(angle).rotateY(2*angle).rotateZ(angle/2))
    vertices = new_vertices

def draw_cube(pos):
    for l in lines:
        p1 = vertices[l[0]].scale(factor).translate(pos[0], pos[1], 0)
        p2 = vertices[l[1]].scale(factor).translate(pos[0], pos[1], 0)

        pygame.draw.line(screen, white, (p1.x, p1.y), (p2.x, p2.y), 5)

    # Update the display
    pygame.display.flip()


# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))  # Window size: 800x600
pygame.display.set_caption('Draw a Line with Pygame')  # Window title

# Define colors
white = (255, 255, 255)

change_direction_btn = Button([120, 40], "Change Direction", [50, 50])
velocity_plus_btn = Button([80, 40], "Velocity ++", [200, 50])
velocity_minus_btn = Button([80, 40], "Velocity --", [310, 50])
add_cube_btn = Button([80, 40], "Add cube", [410, 50])
delete_cube_btn = Button([80, 40], "Delete cube", [510, 50])

# Main game loop
running = True
while running:
    st_time = time.time()


    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with black
    screen.fill((0, 0, 0))

    change_direction_btn.render(screen)
    if change_direction_btn.clicked(events):
        angle = -angle
    
    velocity_plus_btn.render(screen)
    if velocity_plus_btn.clicked(events):
        if angle > 0:
            angle += 0.001
        else:
            angle -= 0.001

    velocity_minus_btn.render(screen)
    if velocity_minus_btn.clicked(events):
        if angle > 0:
            angle -= 0.001
        elif angle == 0:
            pass
        else:
            angle += 0.001
    
    add_cube_btn.render(screen)
    if add_cube_btn.clicked(events):
        cube_pos.append([random.randint(0, 600), random.randint(0, 400)])
    
    delete_cube_btn.render(screen)
    if delete_cube_btn.clicked(events):
        if len(cube_pos) > 1:
            cube_pos.pop()

    rotate()
    for cube in cube_pos:
        draw_cube(cube)
    

    # Set max frame rate 
    try:
        time.sleep((1/frame_rate) - (time.time() - st_time))
    except Exception:
        pass

# Quit Pygame
pygame.quit()
sys.exit()
