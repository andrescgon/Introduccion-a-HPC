# Deteccion de Bordes con Algoritmo Sobel

## Descripcion

Este proyecto implementa el algoritmo de deteccion de bordes **Sobel** de dos formas:
1. **Version Secuencial**: Procesa la imagen pixel por pixel en CPU
2. **Version Paralela GPU**: Distribuye el procesamiento usando CUDA

## Algoritmo Sobel

El operador Sobel detecta bordes calculando el gradiente de intensidad en cada pixel usando dos kernels 3x3:

**Kernel Horizontal (Kx):**
```
[-1  0  1]
[-2  0  2]
[-1  0  1]
```

**Kernel Vertical (Ky):**
```
[-1 -2 -1]
[ 0  0  0]
[ 1  2  1]
```

**Proceso:**
1. Convertir imagen a escala de grises
2. Para cada pixel, extraer ventana 3x3
3. Calcular Gx y Gy mediante convolucion
4. Calcular magnitud: G = sqrt(Gx^2 + Gy^2)

## Estructura del Proyecto

```
sobel_edge_detection/
├── images/
│   ├── input/          # Imagenes de prueba
│   └── output/         # Resultados
├── src/
│   ├── utils.py
│   ├── sobel_sequential.py
│   └── sobel_gpu.py
├── tests/
│   └── test_algorithms.py
├── results/
│   └── timing_results.txt
└── main.py
```

## Instalacion

```bash
pip install -r requirements.txt
```

## Uso

### Ejecucion Completa

```bash
python main.py
```

Este script ejecuta ambas versiones y compara resultados.

### Uso Individual

**Version Secuencial:**
```python
from src.sobel_sequential import sobel_edge_detection_sequential

time = sobel_edge_detection_sequential(
    "images/input/pikachu.jpg",
    "images/output/edges_sequential.jpg"
)
```

**Version GPU:**
```python
from src.sobel_gpu import sobel_edge_detection_gpu

time = sobel_edge_detection_gpu(
    "images/input/pikachu.jpg",
    "images/output/edges_gpu.jpg"
)
```

## Tests

```bash
python -m pytest tests/test_algorithms.py -v
```

## Autores

Juan Hurtado, Miguel Flechas T, Andres Castro
