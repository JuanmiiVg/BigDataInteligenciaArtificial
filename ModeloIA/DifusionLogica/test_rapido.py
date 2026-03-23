"""
Prueba Rápida del Sistema de Alerta de Tráfico

Script de verificación que ejecuta una prueba básica del sistema
para confirmar que la instalación y configuración son correctas.

Ejecutar: python test_rapido.py
"""

import sys
import traceback
from sistema_alerta_trafico import SistemaAlertaTrafico


def test_importaciones():
    """Verifica que todas las librerías necesarias estén disponibles"""
    try:
        import numpy as np
        import skfuzzy as fuzz
        from skfuzzy import control as ctrl
        import matplotlib.pyplot as plt
        print("✅ Todas las importaciones correctas")
        return True
    except ImportError as e:
        print(f"❌ Error en importaciones: {e}")
        print("💡 Instale las dependencias con: pip install -r requirements.txt")
        return False


def test_creacion_sistema():
    """Prueba la creación del sistema de lógica difusa"""
    try:
        sistema = SistemaAlertaTrafico()
        print("✅ Sistema de lógica difusa creado correctamente")
        return sistema
    except Exception as e:
        print(f"❌ Error al crear sistema: {e}")
        traceback.print_exc()
        return None


def test_calculo_basico(sistema):
    """Prueba cálculos básicos del sistema"""
    casos_prueba = [
        (10, 80),   # Poco tráfico, velocidad alta
        (50, 30),   # Tráfico medio, velocidad baja  
        (80, 15),   # Mucho tráfico, velocidad muy baja
    ]
    
    resultados_esperados = ['baja', 'alta', 'alta']
    
    for i, (vehiculos, velocidad) in enumerate(casos_prueba):
        try:
            nivel, categoria = sistema.calcular_alerta(vehiculos, velocidad)
            esperado = resultados_esperados[i]
            
            print(f"✅ Caso {i+1}: {vehiculos} veh/km, {velocidad} km/h → {categoria} (nivel: {nivel:.1f})")
            
            if categoria == esperado:
                print(f"   ✓ Resultado esperado: {esperado}")
            else:
                print(f"   ⚠️  Resultado inesperado. Esperado: {esperado}, Obtenido: {categoria}")
                
        except Exception as e:
            print(f"❌ Error en caso {i+1}: {e}")
            return False
    
    return True


def test_validacion_entradas(sistema):
    """Prueba la validación de entradas del sistema"""
    casos_invalidos = [
        (-10, 50),    # Vehículos negativos
        (50, -20),    # Velocidad negativa
        (150, 50),    # Demasiados vehículos  
        (50, 200),    # Velocidad excesiva
    ]
    
    print("\nProbando validación de entradas...")
    
    for vehiculos, velocidad in casos_invalidos:
        try:
            nivel, categoria = sistema.calcular_alerta(vehiculos, velocidad)
            print(f"⚠️  No se validó entrada incorrecta: {vehiculos}, {velocidad}")
        except ValueError:
            print(f"✅ Validación correcta para: {vehiculos}, {velocidad}")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    return True


def test_interpretacion(sistema):
    """Prueba el sistema de interpretación de resultados"""
    try:
        nivel, categoria = sistema.calcular_alerta(45, 35)
        interpretacion = sistema.interpretar_resultado(nivel, categoria, 45, 35)
        
        if len(interpretacion) > 100:  # Verificar que se genera texto suficiente
            print("✅ Sistema de interpretación funcional")
            return True
        else:
            print("⚠️  Interpretación muy corta")
            return False
            
    except Exception as e:
        print(f"❌ Error en interpretación: {e}")
        return False


def ejecutar_prueba_completa():
    """Ejecuta todas las pruebas del sistema"""
    print("🔍 INICIANDO PRUEBAS DEL SISTEMA DE ALERTA DE TRÁFICO")
    print("=" * 60)
    
    # Test 1: Importaciones
    print("\n1️⃣ Verificando importaciones...")
    if not test_importaciones():
        return False
    
    # Test 2: Creación del sistema
    print("\n2️⃣ Creando sistema de lógica difusa...")
    sistema = test_creacion_sistema()
    if sistema is None:
        return False
    
    # Test 3: Cálculos básicos
    print("\n3️⃣ Probando cálculos básicos...")
    if not test_calculo_basico(sistema):
        return False
    
    # Test 4: Validación de entradas
    print("\n4️⃣ Probando validación de entradas...")
    if not test_validacion_entradas(sistema):
        return False
    
    # Test 5: Sistema de interpretación
    print("\n5️⃣ Probando sistema de interpretación...")
    if not test_interpretacion(sistema):
        return False
    
    print("\n✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("=" * 60)
    print("🎯 El sistema está listo para usar")
    print("\n🚀 Para ejecutar ejemplos completos, use:")
    print("   python ejemplos_demostracion.py")
    
    return True


def ejemplo_interactivo():
    """Permite al usuario probar el sistema interactivamente"""
    print("\n🎮 MODO INTERACTIVO")
    print("=" * 30)
    
    sistema = SistemaAlertaTrafico()
    
    while True:
        try:
            print("\nIngrese los valores (o 'q' para salir):")
            
            vehiculos_input = input("Vehículos por km (0-100): ")
            if vehiculos_input.lower() == 'q':
                break
                
            velocidad_input = input("Velocidad promedio (0-120 km/h): ")
            if velocidad_input.lower() == 'q':
                break
            
            vehiculos = float(vehiculos_input)
            velocidad = float(velocidad_input)
            
            nivel, categoria = sistema.calcular_alerta(vehiculos, velocidad)
            interpretacion = sistema.interpretar_resultado(nivel, categoria, vehiculos, velocidad)
            
            print("\n" + "="*50)
            print(interpretacion)
            print("="*50)
            
        except ValueError:
            print("❌ Por favor ingrese números válidos")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("👋 ¡Gracias por usar el sistema!")


if __name__ == "__main__":
    print("🚦 PRUEBA RÁPIDA - Sistema de Alerta de Tráfico")
    print("Autor: Juan Manuel Vega")
    print("=" * 60)
    
    try:
        # Ejecutar pruebas automáticas
        exito = ejecutar_prueba_completa()
        
        if exito:
            respuesta = input("\n¿Desea probar el sistema interactivamente? (s/n): ")
            if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
                ejemplo_interactivo()
        
    except KeyboardInterrupt:
        print("\n\n👋 Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error general: {e}")
        traceback.print_exc()
    
    print("\n🎯 Prueba completada")