import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import pymunk
from pymunk.vec2d import Vec2d

# Window Settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FOV = 45
SCREEN_ASPECT_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT
NEAR_PLANE = 0.1
FAR_PLANE = 100.0
FPS = 60
MILLISECONDS_PER_SECOND = 1000

# Cradle Settings
NUMBER_OF_PENDULUMS = 5
PENDULUM_RADIUS = 0.45
PENDULUM_LENGTH = 2.0
PENDULUM_MASS = 10
INITIAL_IMPULSE = -12000
GRAVITY = 9820
DAMPING = 0.999


class Camara:
    def __init__(self):
        self.distance = 10.0
        self.rot_x = 30
        self.rot_y = 0
        self.rot_z = 0
        self.pos_x = 0
        self.pos_y = 0
        self.pos_z = self.distance

    def actualizar_camara(self):
        self.pos_x = self.distance * math.sin(math.radians(self.rot_y))
        self.pos_z = self.distance * math.cos(math.radians(self.rot_y))

    def obtener_posicion(self):
        return (self.pos_x, self.pos_y, self.pos_z)


class Pendulum:
    def __init__(self, pos_x, space, is_moving=False):
        self.mass = PENDULUM_MASS
        self.radius = PENDULUM_RADIUS
        self.moment = pymunk.moment_for_circle(self.mass, 0, self.radius)

        # Physical body
        self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = pos_x, 2.0
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.9999

        # Anchor point (now in 3D)
        self.anchor_pos = (pos_x, 3.5, 0.0)

        # Add to space
        space.add(self.body, self.shape)
        # Convert 3D anchor position back to 2D for pymunk
        joint = pymunk.PinJoint(
            space.static_body, self.body, (self.anchor_pos[0], self.anchor_pos[1]), (0, 0))
        space.add(joint)

        if is_moving:
            self.body.apply_impulse_at_local_point((INITIAL_IMPULSE, 0))

    def get_position(self):
        """Returns the position as a 3D tuple"""
        return (self.body.position.x, self.body.position.y, 0.0)


def init_scene():
    pygame.init()
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Newton's Cradle")

    glClearColor(0.9, 0.9, 0.9, 1)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (5, 5, 5, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1))

    glMatrixMode(GL_PROJECTION)
    gluPerspective(FOV, SCREEN_ASPECT_RATIO, NEAR_PLANE, FAR_PLANE)
    glMatrixMode(GL_MODELVIEW)

    return screen


def draw_sphere(position, radius):
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    quad = gluNewQuadric()
    glColor3f(0.7, 0.7, 0.7)
    gluSphere(quad, radius, 32, 32)
    glPopMatrix()


def draw_cylinder(start, end, radius):
    """Draw a cylinder from start to end point
    start: (x, y, z) tuple
    end: (x, y, z) tuple
    radius: float
    """
    glPushMatrix()

    # Calculate the direction vector
    direction = (end[0] - start[0], end[1] - start[1], end[2] - start[2])
    length = math.sqrt(sum(x*x for x in direction))

    # Calculate rotation angle and axis
    if length > 0:
        dx, dy, dz = (x/length for x in direction)
        angle = math.acos(dy) * 180/math.pi
        # Avoid division by zero when calculating rotation axis
        if abs(dx) < 1e-6 and abs(dz) < 1e-6:
            # Default axis if the cylinder is perfectly vertical
            axis = (1, 0, 0)
        else:
            axis = (-dz, 0, dx)
    else:
        angle = 0
        axis = (1, 0, 0)

    # Position and rotate
    glTranslatef(start[0], start[1], start[2])
    if angle != 0:  # Only rotate if needed
        glRotatef(angle, axis[0], axis[1], axis[2])

    # Draw cylinder
    quad = gluNewQuadric()
    glColor3f(0.4, 0.4, 0.4)
    gluCylinder(quad, radius, radius, length, 32, 1)
    gluDeleteQuadric(quad)

    glPopMatrix()


def main():
    screen = init_scene()
    clock = pygame.time.Clock()
    camera = Camara()

    # Physics setup
    space = pymunk.Space()
    space.gravity = (0, -GRAVITY)
    space.damping = DAMPING

    # Create pendulums
    pendulums = []
    start_x = -(NUMBER_OF_PENDULUMS - 1) * PENDULUM_RADIUS
    for i in range(NUMBER_OF_PENDULUMS):
        is_moving = (i == 0)  # First pendulum starts with movement
        pendulums.append(
            Pendulum(start_x + i * PENDULUM_RADIUS * 2, space, is_moving))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    camera.rot_y -= 5
                elif event.key == pygame.K_RIGHT:
                    camera.rot_y += 5
                elif event.key == pygame.K_UP:
                    camera.distance = max(5, camera.distance - 0.5)
                elif event.key == pygame.K_DOWN:
                    camera.distance = min(20, camera.distance + 0.5)

        # Update physics
        space.step(1/FPS)

        # Update camera
        camera.actualizar_camara()

        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Position camera
        cam_pos = camera.obtener_posicion()
        gluLookAt(cam_pos[0], cam_pos[1], cam_pos[2], 0, 0, 0, 0, 1, 0)

        # Draw support bar
        glColor3f(0.4, 0.4, 0.4)
        bar_length = (NUMBER_OF_PENDULUMS + 1) * PENDULUM_RADIUS
        draw_cylinder((-bar_length, 3.5, 0), (bar_length, 3.5, 0), 0.1)

        # Draw pendulums
        for pendulum in pendulums:
            pos = pendulum.get_position()
            # Draw string
            draw_cylinder(pendulum.anchor_pos, pos, 0.02)
            # Draw ball
            draw_sphere(pos, pendulum.radius)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
