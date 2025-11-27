# Taller Práctico 3: Procesamiento de Video en Algoritmos Paralelos

Este proyecto implementa y compara la eficiencia de algoritmos secuenciales y paralelos (multihilos) para el procesamiento de video, específicamente transformando un video original a escala de grises.

**Universidad Sergio Arboleda - Noviembre 2025**

**Autores:**
* Juan Hurtado
* Miguel Flechas
* Andres Castro

## 📋 Descripción

El objetivo principal es medir el rendimiento (Speedup y Eficiencia) al utilizar múltiples núcleos de CPU para procesar frames de video en comparación con un enfoque secuencial tradicional.

El proyecto realiza las siguientes tareas:
1.  Carga un video de entrada (`rana.mp4`).
2.  Extrae los frames del video.
3.  Aplica una conversión a escala de grises utilizando dos métodos:
    *   **Secuencial:** Procesa un frame a la vez.
    *   **Paralelo:** Utiliza `multiprocessing` para procesar múltiples frames simultáneamente aprovechando los núcleos disponibles.
4.  Genera un nuevo video en escala de grises (`video_escala_grises.mp4`).
5.  Calcula y muestra métricas de rendimiento: Tiempo de ejecución, Speedup y Eficiencia.

## 🛠️ Requisitos

*   Python 3.x
*   Librerías:
    *   `opencv-python` (cv2)
    *   `numpy`

## 🚀 Instalación

Si deseas ejecutar este proyecto localmente, asegúrate de instalar las dependencias necesarias:

```bash
pip install opencv-python numpy
```

## 💻 Uso

### En Google Colab (Recomendado)

1.  Sube el archivo `Taller_3_COLAB.ipynb` a Google Colab.
2.  Sube el video `rana.mp4` al entorno de ejecución (arrastra y suelta en la carpeta de archivos).
3.  Ejecuta todas las celdas ("Runtime > Run all").
4.  El video resultante `video_escala_grises.mp4` se guardará en el entorno y podrás descargarlo.

### Ejecución Local

1.  Asegúrate de tener el video `rana.mp4` en el mismo directorio que el script o notebook.
2.  Ejecuta el notebook o el script de Python.
3.  Los frames procesados se guardarán en carpetas temporales (`frames_video_original`, `frames_video_gray`) y el video final se generará en el directorio raíz.

## 📂 Estructura del Proyecto

*   `Taller_3_COLAB.ipynb`: Notebook principal con el código fuente.
*   `rana.mp4`: Video de entrada para las pruebas.
*   `Procesamiento Paralelo.pdf`: Documentación adicional/teórica del taller.
*   `video_escala_grises.mp4`: (Generado) Video de salida procesado.

## 📊 Resultados Esperados

El script mostrará una comparación de tiempos similar a esta:

```text
Hardware: X núcleos CPU

Tiempos de Ejecución:
  Secuencial:  X.XXXX segundos
  Paralelo:    Y.YYYY segundos

Speedup: Z.ZZx
Eficiencia: WW.WW%
```
