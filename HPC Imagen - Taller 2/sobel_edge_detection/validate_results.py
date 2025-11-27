"""
Script de validacion para comparar resultados secuenciales y paralelos
Verifica que ambas implementaciones producen resultados identicos
"""
import sys
import os
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))

from src.utils import load_image, rgb_to_grayscale
from src.sobel_sequential import apply_sobel_sequential
from src.sobel_parallel import apply_sobel_parallel


def compare_images_pixel_by_pixel(image1, image2):
    """
    Compara dos imagenes pixel por pixel

    Args:
        image1: primer array numpy
        image2: segundo array numpy

    Returns:
        dict con estadisticas de comparacion
    """
    if image1.shape != image2.shape:
        return {
            'identical': False,
            'error': f'Shapes diferentes: {image1.shape} vs {image2.shape}'
        }

    # Calcular diferencias
    diff = np.abs(image1.astype(np.float32) - image2.astype(np.float32))

    stats = {
        'identical': np.allclose(image1, image2, atol=0.001),
        'max_difference': np.max(diff),
        'mean_difference': np.mean(diff),
        'std_difference': np.std(diff),
        'num_different_pixels': np.sum(diff > 0.001),
        'total_pixels': image1.size,
        'percentage_different': (np.sum(diff > 0.001) / image1.size) * 100
    }

    return stats


def validate_algorithms():
    """
    Valida que las implementaciones secuencial y paralela producen
    resultados identicos
    """
    print("\n" + "="*70)
    print("=" + "  VALIDACION DE RESULTADOS  ".center(68) + "=")
    print("="*70 + "\n")

    # Configuracion
    test_image = "images/input/pikachu.jpg"

    if not os.path.exists(test_image):
        print(f"[ERROR] No se encuentra imagen de prueba: {test_image}")
        return False

    # Cargar imagen
    print(f"1. Cargando imagen de prueba: {test_image}")
    rgb_image = load_image(test_image)
    gray_image = rgb_to_grayscale(rgb_image)
    print(f"   Dimensiones: {gray_image.shape}")
    print(f"   Total de pixeles: {gray_image.size:,}\n")

    # Procesar con algoritmo secuencial
    print("2. Procesando con algoritmo SECUENCIAL...")
    edges_sequential = apply_sobel_sequential(gray_image)
    print(f"   Rango: [{np.min(edges_sequential):.2f}, {np.max(edges_sequential):.2f}]\n")

    # Procesar con algoritmo paralelo (diferentes numeros de procesos)
    test_configs = [1, 2, 4, 8]

    print("3. Procesando con algoritmo PARALELO (diferentes configuraciones)...\n")

    all_valid = True

    for num_proc in test_configs:
        print(f"   Probando con {num_proc} procesos...")

        edges_parallel = apply_sobel_parallel(gray_image, num_processes=num_proc)

        # Comparar
        stats = compare_images_pixel_by_pixel(edges_sequential, edges_parallel)

        if stats.get('error'):
            print(f"      [ERROR] {stats['error']}")
            all_valid = False
            continue

        # Mostrar resultados
        print(f"      Diferencia maxima:     {stats['max_difference']:.6f}")
        print(f"      Diferencia promedio:   {stats['mean_difference']:.6f}")
        print(f"      Pixeles diferentes:    {stats['num_different_pixels']:,} "
              f"({stats['percentage_different']:.3f}%)")

        if stats['identical']:
            print(f"      [OK] Resultados IDENTICOS\n")
        else:
            print(f"      [WARNING] Pequenas diferencias (posiblemente por floating point)\n")
            if stats['max_difference'] > 0.1:
                print(f"      [ERROR] Diferencias significativas detectadas!")
                all_valid = False

    # Validar que las imagenes guardadas son identicas
    print("4. Validando imagenes guardadas en disco...\n")

    seq_path = "images/output/pikachu_edges_sequential.jpg"
    par_path = "images/output/pikachu_edges_parallel.jpg"

    if os.path.exists(seq_path) and os.path.exists(par_path):
        img_seq = np.array(Image.open(seq_path).convert('L'))
        img_par = np.array(Image.open(par_path).convert('L'))

        stats_saved = compare_images_pixel_by_pixel(img_seq, img_par)

        print(f"   Imagenes guardadas:")
        print(f"      - {seq_path}")
        print(f"      - {par_path}")
        print(f"      Diferencia maxima:     {stats_saved['max_difference']:.2f}")
        print(f"      Pixeles diferentes:    {stats_saved['num_different_pixels']:,} "
              f"({stats_saved['percentage_different']:.2f}%)")

        # JPG es lossy, permitir pequeñas diferencias
        if stats_saved['max_difference'] < 5:  # Tolerancia para compresion JPG
            print(f"      [OK] Imagenes equivalentes (diferencias por compresion JPG)\n")
        else:
            print(f"      [WARNING] Diferencias mayores de lo esperado\n")
    else:
        print("   [SKIP] Imagenes guardadas no encontradas\n")

    # Resultado final
    print("="*70)
    if all_valid:
        print("=" + "  [OK] VALIDACION EXITOSA  ".center(68) + "=")
        print("=" + "  Todas las implementaciones producen resultados identicos  ".center(68) + "=")
    else:
        print("=" + "  [ERROR] VALIDACION FALLIDA  ".center(68) + "=")
        print("=" + "  Se detectaron diferencias significativas  ".center(68) + "=")
    print("="*70 + "\n")

    return all_valid


def main():
    """Ejecuta la validacion"""
    success = validate_algorithms()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
