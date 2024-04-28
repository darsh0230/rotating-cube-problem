import math
import pygame
import sys
import time
import random


PHI = round((1 + math.sqrt(5)) / 2, 6)


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
        self.pos = pos
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
        mousePos = pygame.mouse.get_pos()  # get the mouse position
        for event in events:
            if self.button.get_rect(topleft=self.pos).collidepoint(mousePos[0], mousePos[1]):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True
        return False


class Entity:
    def __init__(self, pos=None) -> None:
        self.factor = 50
        if pos is None:
            self.pos = [random.randint(200, 1100), random.randint(150, 650)]
        else:
            self.pos = pos

    def rotate(self, angle):
        new_vertices = []
        for v in self.vertices:
            new_vertices.append(
                v.rotateX(angle).rotateY(2*angle).rotateZ(angle/2))
        self.vertices = new_vertices

    def draw(self, pygame, angle):
        self.rotate(angle)
        for l in self.lines:
            p1 = self.vertices[l[0]].scale(self.factor).translate(
                self.pos[0], self.pos[1], 0)
            p2 = self.vertices[l[1]].scale(self.factor).translate(
                self.pos[0], self.pos[1], 0)

            pygame.draw.line(screen, white, (p1.x, p1.y), (p2.x, p2.y), 5)


class Cube(Entity):
    def __init__(self, pos=None) -> None:
        Entity.__init__(self, pos)
        self.vertices = [Point3D(-1, 1, -1),
                         Point3D(1, 1, -1),
                         Point3D(1, 1, 1),
                         Point3D(-1, 1, 1),
                         Point3D(-1, -1, -1),
                         Point3D(1, -1, -1),
                         Point3D(1, -1, 1),
                         Point3D(-1, -1, 1)
                         ]
        self.lines = [(0, 1),
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


class Tetrahedron(Entity):
    def __init__(self, pos=None) -> None:
        Entity.__init__(self, pos)
        self.vertices = [
            Point3D(1, 1, 1),
            Point3D(1, -1, -1),
            Point3D(-1, 1, -1),
            Point3D(-1, -1, 1),
        ]

        self.lines = [
            (0, 1),
            (1, 2),
            (2, 0),
            (0, 3),
            (1, 3),
            (2, 3)
        ]


class Octahedron(Entity):
    def __init__(self, pos=None) -> None:
        Entity.__init__(self, pos)
        self.vertices = [
            Point3D(1, 0, 0),
            Point3D(-1, 0, 0),
            Point3D(0, 1, 0),
            Point3D(0, -1, 0),
            Point3D(0, 0, 1),
            Point3D(0, 0, -1),
        ]

        self.lines = [
            (3, 1),
            (3, 0),
            (3, 4),
            (3, 5),
            (2, 1),
            (2, 0),
            (2, 4),
            (2, 5),
            (5, 1),
            (5, 0),
            (4, 1),
            (4, 0)

        ]


class Dodecahedron(Entity):
    def __init__(self, pos=None) -> None:
        Entity.__init__(self, pos)
        self.factor = 0.75

# vertices_dict = {}
# for i in range(0, len(vertices)):
#     vertices_dict[str(list(vertices[i]))] = i

# new_lines = []
# for line in lines:
#     new_lines.append([vertices_dict[str(line[0])], vertices_dict[str(line[1])]])

# print(new_lines)
        self._temp_lines = [
            [[-34, 0, 89], [34, 0, 89]],
            [[-34, 0, -89], [34, 0, -89]],
            [[89, -34, 0], [55, -55, 55]],
            [[89, -34, 0], [89, 34, 0]],
            [[89, -34, 0], [55, -55, -55]],
            [[89, 34, 0], [55, 55, 55]],
            [[89, 34, 0], [55, 55, -55]],
            [[55, -55, -55], [34, 0, -89]],
            [[55, 55, -55], [34, 0, -89]],
            [[55, -55, 55], [34, 0, 89]],
            [[55, 55, 55], [34, 0, 89]],
            [[-89, -34, 0], [-55, -55, 55]],
            [[-89, -34, 0], [-89, 34, 0]],
            [[-89, -34, 0], [-55, -55, -55]],
            [[-89, 34, 0], [-55, 55, 55]],
            [[-89, 34, 0], [-55, 55, -55]],
            [[-55, -55, -55], [-34, 0, -89]],
            [[-55, 55, -55], [-34, 0, -89]],
            [[-55, -55, 55], [-34, 0, 89]],
            [[-55, 55, 55], [-34, 0, 89]],
            [[0, 89, 34], [-55, 55, 55]],
            [[0, 89, 34], [55, 55, 55]],
            [[0, 89, 34], [0, 89, -34]],
            [[0, 89, -34], [-55, 55, -55]],
            [[0, 89, -34], [55, 55, -55]],
            [[0, -89, 34], [-55, -55, 55]],
            [[0, -89, 34], [55, -55, 55]],
            [[0, -89, 34], [0, -89, -34]],
            [[0, -89, -34], [-55, -55, -55]],
            [[0, -89, -34], [55, -55, -55]],
        ]
        self.vertices = [
            Point3D(-55, -55, 55),
            Point3D(0, -89, -34),
            Point3D(-55, -55, -55),
            Point3D(-89, -34, 0),
            Point3D(-34, 0, -89),
            Point3D(-55, 55, 55),
            Point3D(0, 89, -34),
            Point3D(34, 0, -89),
            Point3D(-55, 55, -55),
            Point3D(0, -89, 34),
            Point3D(-89, 34, 0),
            Point3D(-34, 0, 89),
            Point3D(89, 34, 0),
            Point3D(89, -34, 0),
            Point3D(55, 55, 55),
            Point3D(55, -55, 55),
            Point3D(34, 0, 89),
            Point3D(55, -55, -55),
            Point3D(55, 55, -55),
            Point3D(0, 89, 34)
        ]

        self.lines = [[11, 16], [4, 7], [13, 15], [13, 12], [13, 17], [12, 14], [12, 18], [17, 7], [18, 7], [15, 16], [14, 16], [3, 0], [3, 10], [3, 2], [
            10, 5], [10, 8], [2, 4], [8, 4], [0, 11], [5, 11], [19, 5], [19, 14], [19, 6], [6, 8], [6, 18], [9, 0], [9, 15], [9, 1], [1, 2], [1, 17]]


class Icosahedron(Entity):
    def __init__(self, pos=None) -> None:
        Entity.__init__(self, pos)

        self._temp_lines = [
            [[1, -1.618033988749895, 0], [0, -1, 1.618033988749895]],
            [[1, -1.618033988749895, 0], [-1, -1.618033988749895, 0]],
            [[-1, -1.618033988749895, 0], [0, -1, 1.618033988749895]],
            [[1, -1.618033988749895, 0], [1.618033988749895, 0, 1]],
            [[1.618033988749895, 0, 1], [0, -1, 1.618033988749895]],
            [[0, -1, 1.618033988749895], [-1.618033988749895, 0, 1]],
            [[-1.618033988749895, 0, 1], [-1, -1.618033988749895, 0]],
            [[-1, -1.618033988749895, 0], [-1.618033988749895, 0, -1]],
            [[-1.618033988749895, 0, -1], [-1.618033988749895, 0, 1]],
            [[0, -1, 1.618033988749895], [0, 1, 1.618033988749895]],
            [[0, 1, 1.618033988749895], [1.618033988749895, 0, 1]],
            [[0, 1, 1.618033988749895], [-1.618033988749895, 0, 1]],
            [[-1, 1.618033988749895, 0], [-1.618033988749895, 0, 1]],
            [[-1, 1.618033988749895, 0], [0, 1, 1.618033988749895]],
            [[-1, 1.618033988749895, 0], [-1.618033988749895, 0, -1]],
            [[1, 1.618033988749895, 0], [-1, 1.618033988749895, 0]],
            [[1, 1.618033988749895, 0], [0, 1, 1.618033988749895]],
            [[1, 1.618033988749895, 0], [1.618033988749895, 0, 1]],
            [[1, -1.618033988749895, 0], [0, -1, -1.61803398874989]],
            [[0, -1, -1.61803398874989], [-1, -1.618033988749895, 0]],
            [[0, -1, -1.61803398874989], [-1.618033988749895, 0, -1]],
            [[0, -1, -1.61803398874989], [0, 1, -1.618033988749895]],
            [[0, 1, -1.618033988749895], [-1.618033988749895, 0, -1]],
            [[0, 1, -1.618033988749895], [-1, 1.618033988749895, 0]],
            [[0, 1, -1.618033988749895], [1, 1.618033988749895, 0]],
            [[1, 1.618033988749895, 0], [1.618033988749895, 0, -1]],
            [[1.618033988749895, 0, -1], [0, 1, -1.618033988749895]],
            [[1.618033988749895, 0, -1], [1.618033988749895, 0, 1]],
            [[1.618033988749895, 0, -1], [1, -1.618033988749895, 0]],
            [[1.618033988749895, 0, -1], [0, -1, -1.61803398874989]]
        ]
        self.vertices = [Point3D(-1, PHI, 0), Point3D(1, PHI, 0), Point3D(-1, -PHI, 0), Point3D(1, -PHI, 0), Point3D(0, -1, PHI),
                         Point3D(0, 1, PHI), Point3D(0, -1, -PHI), Point3D(0, 1, -PHI), Point3D(PHI, 0, -1), Point3D(PHI, 0, 1), Point3D(-PHI, 0, -1), Point3D(-PHI, 0, 1)]
        self.lines = [[3, 4], [3, 2], [2, 4], [3, 9], [9, 4], [4, 11], [11, 2], [2, 10], [10, 11], [4, 5], [5, 9], [5, 11], [0, 11], [0, 5], [
            0, 10], [1, 0], [1, 5], [1, 9], [3, 6], [6, 2], [6, 10], [6, 7], [7, 10], [7, 0], [7, 1], [1, 8], [8, 7], [8, 9], [8, 3], [8, 6]]


angle = 0.01
frame_rate = 30
objects_pos = [Cube([400, 300])]


# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((1280, 720))  # Window size: 800x600
pygame.display.set_caption('Draw a Line with Pygame')  # Window title

# Define colors
white = (255, 255, 255)

change_direction_btn = Button([120, 40], "Change Direction", [50, 50])
velocity_plus_btn = Button([80, 40], "Velocity ++", [200, 50])
velocity_minus_btn = Button([80, 40], "Velocity --", [310, 50])
delete_cube_btn = Button([100, 40], "Delete objects", [410, 50])

add_cube_btn = Button([80, 40], "Add cube", [50, 120])
add_tetrahedron_btn = Button([120, 40], "Add Tetrahedron", [50, 180])
add_octahedron_btn = Button([120, 40], "Add Octahedron", [50, 240])
add_dodecahedron_btn = Button([120, 40], "Add Dodecahedron", [50, 300])
add_icosahedron_btn = Button([120, 40], "Add Icosahedron", [50, 360])

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
            angle += 0.01
        else:
            angle -= 0.01

    velocity_minus_btn.render(screen)
    if velocity_minus_btn.clicked(events):
        if angle > 0:
            angle = round(angle - 0.01, 2)
        elif angle == 0:
            pass
        else:
            angle = round(angle + 0.01, 2)

    delete_cube_btn.render(screen)
    if delete_cube_btn.clicked(events):
        if len(objects_pos) > 1:
            objects_pos.pop()

    add_cube_btn.render(screen)
    if add_cube_btn.clicked(events):
        objects_pos.append(Cube())

    add_tetrahedron_btn.render(screen)
    if add_tetrahedron_btn.clicked(events):
        objects_pos.append(Tetrahedron())

    add_octahedron_btn.render(screen)
    if add_octahedron_btn.clicked(events):
        objects_pos.append(Octahedron())

    add_dodecahedron_btn.render(screen)
    if add_dodecahedron_btn.clicked(events):
        objects_pos.append(Dodecahedron())
    
    add_icosahedron_btn.render(screen)
    if add_icosahedron_btn.clicked(events):
        objects_pos.append(Icosahedron())

    for obj in objects_pos:
        obj.draw(pygame, angle)

    # Set max frame rate
    try:
        time.sleep((1/frame_rate) - (time.time() - st_time))
    except Exception:
        pass

    pygame.display.flip()


# Quit Pygame
pygame.quit()
sys.exit()
