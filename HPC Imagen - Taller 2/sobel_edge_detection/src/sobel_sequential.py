"""
Implementacion secuencial del algoritmo de deteccion de bordes Sobel
"""
import numpy as np

# Manejar imports relativos y absolutos
try:
    from .utils import Timer
except ImportError:
    from utils import Timer

SOBEL_KX = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
], dtype=np.float32)

SOBEL_KY = np.array([
    [-1, -2, -1],
    [0, 0, 0],
    [1, 2, 1]
], dtype=np.float32)


def apply_sobel_sequential(gray_image):
    """
    Aplica el operador Sobel de forma secuencial

    Args:
        gray_image: numpy array (height, width) en escala de grises

    Returns:
        numpy array (height, width) con magnitudes de gradientes
    """
    height, width = gray_image.shape

    if height < 3 or width < 3:
        raise ValueError(f"Imagen muy pequeña ({height}x{width}). Minimo: 3x3")

    edges = np.zeros_like(gray_image, dtype=np.float32)

    # Procesar cada pixel interior
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            window = gray_image[i-1:i+2, j-1:j+2]

            # Calcular gradientes
            gx = 0.0
            gy = 0.0
            for m in range(3):
                for n in range(3):
                    gx += window[m, n] * SOBEL_KX[m, n]
                    gy += window[m, n] * SOBEL_KY[m, n]

            # Magnitud del gradiente
            magnitude = np.sqrt(gx**2 + gy**2)
            edges[i, j] = magnitude

    return edges


def sobel_edge_detection_sequential(image_path, output_path):
    """
    Pipeline completo de deteccion de bordes secuencial

    Args:
        image_path: Ruta de imagen de entrada
        output_path: Ruta donde guardar resultado

    Returns:
        float: Tiempo de ejecucion en segundos
    """
    try:
        from .utils import load_image, rgb_to_grayscale, save_image, normalize_image
    except ImportError:
        from utils import load_image, rgb_to_grayscale, save_image, normalize_image

    print("\n" + "="*60)
    print("SOBEL EDGE DETECTION - VERSION SECUENCIAL")
    print("="*60)

    print(f"\nCargando imagen: {image_path}")
    rgb_image = load_image(image_path)
    print(f"Dimensiones: {rgb_image.shape[0]}x{rgb_image.shape[1]} pixeles")

    print("\nConvirtiendo a escala de grises...")
    gray_image = rgb_to_grayscale(rgb_image)

    print("\nAplicando deteccion de bordes Sobel...")
    with Timer("Procesamiento Sobel") as timer:
        edges = apply_sobel_sequential(gray_image)

    print("\nNormalizando y guardando resultado...")
    edges_normalized = normalize_image(edges)
    save_image(edges_normalized, output_path)

    print("\n" + "="*60)
    print(f"PROCESAMIENTO COMPLETADO")
    print(f"Tiempo: {timer.elapsed:.4f} segundos")
    print("="*60 + "\n")

    return timer.elapsed
