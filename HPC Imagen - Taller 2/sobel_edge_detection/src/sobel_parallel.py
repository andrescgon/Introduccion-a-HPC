"""
Implementacion paralela del algoritmo de deteccion de bordes Sobel
Utiliza multiprocessing para distribuir el trabajo entre multiples cores
"""
import numpy as np
from multiprocessing import Pool, cpu_count

# Manejar imports relativos y absolutos
try:
    from .utils import Timer
    from .sobel_sequential import SOBEL_KX, SOBEL_KY
except ImportError:
    from utils import Timer
    from sobel_sequential import SOBEL_KX, SOBEL_KY


def process_image_chunk(args):
    """
    Procesa un fragmento de la imagen (funcion worker para multiprocessing)

    Args:
        args: tupla con (gray_image, start_row, end_row)

    Returns:
        tupla (start_row, end_row, chunk_edges)
    """
    gray_image, start_row, end_row = args
    height, width = gray_image.shape

    chunk_edges = np.zeros((end_row - start_row, width), dtype=np.float32)

    for i in range(max(1, start_row), min(end_row, height-1)):
        for j in range(1, width-1):
            window = gray_image[i-1:i+2, j-1:j+2]

            gx = 0.0
            gy = 0.0
            for m in range(3):
                for n in range(3):
                    gx += window[m, n] * SOBEL_KX[m, n]
                    gy += window[m, n] * SOBEL_KY[m, n]

            magnitude = np.sqrt(gx**2 + gy**2)
            chunk_edges[i - start_row, j] = magnitude

    return (start_row, end_row, chunk_edges)


def apply_sobel_parallel(gray_image, num_processes=None):
    """
    Aplica Sobel usando multiples procesos en paralelo

    Args:
        gray_image: numpy array (height, width) en escala de grises
        num_processes: numero de procesos a usar (None = usar todos los cores)

    Returns:
        numpy array (height, width) con bordes detectados
    """
    if num_processes is None:
        num_processes = cpu_count()

    height, width = gray_image.shape

    if height < 3 or width < 3:
        raise ValueError(f"Imagen muy pequena ({height}x{width}). Minimo: 3x3")

    edges = np.zeros_like(gray_image, dtype=np.float32)

    # Dividir imagen en chunks
    rows_per_process = height // num_processes

    chunks_args = []
    for i in range(num_processes):
        start_row = i * rows_per_process

        if i < num_processes - 1:
            end_row = (i + 1) * rows_per_process
        else:
            end_row = height

        chunks_args.append((gray_image, start_row, end_row))

    # Procesar en paralelo
    with Pool(processes=num_processes) as pool:
        results = pool.map(process_image_chunk, chunks_args)

    # Combinar resultados
    for start_row, end_row, chunk_edges in results:
        edges[start_row:end_row, :] = chunk_edges

    return edges


def sobel_edge_detection_parallel(image_path, output_path, num_processes=None):
    """
    Pipeline completo de deteccion de bordes paralelo

    Args:
        image_path: Ruta de imagen de entrada
        output_path: Ruta donde guardar resultado
        num_processes: numero de procesos paralelos (None = usar todos los cores)

    Returns:
        float: Tiempo de ejecucion en segundos
    """
    try:
        from .utils import load_image, rgb_to_grayscale, save_image, normalize_image
    except ImportError:
        from utils import load_image, rgb_to_grayscale, save_image, normalize_image

    if num_processes is None:
        num_processes = cpu_count()

    print("\n" + "="*60)
    print("SOBEL EDGE DETECTION - VERSION PARALELA")
    print(f"Usando {num_processes} procesos paralelos")
    print("="*60)

    print(f"\nCargando imagen: {image_path}")
    rgb_image = load_image(image_path)
    print(f"Dimensiones: {rgb_image.shape[0]}x{rgb_image.shape[1]} pixeles")

    print("\nConvirtiendo a escala de grises...")
    gray_image = rgb_to_grayscale(rgb_image)

    print(f"\nAplicando deteccion de bordes Sobel ({num_processes} cores)...")
    with Timer("Procesamiento Sobel Paralelo") as timer:
        edges = apply_sobel_parallel(gray_image, num_processes)

    print("\nNormalizando y guardando resultado...")
    edges_normalized = normalize_image(edges)
    save_image(edges_normalized, output_path)

    print("\n" + "="*60)
    print(f"PROCESAMIENTO COMPLETADO")
    print(f"Tiempo: {timer.elapsed:.4f} segundos")
    print("="*60 + "\n")

    return timer.elapsed
