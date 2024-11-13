# main.py

from modelo import Modelo
from utilidades import *
from usuario import *
from camara import Camara
from configuracion import *
from luces import configurar_luces
# Importa cargar_textura para gestionar texturas
from texturas import cargar_textura

# Inicialización de la cámara y el modelo 3D
camara = Camara()

# Inicialización de la escena


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


# Configuración e inicialización del entorno
screen = inicializar_escena()  # Crea la ventana y configura el contexto OpenGL

# Modelos
cubo = Modelo("modelos/cubo.obj")  # Cubo
cilindro = Modelo("modelos/cilindro.obj")
# Texturas
textura_cubo = cargar_textura("texturas/marron.png")  # Textura marrón
textura_cilindro = cargar_textura("texturas/gris.png")

textura_azul = cargar_textura("texturas/azul.png")
textura_rojo = cargar_textura("texturas/rojo.png")
textura_verde = cargar_textura("texturas/verde.png")
textura_amarillo = cargar_textura("texturas/amarillo.png")
textura_naranja = cargar_textura("texturas/naranja.png")
clock = pygame.time.Clock()
ejecutando = True

# Renderiza la escena


def renderizar():
    """Renderiza los elementos de la escena, incluyendo la cámara, elementos auxiliares y el modelo 3D."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glRotatef(camara.roll, 0, 0, 1)
    cam_x, cam_y, cam_z = camara.obtener_posicion()
    gluLookAt(cam_x, cam_y, cam_z, 0, 0, 0, 0, 1, 0)

    glDisable(GL_LIGHTING)
    dibujar_elementos_auxiliares(ejes=True, rejilla=True)
    glEnable(GL_LIGHTING)

    # Dibuja el cubo
    # Dibuja la base (6.0x2.0x0.2)
    cubo.dibujar(textura_id=textura_cubo, t_x=0.0, t_y=0.1, t_z=0.0,  # t_y=0.1 para ponerlo sobre la rejilla
                 angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                 sx=6.0, sy=0.2, sz=2.0)  # Dimensiones según especificaciones

    # Dibuja los tres postes
    # Poste izquierdo
    cilindro.dibujar(textura_id=textura_cilindro, t_x=-2.0, t_y=1.1, t_z=0.0,
                     angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                     sx=0.2, sy=2.0, sz=0.2)

    # Poste central
    cilindro.dibujar(textura_id=textura_cilindro, t_x=0.0, t_y=1.1, t_z=0.0,
                     angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                     sx=0.2, sy=2.0, sz=0.2)

    # Poste derecho
    cilindro.dibujar(textura_id=textura_cilindro, t_x=2.0, t_y=1.1, t_z=0.0,
                     angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                     sx=0.2, sy=2.0, sz=0.2)

    # Discos poste izquierdo (usando cilindro)

    cilindro.dibujar(textura_id=textura_azul, t_x=-2.0, t_y=0.3, t_z=0.0,
                     angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                     sx=2.0, sy=0.2, sz=2.0)
    cilindro.dibujar(textura_id=textura_verde, t_x=-2.0, t_y=0.5, t_z=0.0,
                     angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                     sx=1.7, sy=0.2, sz=1.7)
    cilindro.dibujar(textura_id=textura_amarillo, t_x=-2.0, t_y=0.7, t_z=0.0,
                     angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                     sx=1.4, sy=0.2, sz=1.4)
    cilindro.dibujar(textura_id=textura_naranja, t_x=-2.0, t_y=0.9, t_z=0.0,
                     angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                     sx=1.1, sy=0.2, sz=1.1)
    cilindro.dibujar(textura_id=textura_rojo, t_x=-2.0, t_y=1.1, t_z=0.0,
                     angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                     sx=0.8, sy=0.2, sz=0.8)


    # Discos sobre
# Bucle principal de la aplicación
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
