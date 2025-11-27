# Solucionador Distribuido TSP con Docker Swarm

Un sistema distribuido diseñado para resolver el **Problema del Viajante (TSP)** utilizando una arquitectura de microservicios orquestada por **Docker Swarm**. Este proyecto demuestra el poder de la computación paralela y el balanceo de carga en la resolución de problemas de optimización combinatoria.

## Descripción General

Esta solución divide la carga de trabajo en dos componentes principales:
1.  **Cluster Swarm (Servidor):** Una API Flask escalable que calcula la distancia euclidiana de una ruta. Desplegada con N réplicas para manejar peticiones concurrentes.
2.  **Cliente de Fuerza Bruta:** Un cliente en Python que genera todas las permutaciones posibles de ciudades y distribuye las tareas de cálculo a través del cluster Swarm usando concurrencia.

## Arquitectura

```mermaid
graph LR
    Client[Cliente Python] -->|Peticiones HTTP (Concurrentes)| LB[Ingress Docker Swarm]
    LB -->|Balanceo de Carga| Node1[Réplica 1]
    LB -->|Balanceo de Carga| Node2[Réplica 2]
    LB -->|Balanceo de Carga| Node3[Réplica 3]
    LB -->|Balanceo de Carga| Node4[Réplica 4]
```

## Comenzando

### Prerrequisitos
*   Docker Desktop (con Swarm habilitado)
*   Python 3.x
*   `pip install requests`

### 1. Desplegar el Cluster
Navega al directorio `docker` y ejecuta el script de despliegue:

```powershell
cd docker
.\deploy_swarm.ps1
```
*Esto construirá la imagen `travel-calculator:1.0` y desplegará 4 réplicas.*

### 2. Ejecutar el Solucionador
Navega al directorio `client and servers` y ejecuta el cliente:

```bash
cd "client and servers"
python client.py
```

##  Resultados
El sistema distribuye exitosamente la carga de calcular $N!$ rutas.
*   **Optimización:** Encuentra la distancia mínima global.
*   **Rendimiento:** Usa `ThreadPoolExecutor` para saturar la capacidad del cluster.

##  Autores
*   **Juan Hurtado**
*   **Andres Castro**
*   **Miguel Flechas**

---
*Universidad Sergio Arboleda - HPC Cluster*
