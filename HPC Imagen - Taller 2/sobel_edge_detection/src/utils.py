"""
Utilidades para procesamiento de imágenes
"""
from PIL import Image
import numpy as np
import time


def load_image(image_path):
    """
    Carga una imagen y la convierte a array numpy RGB

    Args:
        image_path: Ruta de la imagen

    Returns:
        numpy array con la imagen RGB (height, width, 3)

    Raises:
        FileNotFoundError: Si la imagen no existe
        IOError: Si hay un error al cargar la imagen
    """
    try:
        # Abrir imagen con PIL
        img = Image.open(image_path)

        # Convertir a RGB (por si está en otro modo como RGBA o escala de grises)
        img_rgb = img.convert('RGB')

        # Convertir a numpy array
        img_array = np.array(img_rgb)

        return img_array

    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró la imagen en: {image_path}")
    except Exception as e:
        raise IOError(f"Error al cargar la imagen: {str(e)}")


def rgb_to_grayscale(rgb_image):
    """
    Convierte imagen RGB a escala de grises usando fórmula estándar

    La fórmula estándar pondera los canales según la percepción humana:
    Grayscale = 0.299*R + 0.587*G + 0.114*B

    Args:
        rgb_image: numpy array (height, width, 3) con valores RGB 0-255

    Returns:
        numpy array (height, width) con valores 0-255 en escala de grises

    Raises:
        ValueError: Si la imagen no tiene 3 canales
    """
    if len(rgb_image.shape) != 3 or rgb_image.shape[2] != 3:
        raise ValueError(f"La imagen debe tener 3 canales RGB. Forma actual: {rgb_image.shape}")

    # Coeficientes estándar para conversión RGB -> Grayscale
    # Estos valores reflejan la sensibilidad del ojo humano a diferentes colores
    r_weight = 0.299
    g_weight = 0.587
    b_weight = 0.114

    # Aplicar la fórmula de conversión
    gray = (rgb_image[:, :, 0] * r_weight +
            rgb_image[:, :, 1] * g_weight +
            rgb_image[:, :, 2] * b_weight)

    # Asegurar que los valores estén en el rango 0-255
    gray = np.clip(gray, 0, 255)

    # Convertir a uint8 para ahorrar memoria
    return gray.astype(np.uint8)


def save_image(image_array, output_path):
    """
    Guarda un array numpy como imagen

    Args:
        image_array: numpy array (2D para escala de grises o 3D para RGB)
        output_path: Ruta donde guardar la imagen

    Raises:
        ValueError: Si el array no tiene el formato correcto
        IOError: Si hay un error al guardar la imagen
    """
    try:
        # Validar dimensiones
        if len(image_array.shape) not in [2, 3]:
            raise ValueError(f"El array debe ser 2D o 3D. Forma actual: {image_array.shape}")

        # Asegurar que los valores estén en el rango correcto
        if image_array.dtype != np.uint8:
            # Normalizar si es necesario
            image_array = normalize_image(image_array)

        # Convertir a imagen PIL
        img = Image.fromarray(image_array)

        # Guardar
        img.save(output_path)

    except Exception as e:
        raise IOError(f"Error al guardar la imagen en {output_path}: {str(e)}")


def normalize_image(image_array):
    """
    Normaliza valores de imagen al rango 0-255

    Útil después de aplicar Sobel ya que los valores pueden exceder 255
    o ser negativos. Esta función escala linealmente todos los valores
    al rango completo 0-255.

    Args:
        image_array: numpy array con cualquier rango de valores

    Returns:
        numpy array con valores 0-255 (uint8)
    """
    # Convertir a float para evitar problemas de overflow
    img_float = image_array.astype(np.float32)

    # Encontrar el valor mínimo y máximo
    min_val = np.min(img_float)
    max_val = np.max(img_float)

    # Evitar división por cero
    if max_val - min_val == 0:
        # Si todos los valores son iguales, devolver una imagen uniforme
        return np.zeros_like(image_array, dtype=np.uint8)

    # Normalizar al rango 0-255
    normalized = ((img_float - min_val) / (max_val - min_val)) * 255.0

    # Convertir a uint8
    return normalized.astype(np.uint8)


class Timer:
    """
    Context manager para medir tiempo de ejecución

    Uso:
        with Timer("Mi operación") as timer:
            # código a medir
            realizar_operacion()

        # Al salir del bloque, imprime automáticamente el tiempo
        # También se puede acceder a timer.elapsed después
    """
    def __init__(self, name="Operation"):
        """
        Args:
            name: Nombre descriptivo de la operación a medir
        """
        self.name = name
        self.start = None
        self.end = None
        self.elapsed = None

    def __enter__(self):
        """Inicia el cronómetro al entrar al bloque with"""
        self.start = time.time()
        return self

    def __exit__(self, *args):
        """
        Detiene el cronómetro al salir del bloque with
        Calcula el tiempo transcurrido y lo imprime
        """
        self.end = time.time()
        self.elapsed = self.end - self.start
        print(f"{self.name} took {self.elapsed:.4f} seconds")
