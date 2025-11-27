"""
Script principal para ejecutar y comparar las implementaciones
Deteccion de Bordes Sobel: Secuencial vs Paralelo (Multicore)
"""
import os
import sys
from multiprocessing import cpu_count

sys.path.insert(0, os.path.dirname(__file__))

from src.sobel_sequential import sobel_edge_detection_sequential
from src.sobel_parallel import sobel_edge_detection_parallel


def main():
    """Ejecuta implementaciones secuencial y paralela, compara resultados"""

    input_image = "images/input/pikachu.jpg"
    output_seq = "images/output/pikachu_edges_sequential.jpg"
    output_par = "images/output/pikachu_edges_parallel.jpg"

    os.makedirs("images/input", exist_ok=True)
    os.makedirs("images/output", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    print("\n" + "="*70)
    print("  DETECCION DE BORDES SOBEL  ".center(70))
    print("  Comparacion Secuencial vs Paralelo (Multicore)  ".center(70))
    print("="*70 + "\n")

    cores_disponibles = cpu_count()
    print(f"Cores CPU disponibles: {cores_disponibles}")
    print(f"Imagen de entrada: {input_image}\n")

    if not os.path.exists(input_image):
        print(f"[ERROR] No se encuentra la imagen {input_image}")
        print("Por favor, coloca una imagen en images/input/")
        return

    # Ejecucion secuencial
    print("\n" + ">"*70)
    print("> EJECUCION SECUENCIAL (1 core)")
    print(">"*70)

    try:
        time_sequential = sobel_edge_detection_sequential(input_image, output_seq)
    except Exception as e:
        print(f"\n[ERROR] Fallo en ejecucion secuencial: {e}\n")
        return

    # Ejecucion paralela
    print("\n" + ">"*70)
    print(f"> EJECUCION PARALELA ({cores_disponibles} cores)")
    print(">"*70)

    try:
        time_parallel = sobel_edge_detection_parallel(
            input_image,
            output_par,
            num_processes=cores_disponibles
        )
    except Exception as e:
        print(f"\n[ERROR] Fallo en ejecucion paralela: {e}\n")
        return

    # Analisis de resultados
    print("\n" + "="*70)
    print("  ANALISIS DE RENDIMIENTO  ".center(70))
    print("="*70 + "\n")

    speedup = time_sequential / time_parallel
    efficiency = (speedup / cores_disponibles) * 100
    reduction = ((time_sequential - time_parallel) / time_sequential) * 100

    print(f"{'METRICA':<35} {'VALOR':>20}")
    print("-" * 70)
    print(f"{'Tiempo Secuencial (1 core):':<35} {time_sequential:>17.4f} seg")
    print(f"{'Tiempo Paralelo ({} cores):'.format(cores_disponibles):<35} {time_parallel:>17.4f} seg")
    print(f"{'Reduccion de tiempo:':<35} {time_sequential - time_parallel:>17.4f} seg")
    print("-" * 70)
    print(f"{'SPEEDUP:':<35} {speedup:>17.2f}x")
    print(f"{'Eficiencia:':<35} {efficiency:>17.2f}%")
    print(f"{'Reduccion porcentual:':<35} {reduction:>17.2f}%")
    print("-" * 70)

    print("\nINTERPRETACION:")
    print(f"La version paralela es {speedup:.2f}x mas rapida que la secuencial")
    print(f"usando {cores_disponibles} cores de CPU.")

    if efficiency > 70:
        print(f"Eficiencia excelente ({efficiency:.1f}%) - Muy buen aprovechamiento del paralelismo")
    elif efficiency > 40:
        print(f"Eficiencia buena ({efficiency:.1f}%) - Buen aprovechamiento del paralelismo")
    elif efficiency > 20:
        print(f"Eficiencia moderada ({efficiency:.1f}%) - Overhead de comunicacion entre procesos")
    else:
        print(f"Eficiencia baja ({efficiency:.1f}%) - Alto overhead, imagen pequena o muchos cores")

    # Guardar resultados
    with open("results/timing_results.txt", "w", encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("RESULTADOS - DETECCION DE BORDES SOBEL\n")
        f.write("="*70 + "\n\n")

        f.write(f"Imagen procesada: {input_image}\n")
        f.write(f"Cores CPU utilizados: {cores_disponibles}\n\n")

        f.write("-" * 70 + "\n")
        f.write("TIEMPOS DE EJECUCION\n")
        f.write("-" * 70 + "\n")
        f.write(f"Tiempo Secuencial (1 core):   {time_sequential:.4f} segundos\n")
        f.write(f"Tiempo Paralelo ({cores_disponibles} cores):    {time_parallel:.4f} segundos\n")
        f.write(f"Reduccion:                    {time_sequential - time_parallel:.4f} segundos\n\n")

        f.write("-" * 70 + "\n")
        f.write("METRICAS DE RENDIMIENTO\n")
        f.write("-" * 70 + "\n")
        f.write(f"Speedup:                      {speedup:.2f}x\n")
        f.write(f"Eficiencia:                   {efficiency:.2f}%\n")
        f.write(f"Reduccion porcentual:         {reduction:.2f}%\n\n")

        f.write("-" * 70 + "\n")
        f.write("INTERPRETACION\n")
        f.write("-" * 70 + "\n")
        f.write(f"La version paralela logro un speedup de {speedup:.2f}x\n")
        f.write(f"usando {cores_disponibles} cores de CPU.\n")
        f.write(f"Eficiencia: {efficiency:.2f}%\n")

    print(f"\nResultados guardados en: results/timing_results.txt")

    print("\n" + "="*70)
    print("  RESUMEN FINAL  ".center(70))
    print("="*70)
    print(f"\nProcesamiento completado exitosamente")
    print(f"Archivos generados:")
    print(f"  - {output_seq}")
    print(f"  - {output_par}")
    print(f"  - results/timing_results.txt")
    print(f"\nSpeedup obtenido: {speedup:.2f}x con {cores_disponibles} cores")
    print(f"Eficiencia: {efficiency:.2f}%")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
