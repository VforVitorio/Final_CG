import numpy as np

def generar_toro(R=1.0, r=0.3, N=16, M=8, filename='donut.obj'):
    """
    Genera un toro (donut) con coordenadas de textura y normales, y lo guarda en un archivo OBJ.

    Parámetros:
    - R: Radio mayor (distancia desde el centro del toro hasta el centro del tubo).
    - r: Radio menor (radio del tubo).
    - N: Número de segmentos en el anillo mayor.
    - M: Número de segmentos en el anillo menor.
    - filename: Nombre del archivo OBJ de salida.

    Retorna:
    - None
    """
    # Crea ángulos para las divisiones
    theta = np.linspace(0, 2 * np.pi, N + 1)
    phi = np.linspace(0, 2 * np.pi, M + 1)
    theta, phi = np.meshgrid(theta, phi)
    theta = theta.flatten()
    phi = phi.flatten()

    # Calcula las coordenadas de los vértices
    x = (R + r * np.cos(phi)) * np.cos(theta)
    z = (R + r * np.cos(phi)) * np.sin(theta)
    y = r * np.sin(phi)

    vertices = np.column_stack((x, y, z))

    # Calcula las normales
    nx = np.cos(phi) * np.cos(theta)
    nz = np.cos(phi) * np.sin(theta)
    ny = np.sin(phi)

    normales = np.column_stack((nx, ny, nz))

    # Calcularlas coordenadas de textura (u, v)
    u = theta / (2 * np.pi)
    v = phi / (2 * np.pi)
    uvs = np.column_stack((u, v))

    # Genera las caras
    faces = []
    for i in range(M):
        for j in range(N):
            i1 = i * (N + 1) + j
            i2 = (i + 1) * (N + 1) + j
            i3 = (i + 1) * (N + 1) + (j + 1)
            i4 = i * (N + 1) + (j + 1)

            # Cada cuadrilátero se divide en dos triángulos
            faces.append([i1 + 1, i2 + 1, i3 + 1])  # Triángulo 1
            faces.append([i1 + 1, i3 + 1, i4 + 1])  # Triángulo 2

    # Escribe el archivo OBJ
    with open(filename, 'w') as f:
        # Escribe encabezado
        f.write('# Toro corregido con coordenadas de textura y normales\n')
        f.write(f'# Vertices: {len(vertices)}\n')
        f.write(f'# Faces: {len(faces)}\n\n')

        # Escribe vértices
        for v in vertices:
            f.write(f'v {v[0]} {v[1]} {v[2]}\n')

        # Escribe coordenadas de textura
        for vt in uvs:
            f.write(f'vt {vt[0]} {vt[1]}\n')

        # Escribe normales
        for vn in normales:
            f.write(f'vn {vn[0]} {vn[1]} {vn[2]}\n')

        # Escribe caras con índices de vértices, coordenadas de textura y normales
        for face in faces:
            f.write('f')
            for idx in face:
                f.write(f' {idx}/{idx}/{idx}')  # Formato: v/vt/vn
            f.write('\n')

    print(f"El archivo '{filename}' ha sido generado con éxito.")

# Parámetros de la malla
R = 1.0   # Radio mayor
r = 0.5   # Radio menor
N = 16    # Número de segmentos en el anillo mayor
M = 8     # Número de segmentos en el anillo menor

# Genera el toro y lo guarda en archivo OBJ
generar_toro(R, r, N, M, filename='donut.obj')