# HPC — Taller: TSP por Fuerza Bruta (secuencial y paralelo)

## Descripción del Proyecto

Este repositorio contiene una implementación en Python de una solución por fuerza bruta para el Problema del Viajante (TSP). El código compara dos enfoques:

- *Un algoritmo secuencial* que evalúa todas las permutaciones (fuerza bruta).
- *Una versión paralela* que distribuye la evaluación de rutas entre procesos usando el módulo multiprocessing.

El propósito principal es educativo: demostrar el coste exponencial del TSP, comparar tiempos de ejecución secuenciales vs. paralelos y mostrar métricas de rendimiento y uso de recursos.

*Archivos principales:*
- tsp_secuencial.py - Implementación secuencial
- tsp_paralelo.py - Implementación paralela

---

## Requisitos del Sistema

### Hardware Recomendado
- *CPU:* Procesador multi-core (4+ núcleos recomendados)
- *RAM:* 8 GB mínimo; 16+ GB recomendado para experimentar con n≈10–12

### Software y Versiones Probadas
- *Sistema operativo:* macOS (también funciona en Linux/Windows)
- *Python:* 3.11+ (probado con Python 3.11)
- *Arquitectura:* ARM64 (Apple Silicon)

### Librerías Python Necesarias
bash
pip install itertools  # Incluida en Python standard library


---

## Instalación

### Clonar el repositorio
bash
git clone https://github.com/tu-usuario/HPC-TSP.git
cd HPC-TSP


### Instrucciones de Ejecución

*Ejecución del algoritmo secuencial:*
bash
/opt/homebrew/bin/python3.11 tsp_secuencial.py


*Ejecución del algoritmo paralelo:*
bash
/opt/homebrew/bin/python3.11 tsp_paralelo.py


---

## Estructura del Código

### tsp_secuencial.py

*Funciones principales:*

#### calcular_distancia(ciudad1, ciudad2)
- *Propósito:* Calcular la distancia euclidiana entre dos coordenadas (x,y).
- *Entrada:* Dos tuplas de float (x, y).
- *Salida:* Float (distancia).
- *Complejidad:* O(1).

#### calcular_distancia_ruta(ciudades, ruta)
- *Propósito:* Calcular la distancia total de una ruta circular (incluye regreso a la ciudad de origen).
- *Entrada:* ciudades: List[Tuple[float,float]], ruta: List[int].
- *Salida:* Float (distancia total).
- *Complejidad:* O(n) para una ruta de n ciudades.

#### tsp_secuencial(ciudades)
- *Propósito:* Evaluar todas las permutaciones (fijando la ciudad 0 como inicio) y devolver la mejor ruta encontrada.
- *Entrada:* Lista de coordenadas.
- *Salida:* (mejor_ruta, distancia_minima).
- *Complejidad temporal:* O((n-1)!)
- *Complejidad espacial:* O(1) adicional aparte de la entrada y el iterador de permutaciones.

*Pseudocódigo (secuencial):*
python
fijar ciudad_inicial = 0
para cada permutacion de ciudades[1..n-1]:
    ruta = [0] + permutacion
    distancia = calcular_distancia_ruta(ciudades, ruta)
    si distancia < mejor_distancia:
        guardar mejor_ruta y mejor_distancia
retornar mejor_ruta, mejor_distancia


---

### tsp_paralelo.py

*Funciones principales:*

#### evaluar_grupo_rutas(args)
- *Propósito:* Worker para evaluar un subconjunto de rutas (usado por Pool.map).
- *Entrada:* Tupla (ciudades, rutas_del_grupo).
- *Salida:* (mejor_ruta_local, distancia_minima_local).

#### tsp_paralelo(ciudades, num_procesos=None)
- *Propósito:* Genera todas las permutaciones, las reparte en num_procesos grupos y usa multiprocessing.Pool para evaluar cada grupo en paralelo.
- *Entrada:* Lista de coordenadas, número de procesos (opcional, por defecto usa todos los núcleos disponibles).
- *Salida:* (mejor_ruta, distancia_minima).
- *Complejidad temporal:* O((n-1)!) en trabajo total; el tiempo de pared puede reducirse aproximadamente por un factor de num_procesos menos overhead.

*Pseudocódigo (paralelo):*
python
generar lista completa de permutaciones
dividir la lista en k grupos (k = num_procesos)
pool.map(evaluar_grupo_rutas, grupos)
reducir resultados para obtener la mejor ruta global
retornar mejor_ruta, mejor_distancia


---

## Características Técnicas

### Algoritmos Implementados
- *Fuerza bruta (brute force):* Evaluación completa de permutaciones.
- *Patrones:* Maestro/worker (pool de procesos) en la versión paralela.

### Optimizaciones Aplicadas
- Fijar la ciudad 0 como punto de inicio para evitar rotaciones equivalentes (reduce factor n).
- Uso de itertools.permutations para generación eficiente de permutaciones.

### Manejo de Errores
- Validación de rutas y distancias.
- Manejo de casos especiales (rutas vacías, ciudades duplicadas).

---

## Ejemplo de Salida (Resultados Reales)

### Configuración del Sistema

Procesador: Apple Silicon (ARM64)
Núcleos físicos: 8
Arquitectura: ARM64
Sistema operativo: macOS
Python: 3.11


### Ejecución con 10 ciudades


================================================================================
PROBLEMA DEL VIAJERO - MÉTODO FUERZA BRUTA
COMPARACIÓN: SECUENCIAL vs PARALELO
================================================================================

Número de ciudades: 10
Rutas totales a evaluar: 181,440

Coordenadas de ciudades:
   Ciudad 0: (x₀, y₀)
   Ciudad 1: (x₁, y₁)
   Ciudad 2: (x₂, y₂)
   Ciudad 3: (x₃, y₃)
   Ciudad 4: (x₄, y₄)
   Ciudad 5: (x₅, y₅)
   Ciudad 6: (x₆, y₆)
   Ciudad 7: (x₇, y₇)
   Ciudad 8: (x₈, y₈)
   Ciudad 9: (x₉, y₉)

--------------------------------------------------------------------------------
 EJECUTANDO ALGORITMO SECUENCIAL (FUERZA BRUTA)
--------------------------------------------------------------------------------
   Evaluando rutas secuencialmente (fuerza bruta)...

 Mejor ruta encontrada: (0, 1, 9, 2, 7, 4, 8, 3, 5, 6)
 Distancia mínima: 31.02 unidades
 Tiempo de ejecución: 6.2098 segundos
 Rutas evaluadas: 181,440
 Procesos utilizados: 1

--------------------------------------------------------------------------------
 EJECUTANDO ALGORITMO PARALELO (FUERZA BRUTA DISTRIBUIDA)
--------------------------------------------------------------------------------
   Generando todas las permutaciones para dividir entre 8 procesos...
   Distribuyendo 181,440 rutas entre 8 procesos...
   Cada proceso evaluará aproximadamente 22,680 rutas...

 Mejor ruta encontrada: (0, 1, 9, 2, 7, 4, 8, 3, 5, 6)
 Distancia mínima: 31.02 unidades
 Tiempo de ejecución: 4.6486 segundos
 Rutas evaluadas: 181,440
 Procesos utilizados: 8
 Rutas por proceso: ~22,680

================================================================================
ANÁLISIS COMPARATIVO DE RENDIMIENTO
================================================================================

MÉTRICAS DE ACELERACIÓN:
   Speedup (aceleración): 1.34x
   Eficiencia paralela: 16.7%
   Mejora de tiempo: 25.1%
   Tiempo ahorrado: 1.5612 segundos

COMPARACIÓN DE TIEMPOS:
   Tiempo secuencial: 6.2098 segundos
   Tiempo paralelo: 4.6486 segundos
   Diferencia: 1.5612 segundos

COMPARACIÓN DE RECURSOS:
   Procesos secuencial: 1
   Procesos paralelo: 8
   Núcleos utilizados: 8 de 8

VERIFICACIÓN DE RESULTADOS:
   ✓ Ambos algoritmos encontraron la misma solución óptima
   ✓ Distancia: 31.02 unidades

CONCLUSIÓN:
   El algoritmo paralelo fue 1.34 veces más rápido
   Se logró aprovechar 16.7% de la capacidad de paralelización

================================================================================


---

## Interpretación de Resultados

La versión paralela reduce el tiempo de ejecución de *6.21 segundos a 4.65 segundos* (mejora del 25.1%), logrando un *speedup de 1.34×* con 8 núcleos.

La *eficiencia del 16.7%* es relativamente baja debido a:
- *Overhead de creación y gestión de procesos:* La inicialización del pool de workers y la comunicación inter-proceso consume tiempo.
- *Tamaño del problema:* Con 10 ciudades, aunque ya es suficiente para obtener beneficio del paralelismo, el overhead representa aproximadamente 20-30% del tiempo total.
- *Serialización de datos:* Python debe serializar/deserializar datos entre procesos.

### Escalabilidad Esperada
- *Para n=12-15 ciudades:* Se espera un speedup mayor (2-4×) ya que el overhead será una fracción menor del tiempo total.
- *Para n>15 ciudades:* El problema puede volverse intratable debido al crecimiento factorial, requiriendo heurísticas más sofisticadas.

---

## Problemas Conocidos y Soluciones

### Problema 1: Consumo de memoria en versión paralela
*Descripción:* La implementación actual materializa todas las permutaciones en memoria antes de distribuirlas.

*Solución:*
- Implementar streaming/chunks para no almacenar todo en memoria.
- Usar itertools.islice para procesar permutaciones en bloques.

### Problema 2: Overhead de paralelización
*Descripción:* Para problemas pequeños (n<10), el overhead puede superar los beneficios.

*Solución:*
- Ejecutar versión paralela solo si n≥10.
- Medir tiempo secuencial primero para decidir estrategia.

### Problema 3: Eficiencia subóptima
*Descripción:* Eficiencia del 16.7% indica subutilización de núcleos.

*Solución:*
- Aumentar el tamaño del problema (más ciudades).
- Optimizar la distribución de carga entre procesos.
- Reducir overhead usando técnicas de memoria compartida.

---

## Limitaciones Conocidas

1. *Escalabilidad:* Fuerza bruta es factorial — impracticable para n>12 en CPUs convencionales.
2. *Memoria:* La versión paralela puede fallar si la RAM es insuficiente para materializar todas las permutaciones.
3. *Eficiencia:* Con 8 núcleos solo se alcanza ~17% de eficiencia, indicando alto overhead.

---

## Autores

*Integrantes:*
- Miguel Flechas
- Andrés Castro
- Juan Hurtado

*Programa:* Ciencia de la Computación e Inteligencia Artificial  
*Universidad:* Sergio Arboleda  
*Asignatura:* Introducción a HPC  
*Fecha:* Octubre 2025

---

## Referencias

1. Applegate, D. L., Bixby, R. E., Chvátal, V., & Cook, W. J. (2006). The traveling salesman problem: a computational study. Princeton University Press.

2. Gutin, G., & Punnen, A. P. (Eds.). (2006). The traveling salesman problem and its variations. Springer Science & Business Media.

3. Python Software Foundation. (2023). multiprocessing — Process-based parallelism. Python Documentation.

---
