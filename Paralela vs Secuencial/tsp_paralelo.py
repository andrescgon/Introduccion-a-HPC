import itertools
import math
import time
from multiprocessing import Pool, cpu_count

def distancia(ciudad1, ciudad2):
    return math.sqrt((ciudad1[0] - ciudad2[0])**2 + (ciudad1[1] - ciudad2[1])**2)

def distancia_total(ruta, ciudades):
    total = 0
    for i in range(len(ruta) - 1):
        total += distancia(ciudades[ruta[i]], ciudades[ruta[i+1]])
    total += distancia(ciudades[ruta[-1]], ciudades[ruta[0]])
    return total

def evaluar_ruta(args):
    perm, ciudades = args
    return (perm, distancia_total(perm, ciudades))

def tsp_paralelo(ciudades):
    indices = list(range(len(ciudades)))
    permutaciones = list(itertools.permutations(indices))

    with Pool(processes=cpu_count()) as pool:
        resultados = pool.map(evaluar_ruta, [(p, ciudades) for p in permutaciones])

    mejor_ruta, mejor_distancia = min(resultados, key=lambda x: x[1])
    return mejor_ruta, mejor_distancia

if __name__ == "__main__":
    ciudades = [(0,0), (2,3), (5,2), (6,6), (8,3), (3,8), (1,5), (7,1), (9,6), (4,4)]
    print("Número de ciudades:", len(ciudades))
    print("Usando", cpu_count(), "núcleos")

    inicio = time.time()
    ruta, dist = tsp_paralelo(ciudades)
    fin = time.time()

    print("\n--- RESULTADOS PARALELOS ---")
    print("Mejor ruta:", ruta)
    print("Distancia mínima:", round(dist, 2))
    print("Tiempo de ejecución:", round(fin - inicio, 4), "segundos")