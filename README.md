# Péndulos de Newton: Modelo Inicial Proyecto Computación Gráfica

## 📝 Descripción

En este repositorio se encuentra el código desarrollado por el Grupo 06 de la asignatura de Computación Gráfica para el renderizado, diseño y modelado de un péndulo de Newton.

Se trata del primer modelo desarrollado, ausente de simulación física y con las operaciones enviadas a la CPU.

## ✔️ Características

- Renderizado 3D con OpenGL
- Texturas y materiales realistas
- Sistema de cámara interactivo
- Iluminación dinámica
- Interfaz de usuario intuitiva

## 🗂️ Estructura del Proyecto

| Archivo               | Descripción                 |
| --------------------- | --------------------------- |
| `main.py`             | Punto de entrada principal  |
| `modelo.py`           | Gestión de modelos 3D       |
| `camara.py`           | Sistema de cámara           |
| `transformaciones.py` | Funciones de transformación |
| `texturas.py`         | Gestión de texturas         |
| `luces.py`            | Sistema de iluminación      |
| `utilidades.py`       | Funciones auxiliares        |
| `configuracion.py`    | Constantes globales         |

## 🎮 Controles

| Acción        | Control         |
| ------------- | --------------- |
| Rotar cámara  | Mouse / Flechas |
| Zoom          | Rueda del mouse |
| Zoom in/out   | Q/A             |
| Roll cámara   | E/D             |
| Reset cámara  | R               |
| Control luces | 1/2/3           |

## ⚙️ Requisitos

1. `pygame==2.5.2`
2. `PyOpenGL==3.1.7`
3. `PyOpenGL-accelerate==3.1.7`
4. `numpy==1.26.2`

## 🚀 Instalación

1. Clonar el repositorio

```bash
git clone https://github.com/VforVitorio/Final_CG.git
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt

python main.py
```
