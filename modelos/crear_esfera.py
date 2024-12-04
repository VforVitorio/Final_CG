import numpy as np

def generar_esfera(filename, radio=0.5, latitudes=8, longitudes=16):
    """
    Genera un archivo .obj para una esfera de radio especificado, dividida en segmentos.

    Args:
        filename (str): Nombre del archivo de salida .obj.
        radio (float): Radio de la esfera.
        latitudes (int): Número de segmentos verticales.
        longitudes (int): Número de segmentos horizontales.
    """
    vertices = []
    normales = []
    texturas = []
    caras = []
    index_counter = 1  # Contador de índices de vértices

    # Matriz para almacenar los índices de los vértices
    indices_vertices = []

    # Generar vértices, normales y coordenadas de textura
    for i in range(latitudes + 1):
        theta = np.pi * i / latitudes
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)
        fila_indices = []

        for j in range(longitudes + 1):  # Añadimos un segmento extra para cerrar la esfera
            phi = 2 * np.pi * j / longitudes
            sin_phi = np.sin(phi)
            cos_phi = np.cos(phi)

            x = radio * sin_theta * cos_phi
            y = radio * cos_theta
            z = radio * sin_theta * sin_phi
            u = j / longitudes  # U va de 0 a 1
            v = i / latitudes   # V va de 0 a 1

            vertices.append(f"v {x} {y} {z}")
            normales.append(f"vn {x / radio} {y / radio} {z / radio}")
            texturas.append(f"vt {u} {v}")

            fila_indices.append(index_counter)
            index_counter += 1

        indices_vertices.append(fila_indices)

    # Generar caras (excepto los polos)
    for i in range(latitudes):
        for j in range(longitudes):
            p1 = indices_vertices[i][j]
            p2 = indices_vertices[i + 1][j]
            p3 = indices_vertices[i + 1][j + 1]
            p4 = indices_vertices[i][j + 1]

            # Evitar crear caras en los polos
            if i != 0:
                caras.append(f"f {p1}/{p1}/{p1} {p2}/{p2}/{p2} {p4}/{p4}/{p4}")
            if i != latitudes - 1:
                caras.append(f"f {p4}/{p4}/{p4} {p2}/{p2}/{p2} {p3}/{p3}/{p3}")

    # Escribir en el archivo
    with open(filename, 'w') as f:
        f.write(f"# ESFERA radio={radio}, latitudes={latitudes}, longitudes={longitudes}\n")
        f.write("# Vertices\n")
        f.write("\n".join(vertices) + "\n")
        f.write("# Normales\n")
        f.write("\n".join(normales) + "\n")
        f.write("# Texturas\n")
        f.write("\n".join(texturas) + "\n")
        f.write("# Caras\n")
        f.write("\n".join(caras) + "\n")

# Uso
generar_esfera("esfera.obj")
