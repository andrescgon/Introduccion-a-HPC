import itertools
import math
import time

def distancia(ciudad1, ciudad2):
    """Calcula la distancia euclidiana entre dos ciudades."""
    return math.sqrt((ciudad1[0] - ciudad2[0])**2 + (ciudad1[1] - ciudad2[1])**2)

def distancia_total(ruta, ciudades):
    """Evalúa la distancia total de una ruta."""
    total = 0
    for i in range(len(ruta) - 1):
        total += distancia(ciudades[ruta[i]], ciudades[ruta[i+1]])
    # Regresa a la ciudad inicial
    total += distancia(ciudades[ruta[-1]], ciudades[ruta[0]])
    return total

def tsp_fuerza_bruta(ciudades):
    indices = list(range(len(ciudades)))
    mejor_ruta = None
    mejor_distancia = float('inf')

    for perm in itertools.permutations(indices):
        d = distancia_total(perm, ciudades)
        if d < mejor_distancia:
            mejor_distancia = d
            mejor_ruta = perm

    return mejor_ruta, mejor_distancia

if __name__ == "__main__":
    ciudades = [(0,0), (2,3), (5,2), (6,6), (8,3), (3,8), (1,5), (7,1), (9,6), (4,4)]
    print("Número de ciudades:", len(ciudades))

    inicio = time.time()
    ruta, dist = tsp_fuerza_bruta(ciudades)
    fin = time.time()

    print("\n--- RESULTADOS ---")
    print("Mejor ruta:", ruta)
    print("Distancia mínima:", round(dist, 2))
    print("Tiempo de ejecución:", round(fin - inicio, 4), "segundos")