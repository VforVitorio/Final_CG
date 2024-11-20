# main.py
from modelo import Modelo
from utilidades import *
from usuario import *
from camara import Camara
from configuracion import *
from luces import configurar_luces
from texturas import cargar_textura
import math
import numpy as np
import pymunk
from pymunk.vec2d import Vec2d

G = 9820            # Gravedad ajustada como en el ejemplo
L = 2.0
INITIAL_IMPULSE = -12000  # Impulso inicial


class Pendulo:
    def __init__(self, pos_x, is_moving=False):
        # Configuración física
        self.mass = 10
        self.radius = 0.45  # Radio de la bola
        self.moment = pymunk.moment_for_circle(self.mass, 0, self.radius)

        # Crear cuerpo físico
        self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = pos_x, 2.0  # Posición inicial
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = 0.9999  # Alta elasticidad para conservar energía

        # Punto de anclaje
        self.anchor_pos = (pos_x, 3.5)

        # Aplicar impulso inicial si es necesario
        if is_moving:
            self.body.apply_impulse_at_local_point((INITIAL_IMPULSE, 0))

    def get_position(self):
        return (self.body.position.x, self.body.position.y, 0)


def inicializar_escena():
    """Inicializa la ventana gráfica con Pygame y configura los ajustes de OpenGL para la escena 3D.

    Returns:
        screen: Objeto de la ventana gráfica creada por Pygame.
    """
    pygame.init()
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('VEGA SOBRAL VICTOR')

    # Configuración de OpenGL
    glClearColor(0, 0, 0, 1)  # Fondo negro
    glEnable(GL_DEPTH_TEST)  # Activa el z-buffer para la profundidad
    glShadeModel(GL_SMOOTH)  # Activa el sombreado suave
    glMatrixMode(GL_PROJECTION)  # Selecciona la matriz de proyección
    # Configura la proyección en perspectiva
    gluPerspective(FOV, SCREEN_ASPECT_RATIO, NEAR_PLANE, FAR_PLANE)
    glMatrixMode(GL_MODELVIEW)  # Selecciona la matriz de modelo-vista
    glLoadIdentity()  # Restablece la matriz a la identidad
    # Inicializa la iluminación
    configurar_luces()
    # Activa la luz 1 (GL_LIGHT0)
    glEnable(GL_LIGHT0)
    # Activa la luz 2
    glEnable(GL_LIGHT1)

    # Activa la iluminación en general
    glEnable(GL_LIGHTING)
    return screen


# Inicialización
camara = Camara()
screen = inicializar_escena()

# Modelos y texturas
esfera = Modelo("modelos/esfera.obj")
cilindro = Modelo("modelos/cilindro.obj")

textura_esfera = cargar_textura("texturas/gris.png")
textura_hilo = cargar_textura("texturas/gris.png")

clock = pygame.time.Clock()
ejecutando = True

# Inicialización del espacio físico
space = pymunk.Space()
space.gravity = (0, -G)
space.damping = 0.999  # Amortiguación mínima


tiempo = 0.0
# Modificar la creación de péndulos
pendulos = [
    Pendulo(-0.5, False),
    Pendulo(0.5, True)
]

# Agregar péndulos al espacio
for p in pendulos:
    space.add(p.body, p.shape)
    # Crear articulación fija en el punto de anclaje
    joint = pymunk.PinJoint(space.static_body, p.body, p.anchor_pos, (0, 0))
    space.add(joint)


def renderizar():
    global tiempo

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glRotatef(camara.roll, 0, 0, 1)
    cam_x, cam_y, cam_z = camara.obtener_posicion()
    gluLookAt(cam_x, cam_y, cam_z, 0, 0, 0, 0, 1, 0)

    glDisable(GL_LIGHTING)
    dibujar_elementos_auxiliares(ejes=True, rejilla=True)
    glEnable(GL_LIGHTING)

    # Actualizar física
    space.step(delta_time)

    # Dibujar péndulos
    for pendulo in pendulos:
        pos = pendulo.get_position()
        dibujar_hilo(
            cilindro, pendulo.anchor_pos[0], pendulo.anchor_pos[1], 0, pos)
        dibujar_bola_pendulo(esfera, pos[0], pos[1], pos[2])

    tiempo += delta_time


def dibujar_hilo(modelo, t_x, t_y, t_z, punto_destino):
    dx = punto_destino[0] - t_x
    dy = punto_destino[1] - t_y
    dz = punto_destino[2] - t_z
    longitud = math.sqrt(dx*dx + dy*dy + dz*dz)

    # Calcular ángulo de rotación para el hilo
    angulo = math.atan2(dx, -dy) * 180.0 / math.pi

    modelo.dibujar(
        textura_id=textura_hilo,
        t_x=t_x + dx/2,  # Punto medio en X
        t_y=t_y + dy/2,  # Punto medio en Y
        t_z=t_z,
        angulo=angulo,   # Aplicar rotación
        eje_x=0.0,
        eje_y=0.0,
        eje_z=1.0,       # Rotar alrededor del eje Z
        sx=0.01,
        sy=longitud,
        sz=0.01
    )


def dibujar_bola_pendulo(modelo, x, y, z):
    esfera.dibujar(
        textura_id=textura_esfera,
        t_x=x,
        t_y=y,
        t_z=z,
        angulo=0.0,
        eje_x=1.0, eje_y=0.0, eje_z=0.0,
        sx=0.8,
        sy=0.8,
        sz=0.8
    )


while ejecutando:
    delta_time = clock.tick(FPS) / MILLISECONDS_PER_SECOND
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.MOUSEWHEEL):
            procesar_eventos_raton(evento, camara)

    consultar_estado_teclado(camara, delta_time)
    camara.actualizar_camara()
    configurar_luces()
    renderizar()
    pygame.display.flip()

pygame.quit()
