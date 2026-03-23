"""
Sistema de Alerta de Tráfico usando Lógica Difusa

Este sistema determina el nivel de alerta de congestión de tráfico basándose en:
- Cantidad de vehículos en la vía
- Velocidad promedio de los vehículos

El sistema genera alertas de tres niveles: baja, media y alta.

Autor: Juan Manuel Vega
Fecha: Febrero 2026
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


class SistemaAlertaTrafico:
    """
    Clase que implementa un sistema de alerta de tráfico usando lógica difusa.
    
    Variables de entrada:
    - Vehículos: cantidad de vehículos por kilómetro (0-100)
    - Velocidad: velocidad promedio en km/h (0-120)
    
    Variable de salida:
    - Alerta: nivel de alerta de congestión (0-10)
    """
    
    def __init__(self):
        """Inicializa el sistema de lógica difusa"""
        self._crear_variables()
        self._crear_funciones_pertenencia()
        self._crear_reglas()
        self._crear_sistema_control()
    
    def _crear_variables(self):
        """
        Crea las variables difusas de entrada y salida.
        
        Variables de entrada:
        - vehiculos: rango [0, 100] vehículos por km
        - velocidad: rango [0, 120] km/h
        
        Variable de salida:
        - alerta: rango [0, 10] nivel de alerta
        """
        # Variables de entrada
        self.vehiculos = ctrl.Antecedent(np.arange(0, 101, 1), 'vehiculos')
        self.velocidad = ctrl.Antecedent(np.arange(0, 121, 1), 'velocidad')
        
        # Variable de salida
        self.alerta = ctrl.Consequent(np.arange(0, 11, 1), 'alerta')
    
    def _crear_funciones_pertenencia(self):
        """
        Define las funciones de pertenencia para cada variable difusa.
        
        Para vehículos:
        - pocos: función trapezoidal (0, 0, 15, 30)
        - moderados: función triangular (20, 40, 60)
        - muchos: función trapezoidal (50, 70, 100, 100)
        
        Para velocidad:
        - lenta: función trapezoidal (0, 0, 20, 40)
        - media: función triangular (30, 55, 80)
        - rapida: función trapezoidal (70, 90, 120, 120)
        
        Para alerta:
        - baja: función trapezoidal (0, 0, 2, 4)
        - media: función triangular (3, 5, 7)
        - alta: función trapezoidal (6, 8, 10, 10)
        """
        
        # Funciones de pertenencia para vehículos
        self.vehiculos['pocos'] = fuzz.trapmf(self.vehiculos.universe, [0, 0, 15, 30])
        self.vehiculos['moderados'] = fuzz.trimf(self.vehiculos.universe, [20, 40, 60])
        self.vehiculos['muchos'] = fuzz.trapmf(self.vehiculos.universe, [50, 70, 100, 100])
        
        # Funciones de pertenencia para velocidad
        self.velocidad['lenta'] = fuzz.trapmf(self.velocidad.universe, [0, 0, 20, 40])
        self.velocidad['media'] = fuzz.trimf(self.velocidad.universe, [30, 55, 80])
        self.velocidad['rapida'] = fuzz.trapmf(self.velocidad.universe, [70, 90, 120, 120])
        
        # Funciones de pertenencia para alerta
        self.alerta['baja'] = fuzz.trapmf(self.alerta.universe, [0, 0, 2, 4])
        self.alerta['media'] = fuzz.trimf(self.alerta.universe, [3, 5, 7])
        self.alerta['alta'] = fuzz.trapmf(self.alerta.universe, [6, 8, 10, 10])
    
    def _crear_reglas(self):
        """
        Define las reglas difusas del sistema basándose en el conocimiento experto.
        
        Reglas de inferencia:
        1. Si hay pocos vehículos y velocidad rápida → alerta baja
        2. Si hay pocos vehículos y velocidad media → alerta baja
        3. Si hay pocos vehículos y velocidad lenta → alerta media
        4. Si hay vehículos moderados y velocidad rápida → alerta baja
        5. Si hay vehículos moderados y velocidad media → alerta media
        6. Si hay vehículos moderados y velocidad lenta → alerta alta
        7. Si hay muchos vehículos y velocidad rápida → alerta media
        8. Si hay muchos vehículos y velocidad media → alerta alta
        9. Si hay muchos vehículos y velocidad lenta → alerta alta
        """
        
        self.reglas = [
            # Regla 1: Pocos vehículos + velocidad rápida = alerta baja
            ctrl.Rule(self.vehiculos['pocos'] & self.velocidad['rapida'], 
                     self.alerta['baja']),
            
            # Regla 2: Pocos vehículos + velocidad media = alerta baja
            ctrl.Rule(self.vehiculos['pocos'] & self.velocidad['media'], 
                     self.alerta['baja']),
            
            # Regla 3: Pocos vehículos + velocidad lenta = alerta media
            ctrl.Rule(self.vehiculos['pocos'] & self.velocidad['lenta'], 
                     self.alerta['media']),
            
            # Regla 4: Vehículos moderados + velocidad rápida = alerta baja
            ctrl.Rule(self.vehiculos['moderados'] & self.velocidad['rapida'], 
                     self.alerta['baja']),
            
            # Regla 5: Vehículos moderados + velocidad media = alerta media
            ctrl.Rule(self.vehiculos['moderados'] & self.velocidad['media'], 
                     self.alerta['media']),
            
            # Regla 6: Vehículos moderados + velocidad lenta = alerta alta
            ctrl.Rule(self.vehiculos['moderados'] & self.velocidad['lenta'], 
                     self.alerta['alta']),
            
            # Regla 7: Muchos vehículos + velocidad rápida = alerta media
            ctrl.Rule(self.vehiculos['muchos'] & self.velocidad['rapida'], 
                     self.alerta['media']),
            
            # Regla 8: Muchos vehículos + velocidad media = alerta alta
            ctrl.Rule(self.vehiculos['muchos'] & self.velocidad['media'], 
                     self.alerta['alta']),
            
            # Regla 9: Muchos vehículos + velocidad lenta = alerta alta
            ctrl.Rule(self.vehiculos['muchos'] & self.velocidad['lenta'], 
                     self.alerta['alta'])
        ]
    
    def _crear_sistema_control(self):
        """
        Crea el sistema de control difuso combinando todas las reglas.
        """
        self.sistema_control = ctrl.ControlSystem(self.reglas)
        self.simulacion = ctrl.ControlSystemSimulation(self.sistema_control)
    
    def calcular_alerta(self, num_vehiculos, velocidad_promedio):
        """
        Calcula el nivel de alerta basado en el número de vehículos y la velocidad.
        
        Args:
            num_vehiculos (float): Número de vehículos por kilómetro (0-100)
            velocidad_promedio (float): Velocidad promedio en km/h (0-120)
        
        Returns:
            float: Nivel de alerta (0-10)
            str: Categoría de alerta ('baja', 'media', 'alta')
        """
        
        # Validar entradas
        if not (0 <= num_vehiculos <= 100):
            raise ValueError("El número de vehículos debe estar entre 0 y 100")
        if not (0 <= velocidad_promedio <= 120):
            raise ValueError("La velocidad debe estar entre 0 y 120 km/h")
        
        # Asignar valores de entrada
        self.simulacion.input['vehiculos'] = num_vehiculos
        self.simulacion.input['velocidad'] = velocidad_promedio
        
        # Ejecutar la simulación
        self.simulacion.compute()
        
        # Obtener el valor de salida
        nivel_alerta = self.simulacion.output['alerta']
        
        # Determinar la categoría de alerta
        if nivel_alerta <= 3:
            categoria = 'baja'
        elif nivel_alerta <= 6:
            categoria = 'media'
        else:
            categoria = 'alta'
        
        return nivel_alerta, categoria
    
    def interpretar_resultado(self, nivel_alerta, categoria, num_vehiculos, velocidad_promedio):
        """
        Proporciona una interpretación textual del resultado.
        
        Args:
            nivel_alerta (float): Valor numérico del nivel de alerta
            categoria (str): Categoría de alerta
            num_vehiculos (float): Número de vehículos usado como entrada
            velocidad_promedio (float): Velocidad promedio usada como entrada
        
        Returns:
            str: Interpretación textual del resultado
        """
        interpretaciones = {
            'baja': {
                'descripcion': 'Tráfico fluido',
                'recomendacion': 'No se requieren acciones especiales. Mantener monitoreo normal.',
                'color': '🟢'
            },
            'media': {
                'descripcion': 'Congestión moderada',
                'recomendacion': 'Considerar activar señalización variable y rutas alternativas.',
                'color': '🟡'
            },
            'alta': {
                'descripcion': 'Congestión severa',
                'recomendacion': 'Activar semáforos adaptativos, rutas alternativas y alertas a usuarios.',
                'color': '🔴'
            }
        }
        
        info = interpretaciones[categoria]
        
        resultado = f"""
{info['color']} ALERTA DE TRÁFICO {info['color']}

Condiciones de entrada:
• Vehículos por km: {num_vehiculos:.1f}
• Velocidad promedio: {velocidad_promedio:.1f} km/h

Resultado del análisis:
• Nivel de alerta: {nivel_alerta:.2f}/10
• Categoría: {categoria.upper()}
• Estado: {info['descripcion']}

Recomendación:
{info['recomendacion']}
        """
        
        return resultado
    
    def visualizar_funciones_pertenencia(self):
        """
        Crea visualizaciones de las funciones de pertenencia de todas las variables.
        """
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
        
        # Visualización de vehículos
        ax1.plot(self.vehiculos.universe, self.vehiculos['pocos'].mf, 'b', linewidth=2, label='Pocos')
        ax1.plot(self.vehiculos.universe, self.vehiculos['moderados'].mf, 'g', linewidth=2, label='Moderados')
        ax1.plot(self.vehiculos.universe, self.vehiculos['muchos'].mf, 'r', linewidth=2, label='Muchos')
        ax1.set_title('Vehículos por km')
        ax1.set_xlabel('Número de vehículos')
        ax1.set_ylabel('Grado de pertenencia')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Visualización de velocidad
        ax2.plot(self.velocidad.universe, self.velocidad['lenta'].mf, 'b', linewidth=2, label='Lenta')
        ax2.plot(self.velocidad.universe, self.velocidad['media'].mf, 'g', linewidth=2, label='Media')
        ax2.plot(self.velocidad.universe, self.velocidad['rapida'].mf, 'r', linewidth=2, label='Rápida')
        ax2.set_title('Velocidad promedio')
        ax2.set_xlabel('Velocidad (km/h)')
        ax2.set_ylabel('Grado de pertenencia')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Visualización de alerta
        ax3.plot(self.alerta.universe, self.alerta['baja'].mf, 'b', linewidth=2, label='Baja')
        ax3.plot(self.alerta.universe, self.alerta['media'].mf, 'g', linewidth=2, label='Media')
        ax3.plot(self.alerta.universe, self.alerta['alta'].mf, 'r', linewidth=2, label='Alta')
        ax3.set_title('Nivel de alerta')
        ax3.set_xlabel('Nivel de alerta')
        ax3.set_ylabel('Grado de pertenencia')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def superficie_control(self, num_puntos=50):
        """
        Genera la superficie de control tridimensional del sistema.
        
        Args:
            num_puntos (int): Número de puntos para cada eje del gráfico
        
        Returns:
            tuple: Figura de matplotlib y datos de la superficie
        """
        # Crear mesh para la superficie
        vehiculos_range = np.linspace(0, 100, num_puntos)
        velocidad_range = np.linspace(0, 120, num_puntos)
        vehiculos_mesh, velocidad_mesh = np.meshgrid(vehiculos_range, velocidad_range)
        
        # Calcular alerta para cada punto
        alerta_mesh = np.zeros_like(vehiculos_mesh)
        
        for i in range(num_puntos):
            for j in range(num_puntos):
                try:
                    alerta_value, _ = self.calcular_alerta(vehiculos_mesh[i, j], velocidad_mesh[i, j])
                    alerta_mesh[i, j] = alerta_value
                except:
                    alerta_mesh[i, j] = np.nan
        
        # Crear gráfico 3D
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        superficie = ax.plot_surface(vehiculos_mesh, velocidad_mesh, alerta_mesh, 
                                   cmap='RdYlGn_r', alpha=0.8)
        
        ax.set_xlabel('Vehículos por km')
        ax.set_ylabel('Velocidad promedio (km/h)')
        ax.set_zlabel('Nivel de alerta')
        ax.set_title('Superficie de Control - Sistema de Alerta de Tráfico')
        
        # Añadir barra de colores
        fig.colorbar(superficie, ax=ax, shrink=0.5, aspect=10)
        
        return fig, (vehiculos_mesh, velocidad_mesh, alerta_mesh)


def ejemplo_uso():
    """
    Función de demonstración del sistema de alerta de tráfico.
    """
    print("=== SISTEMA DE ALERTA DE TRÁFICO ===")
    print("Implementación usando Lógica Difusa")
    print("=" * 50)
    
    # Crear instancia del sistema
    sistema = SistemaAlertaTrafico()
    
    # Casos de prueba representativos
    casos_prueba = [
        (10, 80, "Pocos vehículos circulando a velocidad normal"),
        (25, 45, "Tráfico moderado con velocidad reducida"),
        (60, 30, "Muchos vehículos con velocidad baja"),
        (80, 15, "Alta densidad vehicular con velocidad muy baja"),
        (35, 90, "Densidad media con alta velocidad"),
        (5, 25, "Muy pocos vehículos a baja velocidad")
    ]
    
    print("\nEJECUCIÓN DE CASOS DE PRUEBA:")
    print("=" * 50)
    
    for i, (vehiculos, velocidad, descripcion) in enumerate(casos_prueba, 1):
        print(f"\n--- CASO {i} ---")
        print(f"Escenario: {descripcion}")
        
        try:
            nivel_alerta, categoria = sistema.calcular_alerta(vehiculos, velocidad)
            interpretacion = sistema.interpretar_resultado(nivel_alerta, categoria, vehiculos, velocidad)
            print(interpretacion)
        except Exception as e:
            print(f"Error en el cálculo: {e}")
    
    return sistema


if __name__ == "__main__":
    # Ejecutar ejemplo de uso
    sistema_trafico = ejemplo_uso()
    
    print("\n" + "=" * 50)
    print("Para visualizar las gráficas, ejecute:")
    print("sistema_trafico.visualizar_funciones_pertenencia()")
    print("plt.show()")
    print("=" * 50)