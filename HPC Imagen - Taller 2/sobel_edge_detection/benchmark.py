"""
Script de benchmark para medir rendimiento y generar graficas
Prueba el algoritmo con diferentes configuraciones y genera visualizaciones
"""
import sys
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import cpu_count

sys.path.insert(0, os.path.dirname(__file__))

from src.utils import load_image, rgb_to_grayscale
from src.sobel_sequential import apply_sobel_sequential
from src.sobel_parallel import apply_sobel_parallel


def benchmark_scalability():
    """
    Mide el rendimiento variando el numero de procesos
    Genera graficas de speedup y eficiencia
    """
    print("\n" + "="*70)
    print("=" + "  BENCHMARK DE ESCALABILIDAD  ".center(68) + "=")
    print("="*70 + "\n")

    # Configuracion
    test_image = "images/input/pikachu.jpg"

    if not os.path.exists(test_image):
        print(f"[ERROR] No se encuentra imagen: {test_image}")
        return

    # Cargar imagen
    print(f"Cargando imagen: {test_image}")
    rgb_image = load_image(test_image)
    gray_image = rgb_to_grayscale(rgb_image)
    print(f"Dimensiones: {gray_image.shape}")
    print(f"Pixeles: {gray_image.size:,}\n")

    max_cores = cpu_count()
    print(f"Cores disponibles: {max_cores}\n")

    # Configuraciones a probar
    num_processes_list = [1, 2, 4] + ([8] if max_cores >= 8 else [])
    if max_cores > 8:
        num_processes_list.append(max_cores)

    print(f"Probando con: {num_processes_list} procesos\n")

    # Medir tiempo secuencial (referencia)
    print("=" * 70)
    print("BASELINE: Ejecucion secuencial")
    print("=" * 70)

    times_seq = []
    for i in range(3):  # 3 repeticiones
        print(f"  Iteracion {i+1}/3...", end=" ")
        start = time.time()
        _ = apply_sobel_sequential(gray_image)
        elapsed = time.time() - start
        times_seq.append(elapsed)
        print(f"{elapsed:.4f} seg")

    time_sequential = np.mean(times_seq)
    std_sequential = np.std(times_seq)
    print(f"\nPromedio: {time_sequential:.4f} seg (± {std_sequential:.4f} seg)\n")

    # Medir tiempos paralelos
    results = []

    for num_proc in num_processes_list:
        print("=" * 70)
        print(f"Probando con {num_proc} procesos")
        print("=" * 70)

        times = []
        for i in range(3):  # 3 repeticiones
            print(f"  Iteracion {i+1}/3...", end=" ")
            start = time.time()
            _ = apply_sobel_parallel(gray_image, num_processes=num_proc)
            elapsed = time.time() - start
            times.append(elapsed)
            print(f"{elapsed:.4f} seg")

        avg_time = np.mean(times)
        std_time = np.std(times)
        speedup = time_sequential / avg_time
        efficiency = (speedup / num_proc) * 100

        results.append({
            'num_processes': num_proc,
            'time': avg_time,
            'std': std_time,
            'speedup': speedup,
            'efficiency': efficiency
        })

        print(f"\nPromedio: {avg_time:.4f} seg (± {std_time:.4f} seg)")
        print(f"Speedup:  {speedup:.2f}x")
        print(f"Eficiencia: {efficiency:.2f}%\n")

    # Crear directorio para graficas
    os.makedirs("results/plots", exist_ok=True)

    # Grafica 1: Tiempo de ejecucion vs Numero de procesos
    plt.figure(figsize=(10, 6))
    num_procs = [r['num_processes'] for r in results]
    times = [r['time'] for r in results]
    stds = [r['std'] for r in results]

    plt.errorbar(num_procs, times, yerr=stds, marker='o', linewidth=2,
                 markersize=8, capsize=5, label='Tiempo paralelo')
    plt.axhline(y=time_sequential, color='r', linestyle='--',
                linewidth=2, label='Tiempo secuencial')

    plt.xlabel('Numero de Procesos', fontsize=12)
    plt.ylabel('Tiempo de Ejecucion (segundos)', fontsize=12)
    plt.title('Tiempo de Ejecucion vs Numero de Procesos\nAlgoritmo Sobel', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.xticks(num_procs)
    plt.tight_layout()
    plt.savefig('results/plots/tiempo_vs_procesos.png', dpi=300)
    print("[OK] Grafica guardada: results/plots/tiempo_vs_procesos.png")

    # Grafica 2: Speedup vs Numero de procesos
    plt.figure(figsize=(10, 6))
    speedups = [r['speedup'] for r in results]

    plt.plot(num_procs, speedups, marker='o', linewidth=2, markersize=8,
             label='Speedup real')
    plt.plot(num_procs, num_procs, 'r--', linewidth=2, label='Speedup ideal (lineal)')

    plt.xlabel('Numero de Procesos', fontsize=12)
    plt.ylabel('Speedup', fontsize=12)
    plt.title('Speedup vs Numero de Procesos\nAlgoritmo Sobel', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.xticks(num_procs)
    plt.tight_layout()
    plt.savefig('results/plots/speedup_vs_procesos.png', dpi=300)
    print("[OK] Grafica guardada: results/plots/speedup_vs_procesos.png")

    # Grafica 3: Eficiencia vs Numero de procesos
    plt.figure(figsize=(10, 6))
    efficiencies = [r['efficiency'] for r in results]

    plt.plot(num_procs, efficiencies, marker='o', linewidth=2, markersize=8,
             color='green')
    plt.axhline(y=100, color='r', linestyle='--', linewidth=2, label='Eficiencia ideal (100%)')

    plt.xlabel('Numero de Procesos', fontsize=12)
    plt.ylabel('Eficiencia (%)', fontsize=12)
    plt.title('Eficiencia vs Numero de Procesos\nAlgoritmo Sobel', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.xticks(num_procs)
    plt.ylim([0, 110])
    plt.tight_layout()
    plt.savefig('results/plots/eficiencia_vs_procesos.png', dpi=300)
    print("[OK] Grafica guardada: results/plots/eficiencia_vs_procesos.png")

    # Grafica 4: Comparacion lado a lado
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Subplot 1: Tiempos
    axes[0].bar(num_procs, times, color='steelblue', alpha=0.7)
    axes[0].axhline(y=time_sequential, color='r', linestyle='--', linewidth=2)
    axes[0].set_xlabel('Numero de Procesos', fontsize=11)
    axes[0].set_ylabel('Tiempo (seg)', fontsize=11)
    axes[0].set_title('Tiempo de Ejecucion', fontsize=12)
    axes[0].grid(True, alpha=0.3, axis='y')

    # Subplot 2: Speedup
    axes[1].plot(num_procs, speedups, marker='o', linewidth=2, markersize=8,
                 color='green', label='Real')
    axes[1].plot(num_procs, num_procs, 'r--', linewidth=2, label='Ideal')
    axes[1].set_xlabel('Numero de Procesos', fontsize=11)
    axes[1].set_ylabel('Speedup', fontsize=11)
    axes[1].set_title('Speedup', fontsize=12)
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()

    # Subplot 3: Eficiencia
    axes[2].plot(num_procs, efficiencies, marker='o', linewidth=2, markersize=8,
                 color='orange')
    axes[2].axhline(y=100, color='r', linestyle='--', linewidth=2)
    axes[2].set_xlabel('Numero de Procesos', fontsize=11)
    axes[2].set_ylabel('Eficiencia (%)', fontsize=11)
    axes[2].set_title('Eficiencia', fontsize=12)
    axes[2].grid(True, alpha=0.3)
    axes[2].set_ylim([0, 110])

    plt.suptitle('Analisis de Rendimiento - Algoritmo Sobel Paralelo', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig('results/plots/analisis_completo.png', dpi=300, bbox_inches='tight')
    print("[OK] Grafica guardada: results/plots/analisis_completo.png")

    # Guardar resultados en archivo
    with open('results/benchmark_results.txt', 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("RESULTADOS DEL BENCHMARK\n")
        f.write("="*70 + "\n\n")

        f.write(f"Imagen: {test_image}\n")
        f.write(f"Dimensiones: {gray_image.shape}\n")
        f.write(f"Cores disponibles: {max_cores}\n\n")

        f.write("-"*70 + "\n")
        f.write("TIEMPO SECUENCIAL (BASELINE)\n")
        f.write("-"*70 + "\n")
        f.write(f"Promedio: {time_sequential:.4f} seg\n")
        f.write(f"Desv. Est.: {std_sequential:.4f} seg\n\n")

        f.write("-"*70 + "\n")
        f.write("RESULTADOS PARALELOS\n")
        f.write("-"*70 + "\n")
        f.write(f"{'Procesos':<12} {'Tiempo (seg)':<15} {'Speedup':<12} {'Eficiencia (%)':<15}\n")
        f.write("-"*70 + "\n")

        for r in results:
            f.write(f"{r['num_processes']:<12} "
                   f"{r['time']:<15.4f} "
                   f"{r['speedup']:<12.2f} "
                   f"{r['efficiency']:<15.2f}\n")

        f.write("\n" + "="*70 + "\n")

    print("[OK] Resultados guardados: results/benchmark_results.txt")

    print("\n" + "="*70)
    print("=" + "  BENCHMARK COMPLETADO  ".center(68) + "=")
    print("="*70 + "\n")


def main():
    """Ejecuta el benchmark"""
    try:
        benchmark_scalability()
    except Exception as e:
        print(f"\n[ERROR] Error durante benchmark: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
