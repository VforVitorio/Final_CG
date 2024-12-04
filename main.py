# main.py

from modelo import Modelo
from utilidades import *
from usuario import *
from camara import Camara
from configuracion import *
from luces import configurar_luces
# Importa cargar_textura para gestionar texturas
from texturas import cargar_textura
import math
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

# Carga de los modelos haciendo instancias de la Clase Modelo, junto al archivo obj a cargar
cubo = Modelo("modelos/cubo.obj")
cilindro = Modelo("modelos/cilindro.obj")
donut = Modelo("modelos/donut.obj")
esfera = Modelo("modelos/esfera.obj")
cuarto_esfera = Modelo("modelos/cuarto_esfera.obj")


# Carga de texturas para cada uno de los objetos
textura_cubo = cargar_textura("texturas/madera.png")  # Textura marrón
textura_cilindro = cargar_textura("texturas/metal.png")
textura_donut = cargar_textura("texturas/metal_2.png")
textura_esfera = cargar_textura("texturas/metal_esfera.png")
textura_hilo = cargar_textura("texturas/hilo_metalico.png")


# Definición del reloj e inicio de la variable ejecutando en true
clock = pygame.time.Clock()
ejecutando = True

# Funciones de renderización de la escena


def dibujo_base():
    """
    Funcion que renderiza la base del pendulo.

    Instancia del modelo cubo, aplanándolo y poniéndolo justo encima de la rejilla
    """
    cubo.dibujar(textura_id=textura_cubo, t_x=0.0, t_y=0.2, t_z=0.0,  # t_y=0.1 para ponerlo sobre la rejilla
                 angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                 sx=10.0, sy=0.4, sz=4.0)


def dibujo_estructura():
    """
    Diseño de la estructura de donde colgarán y sostienen las bolas e hilos del pendulo.

    Instancia de 6 cilindros:
        - 4 verticales: soporte del péndulo.
        - 2 horizontales: unión de los soportes, de donde irán sujetadas las bolas del péndulo.
    """
    # Cilindro esquina frontal derecha
    cilindro.dibujar(textura_id=textura_cilindro, t_x=4.5, t_y=1.8, t_z=1.5,
                     angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                     sx=0.25, sy=3.5, sz=0.25)
    # Cilindro esquina frontal izquierda
    cilindro.dibujar(textura_id=textura_cilindro, t_x=-4.5, t_y=1.8, t_z=1.5,
                     angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                     sx=0.25, sy=3.5, sz=0.25)
    # Cilindro esquina trasera derecha
    cilindro.dibujar(textura_id=textura_cilindro, t_x=4.5, t_y=1.8, t_z=-1.5,
                     angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                     sx=0.25, sy=3.5, sz=0.25)
    # Cilindro esquina trasera izquierda
    cilindro.dibujar(textura_id=textura_cilindro, t_x=-4.5, t_y=1.8, t_z=-1.5,
                     angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                     sx=0.25, sy=3.5, sz=0.25)

    # Cilindros horizontales que unen cilindros traseros y delanteros respectivamente

    # Cilindro horizontal frontal (conecta los cilindros frontales)
    cilindro.dibujar(textura_id=textura_cilindro, t_x=0.0, t_y=3.5, t_z=1.5,
                     angulo=90.0, eje_x=0.0, eje_y=0.0, eje_z=1.0,
                     sx=0.25, sy=9.0, sz=0.25)  # sy=9.0 para cubrir la distancia entre -4.5 y 4.5

    # Cilindro horizontal trasero (conecta los cilindros traseros)
    cilindro.dibujar(textura_id=textura_cilindro, t_x=0.0, t_y=3.5, t_z=-1.5,
                     angulo=90.0, eje_x=0.0, eje_y=0.0, eje_z=1.0,
                     sx=0.25, sy=9.0, sz=0.25)


def dibujo_esquinas():
    """
    Renderizacion de las esquinas curvas del modelo, a partir de semiesferas.

    Dispuestas en la intersección de los cilindros traseros y delanteros verticales 
    con su respectivo cilindro horizontal.

    Ayuda a dar una forma curva a las esquinas.

    """
    cuarto_esfera.dibujar(textura_id=textura_cilindro, t_x=4.49, t_y=3.48, t_z=1.5,
                          angulo=-90.0, eje_x=1.0, eje_y=0.0, eje_z=0.0,
                          sx=0.3, sy=0.3, sz=0.3)

    # Delantero izquierdo (tumbado y mirando hacia fuera)
    cuarto_esfera.dibujar(textura_id=textura_cilindro, t_x=-4.49, t_y=3.48, t_z=1.5,
                          angulo=180.0, eje_x=0.0, eje_y=1.0, eje_z=1.0,  # Primero girar en Y
                          sx=0.3, sy=0.3, sz=0.3)

    # Trasero derecho (se mantiene igual)
    cuarto_esfera.dibujar(textura_id=textura_cilindro, t_x=4.49, t_y=3.48, t_z=-1.5,
                          angulo=-90.0, eje_x=1.0, eje_y=0.0, eje_z=0.0,
                          sx=0.3, sy=0.3, sz=0.3)

    # Trasero izquierdo (tumbado y mirando hacia fuera)
    cuarto_esfera.dibujar(textura_id=textura_cilindro, t_x=-4.49, t_y=3.48, t_z=-1.5,
                          angulo=180.0, eje_x=0.0, eje_y=1.0, eje_z=1.0,  # Primero girar en Y
                          sx=0.3, sy=0.3, sz=0.3)


def dibujar_hilo(modelo, t_x, t_y, t_z, punto_destino, es_trasero=False):
    """Dibuja un hilo desde un punto origen a un punto destino

    Usado para dibujar los hilos que sujetan las bolas del péndulo.

    Punto inicial: cada una de las anillas dispuestas en los cilindros horizontales.
    Punto final: pequeña semiesfera soporte de las bolas del péndulo.


    Args:
        modelo (Modelo): Instancia del modelo del hilo.
        t_x (float): Posición en el eje X del punto de origen.
        t_y (float): Posición en el eje Y del punto de origen.
        t_z (float): Posición en el eje Z del punto de origen.
        punto_destino (tuple): Coordenadas (x, y, z) del punto destino.
        es_trasero (bool): Indica si el hilo cuelga del cilindro trasero.

    Componentes:
        - Cálculo de la longitud del hilo.
        - Colocación del hilo en los puntos iniciales y finales.
        - Definición del ángulo de inclinación de los hilos, a partir de si cuelgan del cilindro trasero o no
        - Dibujo de los hilos con método de la instancia modelo.


    """
    # Calculamos la longitud
    dx = punto_destino[0] - t_x
    dy = punto_destino[1] - (t_y - 0.2)
    dz = punto_destino[2] - t_z
    longitud = math.sqrt(dx*dx + dy*dy + dz*dz) * 2.5

    # Ajustamos el punto medio para que el extremo coincida con el donut
    medio_x = t_x + dx/4  # Desplazamos 1/4 de la distancia en X
    medio_y = (t_y - 0.2) + dy/2  # Desplazamos 1/2 de la distancia en Y
    medio_z = t_z + dz/2  # Desplazamos 1/2 de la distancia en Z

    # Ángulo de inclinación
    angulo = 40.0 if not es_trasero else -40.0

    modelo.dibujar(
        # Definicion de la textura
        textura_id=textura_hilo,
        # Definicion de las posiciones del hilo
        t_x=medio_x,
        t_y=medio_y,
        t_z=medio_z,
        # Angulos de rotacion
        angulo=angulo,
        eje_x=1.0, eje_y=0.0, eje_z=0.0,
        # Dimensiones del objeto a partir del escalado
        sx=0.01,
        sy=longitud/2,  # Mantenemos la mitad de la longitud
        sz=0.01
    )


def dibujar_esfera_union(esfera, x, y, z, es_trasero=False):
    """
    Dibuja una media esfera en el extremo de los hilos.

    Son las semiesferas de las que cuelgan las bolas del pendulo

    Creacion de instancia de objeto esfera:
        - Aplicacion de la misma textura que las anillas
        - Transformaciones necesarias para disponerlas a la altura de la intersección de los hilos.
        - Rotacion de la esfera para que se disponga horizontalmente.
        - Transformaciones de dimensiones para que sea pequeña.

    Args:
        esfera (Modelo): Instancia del modelo de la esfera.
        x (float): Posición en el eje X.
        y (float): Posición en el eje Y.
        z (float): Posición en el eje Z.
        es_trasero (bool): Indica si la esfera está en la parte trasera.





    """
    esfera.dibujar(
        # Se aplica la textura de las anillas
        textura_id=textura_donut,
        # Se ajusta la posicion en el eje y
        t_x=x,
        t_y=y - 0.3,  # Ajustamos altura para que coincida con los hilos
        t_z=z,
        angulo=180.0,  # Rotación para que la parte plana mire hacia arriba
        eje_x=1.0,
        eje_y=0.0,
        eje_z=0.0,
        sx=0.08,      # Ancho de la media esfera
        # Altura de la media esfera (más pequeña para que parezca partida)
        sy=0.04,
        sz=0.08       # Profundidad igual al ancho para mantener proporción
    )


def dibujar_bola_pendulo(esfera, x, y, z, es_trasero=False):
    """
    Dibuja una bola grande del péndulo de Newton.

    Instancia del modelo esfera.
    Se baja la altura para que se disponga justo debajo de la semiesfera de union.
    Sin rotacion, puesto que es una esfera completa.
    Escalado de 1, para que sea una esfera de dimensiones grandes.

     Args:
        esfera (Modelo): Instancia del modelo de la esfera.
        x (float): Posición en el eje X.
        y (float): Posición en el eje Y.
        z (float): Posición en el eje Z.
        es_trasero (bool): Indica si la bola está en la parte trasera.

    """
    esfera.dibujar(
        textura_id=textura_esfera,
        t_x=x,
        t_y=y - 0.8,  # Bajamos respecto a la posición de la esfera_union
        t_z=z,
        angulo=0.0,   # Sin rotación, es una esfera completa
        eje_x=1.0,
        eje_y=0.0,
        eje_z=0.0,
        sx=1.0,      # Escala grande para la bola
        sy=1.0,      # Mantener proporciones esféricas
        sz=1.0      # Mantener proporciones esféricas
    )


def dibujar_pendulos_frontales(posiciones_x, donut, cilindro, esfera):
    """

    Dibuja los péndulos de la parte frontal
    Se usan las funciones de dibujo de hilos, esferas de union y bolas del pendulo.

    A traves de la definicon de posiciones en el eje x, se ejecuta bucle 
    que renderiza las anillas de las que salen los hilos, semiesferas de union y bolas del pendulo.



    Args:
        posiciones_x (list): Lista de posiciones en el eje X para los péndulos.
        donut (Modelo): Instancia del modelo del donut.
        cilindro (Modelo): Instancia del modelo del cilindro.
        esfera (Modelo): Instancia del modelo de la esfera.

    """
    for x in posiciones_x:
        # Donuts frontales
        donut.dibujar(textura_id=textura_donut,
                      t_x=x, t_y=3.5, t_z=1.5,
                      angulo=90.0, eje_x=0.0, eje_y=0.0, eje_z=1.0,
                      sx=0.22, sy=0.22, sz=0.12)
        # El resto se mantiene igual usando las nuevas posiciones
        dibujar_hilo(cilindro, x, 3.5, 1.5, (x, 2.0, 0.0), es_trasero=False)
        dibujar_esfera_union(cilindro, x, 2.0, 0.0, es_trasero=False)
        dibujar_bola_pendulo(esfera, x, 2.0, 0.0, es_trasero=False)


def dibujar_pendulos_traseros(posiciones_x, donut, cilindro, esfera):
    """

    Dibuja los péndulos de la parte trasera.

    Misma funcion que pendulos delanteros, pero cambiando valores de ángulos por sus negativos 
    y estableciendo el booleano es_trasero por True.

     Args:
        posiciones_x (list): Lista de posiciones en el eje X para los péndulos.
        donut (Modelo): Instancia del modelo del donut.
        cilindro (Modelo): Instancia del modelo del cilindro.
        esfera (Modelo): Instancia del modelo de la esfera.

    """
    for x in posiciones_x:
        donut.dibujar(textura_id=textura_donut,
                      t_x=x, t_y=3.5, t_z=-1.5,
                      angulo=-90.0, eje_x=0.0, eje_y=0.0, eje_z=1.0,
                      sx=0.22, sy=0.22, sz=0.12)
        dibujar_hilo(cilindro, x, 3.5, -1.5, (x, 2.0, 0.0), es_trasero=True)
        dibujar_esfera_union(cilindro, x, 2.0, 0.0, es_trasero=True)
        dibujar_bola_pendulo(esfera, x, 2.0, 0.0, es_trasero=True)


def renderizar():
    """
    Renderiza los elementos de la escena, incluyendo la cámara, elementos auxiliares y el modelo 3D.

    Funcion principal encargada de renderizar todos los elementos de la escena.
        - Dibujo de la base.
        - Dibujo de la estructura.
        - Dibujo de los péndulos delanteros y traseros.

    """
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
    dibujo_base()

    # Dibuja los 4 cilindros en las esquinas
    # Cilindros ajustados en altura y centrados en las rejillas
    dibujo_estructura()

    # Se añaden esferas pequeñas en los puntos de union
    # Se colocan en las 8 intersecciones (4 frontales y 4 traseras)
    # Cuartos de esfera en las intersecciones de los cilindros horizontales
    dibujo_esquinas()

    # ===========
    # Dibujo de las anillas
    # ===========
    # 5 donuts en el cilindro frontal
    # 5 donuts en el cilindro frontal
    # Ajustamos las posiciones para que estén más juntas
    # Posiciones más cercanas entre sí
    # Ajustamos las posiciones para separar un poco más las bolas
    posiciones_x = [-2, -1, 0.0, 1, 2]
    dibujar_pendulos_frontales(posiciones_x, donut, cilindro, esfera)
    dibujar_pendulos_traseros(posiciones_x, donut, cilindro, esfera)


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
