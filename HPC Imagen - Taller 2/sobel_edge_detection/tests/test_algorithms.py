"""
Tests unitarios para los algoritmos de deteccion de bordes Sobel
"""
import sys
import os
import numpy as np
import pytest

# Agregar el directorio raiz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.utils import load_image, rgb_to_grayscale, normalize_image, save_image
from src.sobel_sequential import apply_sobel_sequential, SOBEL_KX, SOBEL_KY
from src.sobel_parallel import apply_sobel_parallel, process_image_chunk


class TestUtils:
    """Tests para funciones utilitarias"""

    def test_rgb_to_grayscale_shape(self):
        """Verifica que la conversion a escala de grises mantiene dimensiones correctas"""
        # Crear imagen RGB de prueba
        rgb_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)

        # Convertir a escala de grises
        gray_image = rgb_to_grayscale(rgb_image)

        # Verificar dimensiones
        assert gray_image.shape == (100, 100), f"Shape incorrecto: {gray_image.shape}"
        assert gray_image.dtype == np.uint8, f"Tipo incorrecto: {gray_image.dtype}"

    def test_rgb_to_grayscale_formula(self):
        """Verifica que la formula de conversion es correcta"""
        # Imagen simple: un pixel rojo puro
        rgb_image = np.array([[[255, 0, 0]]], dtype=np.uint8)

        # Resultado esperado: 0.299 * 255 = 76.245 ≈ 76
        gray_image = rgb_to_grayscale(rgb_image)
        expected = int(0.299 * 255)

        assert gray_image[0, 0] == expected, f"Formula incorrecta: {gray_image[0, 0]} != {expected}"

    def test_rgb_to_grayscale_invalid_input(self):
        """Verifica que se rechaza entrada invalida"""
        # Imagen sin 3 canales
        invalid_image = np.random.randint(0, 255, (100, 100), dtype=np.uint8)

        with pytest.raises(ValueError):
            rgb_to_grayscale(invalid_image)

    def test_normalize_image_range(self):
        """Verifica que normalize_image produce valores en rango 0-255"""
        # Imagen con valores fuera de rango
        image = np.array([[0, 500, 1000, -100]], dtype=np.float32)

        normalized = normalize_image(image)

        assert np.min(normalized) >= 0, "Valor minimo menor que 0"
        assert np.max(normalized) <= 255, "Valor maximo mayor que 255"
        assert normalized.dtype == np.uint8, f"Tipo incorrecto: {normalized.dtype}"

    def test_normalize_image_uniform(self):
        """Verifica comportamiento con imagen uniforme"""
        # Todos los valores iguales
        image = np.ones((10, 10), dtype=np.float32) * 100

        normalized = normalize_image(image)

        # Todos los valores deben ser 0 (no hay variacion)
        assert np.all(normalized == 0), "Imagen uniforme no se normaliza a 0"


class TestSobelKernels:
    """Tests para verificar los kernels Sobel"""

    def test_sobel_kx_shape(self):
        """Verifica que Kx tiene forma 3x3"""
        assert SOBEL_KX.shape == (3, 3), f"Kx shape incorrecto: {SOBEL_KX.shape}"

    def test_sobel_ky_shape(self):
        """Verifica que Ky tiene forma 3x3"""
        assert SOBEL_KY.shape == (3, 3), f"Ky shape incorrecto: {SOBEL_KY.shape}"

    def test_sobel_kx_values(self):
        """Verifica que Kx tiene los valores correctos"""
        expected = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
        assert np.array_equal(SOBEL_KX, expected), "Valores de Kx incorrectos"

    def test_sobel_ky_values(self):
        """Verifica que Ky tiene los valores correctos"""
        expected = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
        assert np.array_equal(SOBEL_KY, expected), "Valores de Ky incorrectos"


class TestSobelSequential:
    """Tests para implementacion secuencial"""

    def test_apply_sobel_sequential_shape(self):
        """Verifica que la salida tiene las mismas dimensiones que la entrada"""
        gray_image = np.random.randint(0, 255, (50, 50), dtype=np.uint8)

        edges = apply_sobel_sequential(gray_image)

        assert edges.shape == gray_image.shape, f"Shape incorrecto: {edges.shape}"

    def test_apply_sobel_sequential_edges_are_zero(self):
        """Verifica que los bordes de la imagen de salida son cero"""
        gray_image = np.random.randint(0, 255, (50, 50), dtype=np.uint8)

        edges = apply_sobel_sequential(gray_image)

        # Verificar bordes (primera y ultima fila/columna)
        assert np.all(edges[0, :] == 0), "Primera fila no es cero"
        assert np.all(edges[-1, :] == 0), "Ultima fila no es cero"
        assert np.all(edges[:, 0] == 0), "Primera columna no es cero"
        assert np.all(edges[:, -1] == 0), "Ultima columna no es cero"

    def test_apply_sobel_sequential_detects_vertical_edge(self):
        """Verifica que detecta un borde vertical simple"""
        # Crear imagen con borde vertical en el centro
        gray_image = np.zeros((10, 10), dtype=np.uint8)
        gray_image[:, :5] = 0    # Izquierda negra
        gray_image[:, 5:] = 255  # Derecha blanca

        edges = apply_sobel_sequential(gray_image)

        # Debe haber gradiente alto en el centro (columna 5)
        center_col = edges[:, 5]
        # Excluir bordes superior e inferior
        center_values = center_col[1:-1]

        assert np.mean(center_values) > 0, "No se detecto borde vertical"

    def test_apply_sobel_sequential_uniform_image(self):
        """Verifica que imagen uniforme produce bordes cercanos a cero"""
        # Imagen completamente uniforme
        gray_image = np.ones((50, 50), dtype=np.uint8) * 128

        edges = apply_sobel_sequential(gray_image)

        # Todos los valores interiores deben ser 0 (no hay gradiente)
        interior = edges[1:-1, 1:-1]
        assert np.all(interior == 0), "Imagen uniforme produjo gradientes"

    def test_apply_sobel_sequential_minimum_size(self):
        """Verifica que funciona con imagen minima (3x3)"""
        gray_image = np.random.randint(0, 255, (3, 3), dtype=np.uint8)

        edges = apply_sobel_sequential(gray_image)

        assert edges.shape == (3, 3), "No funciona con imagen 3x3"

    def test_apply_sobel_sequential_too_small(self):
        """Verifica que rechaza imagenes muy pequeñas"""
        gray_image = np.random.randint(0, 255, (2, 2), dtype=np.uint8)

        with pytest.raises(ValueError):
            apply_sobel_sequential(gray_image)


class TestSobelParallel:
    """Tests para implementacion paralela"""

    def test_apply_sobel_parallel_shape(self):
        """Verifica que la salida tiene las mismas dimensiones que la entrada"""
        gray_image = np.random.randint(0, 255, (50, 50), dtype=np.uint8)

        edges = apply_sobel_parallel(gray_image, num_processes=2)

        assert edges.shape == gray_image.shape, f"Shape incorrecto: {edges.shape}"

    def test_apply_sobel_parallel_vs_sequential(self):
        """Verifica que paralelo produce el mismo resultado que secuencial"""
        gray_image = np.random.randint(0, 255, (100, 100), dtype=np.uint8)

        edges_seq = apply_sobel_sequential(gray_image)
        edges_par = apply_sobel_parallel(gray_image, num_processes=4)

        # Los resultados deben ser identicos (o muy cercanos debido a floating point)
        diff = np.abs(edges_seq - edges_par)
        max_diff = np.max(diff)

        assert max_diff < 0.001, f"Diferencia maxima entre seq y par: {max_diff}"

    def test_apply_sobel_parallel_different_num_processes(self):
        """Verifica que funciona con diferentes numeros de procesos"""
        gray_image = np.random.randint(0, 255, (80, 80), dtype=np.uint8)

        edges_ref = apply_sobel_sequential(gray_image)

        for num_proc in [1, 2, 4]:
            edges = apply_sobel_parallel(gray_image, num_processes=num_proc)
            diff = np.abs(edges_ref - edges)
            assert np.max(diff) < 0.001, f"Fallo con {num_proc} procesos"

    def test_process_image_chunk(self):
        """Verifica que process_image_chunk funciona correctamente"""
        gray_image = np.random.randint(0, 255, (50, 50), dtype=np.uint8)

        # Procesar chunk central
        start_row, end_row = 10, 40
        args = (gray_image, start_row, end_row)

        result_start, result_end, chunk_edges = process_image_chunk(args)

        assert result_start == start_row, "start_row incorrecto"
        assert result_end == end_row, "end_row incorrecto"
        assert chunk_edges.shape == (end_row - start_row, 50), f"Shape incorrecto: {chunk_edges.shape}"


class TestIntegration:
    """Tests de integracion del pipeline completo"""

    def test_full_pipeline_with_test_image(self):
        """Verifica que el pipeline completo funciona con la imagen de prueba"""
        test_image_path = "images/input/pikachu.jpg"

        # Verificar que existe la imagen
        if not os.path.exists(test_image_path):
            pytest.skip("Imagen de prueba no encontrada")

        # Cargar y procesar
        rgb_image = load_image(test_image_path)
        gray_image = rgb_to_grayscale(rgb_image)
        edges = apply_sobel_sequential(gray_image)
        normalized = normalize_image(edges)

        # Verificaciones
        assert normalized.shape == gray_image.shape, "Shape incorrecto"
        assert normalized.dtype == np.uint8, "Tipo incorrecto"
        assert np.min(normalized) >= 0 and np.max(normalized) <= 255, "Rango incorrecto"

    def test_sequential_vs_parallel_same_output(self):
        """Verifica que secuencial y paralelo producen resultados identicos"""
        test_image_path = "images/input/pikachu.jpg"

        if not os.path.exists(test_image_path):
            pytest.skip("Imagen de prueba no encontrada")

        # Cargar imagen
        rgb_image = load_image(test_image_path)
        gray_image = rgb_to_grayscale(rgb_image)

        # Procesar con ambos metodos
        edges_seq = apply_sobel_sequential(gray_image)
        edges_par = apply_sobel_parallel(gray_image, num_processes=4)

        # Comparar
        diff = np.abs(edges_seq - edges_par)
        max_diff = np.max(diff)
        mean_diff = np.mean(diff)

        print(f"\nDiferencia maxima: {max_diff:.6f}")
        print(f"Diferencia promedio: {mean_diff:.6f}")

        assert max_diff < 0.001, f"Resultados difieren (max diff: {max_diff})"
        assert mean_diff < 0.0001, f"Resultados difieren (mean diff: {mean_diff})"


# Funcion para ejecutar los tests
def run_tests():
    """Ejecuta todos los tests con pytest"""
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_tests()
