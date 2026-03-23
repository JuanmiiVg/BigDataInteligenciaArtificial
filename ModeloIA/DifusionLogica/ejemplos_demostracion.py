"""
Ejemplos y Demostraciones del Sistema de Alerta de Tráfico

Este archivo contiene ejemplos prácticos, visualizaciones y cases de estudio
para demostrar las capacidades del sistema de lógica difusa.

Autor: Juan Manuel Vega
Fecha: Febrero 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from sistema_alerta_trafico import SistemaAlertaTrafico


def ejemplo_basico():
    """Demostración básica del sistema"""
    print("🚦 EJEMPLO BÁSICO - Sistema de Alerta de Tráfico")
    print("=" * 60)
    
    # Crear sistema
    sistema = SistemaAlertaTrafico()
    
    # Evaluar una situación específica
    vehiculos = 55
    velocidad = 25
    
    print(f"\n📊 EVALUANDO SITUACIÓN:")
    print(f"• Vehículos por km: {vehiculos}")
    print(f"• Velocidad promedio: {velocidad} km/h")
    
    # Calcular alerta
    nivel, categoria = sistema.calcular_alerta(vehiculos, velocidad)
    
    # Mostrar resultado
    interpretacion = sistema.interpretar_resultado(nivel, categoria, vehiculos, velocidad)
    print(interpretacion)


def casos_estudio_detallados():
    """Casos de estudio con análisis detallado"""
    print("\n🔍 CASOS DE ESTUDIO DETALLADOS")
    print("=" * 60)
    
    sistema = SistemaAlertaTrafico()
    
    casos = [
        {
            'nombre': 'Hora Pico Matutina',
            'vehiculos': 75,
            'velocidad': 20,
            'contexto': 'Entrada a la ciudad durante hora pico'
        },
        {
            'nombre': 'Tráfico Nocturno',
            'vehiculos': 8,
            'velocidad': 85,
            'contexto': 'Autopista durante la madrugada'
        },
        {
            'nombre': 'Zona Escolar',
            'vehiculos': 35,
            'velocidad': 30,
            'contexto': 'Área residencial cerca de escuela'
        },
        {
            'nombre': 'Evento Deportivo',
            'velocidad': 10,
            'vehiculos': 90,
            'contexto': 'Salida de estadio después del partido'
        },
        {
            'nombre': 'Día Laboral Normal',
            'vehiculos': 42,
            'velocidad': 55,
            'contexto': 'Tráfico promedio en zona comercial'
        }
    ]
    
    for i, caso in enumerate(casos, 1):
        print(f"\n--- CASO {i}: {caso['nombre']} ---")
        print(f"Contexto: {caso['contexto']}")
        
        nivel, categoria = sistema.calcular_alerta(caso['vehiculos'], caso['velocidad'])
        print(f"\nResultado: {nivel:.2f}/10 - {categoria.upper()}")
        print(f"Vehículos: {caso['vehiculos']}/km | Velocidad: {caso['velocidad']} km/h")
        
        # Análisis específico
        if categoria == 'alta':
            print("⚠️  ACCIÓN REQUERIDA: Activar protocolos de emergencia")
        elif categoria == 'media':
            print("⚡ MONITOREO: Preparar medidas preventivas")
        else:
            print("✅ NORMAL: Mantener supervisión estándar")


def comparacion_con_reglas_discretas():
    """Comparación entre lógica difusa y reglas discretas"""
    print("\n⚖️  COMPARACIÓN: Lógica Difusa vs Reglas Discretas")
    print("=" * 70)
    
    sistema = SistemaAlertaTrafico()
    
    def reglas_discretas(vehiculos, velocidad):
        """Implementación simple de reglas discretas para comparación"""
        if vehiculos < 30 and velocidad > 50:
            return 2, 'baja'
        elif vehiculos < 30 and velocidad <= 50:
            return 4, 'media'
        elif 30 <= vehiculos <= 60 and velocidad > 50:
            return 3, 'baja'
        elif 30 <= vehiculos <= 60 and velocidad <= 50:
            return 6, 'media'
        elif vehiculos > 60 and velocidad > 30:
            return 7, 'alta'
        else:  # vehiculos > 60 and velocidad <= 30
            return 9, 'alta'
    
    # Casos límite para mostrar diferencias
    casos_limite = [
        (29, 51),  # Justo debajo del umbral
        (31, 49),  # Justo arriba del umbral
        (59, 31),  # Cerca del límite
        (61, 29),  # Cerca del límite
    ]
    
    print("\n📈 Casos en límites de umbrales:")
    print("Veh/km | Vel(km/h) | Difusa | Discreta | Diferencia")
    print("-" * 55)
    
    for vehiculos, velocidad in casos_limite:
        nivel_difuso, cat_difuso = sistema.calcular_alerta(vehiculos, velocidad)
        nivel_discreto, cat_discreto = reglas_discretas(vehiculos, velocidad)
        
        diferencia = abs(nivel_difuso - nivel_discreto)
        
        print(f"  {vehiculos:2d}   |   {velocidad:2d}    | {nivel_difuso:4.1f}   |   {nivel_discreto:1d}     |   {diferencia:4.1f}")
    
    print("\n💡 OBSERVACIONES:")
    print("• La lógica difusa proporciona transiciones más suaves")
    print("• Las reglas discretas generan saltos abruptos en los límites")
    print("• La lógica difusa refleja mejor la realidad gradual del tráfico")


def visualizacion_completa():
    """Genera todas las visualizaciones del sistema"""
    print("\n📊 GENERANDO VISUALIZACIONES...")
    print("=" * 50)
    
    sistema = SistemaAlertaTrafico()
    
    # Figura 1: Funciones de pertenencia
    print("• Creando gráfico de funciones de pertenencia...")
    fig1 = sistema.visualizar_funciones_pertenencia()
    fig1.suptitle('Funciones de Pertenencia - Sistema de Alerta de Tráfico', fontsize=14, fontweight='bold')
    
    # Figura 2: Superficie de control
    print("• Creando superficie de control 3D...")
    fig2, datos_superficie = sistema.superficie_control(num_puntos=30)
    
    # Figura 3: Mapa de calor
    print("• Creando mapa de calor...")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    
    vehiculos_mesh, velocidad_mesh, alerta_mesh = datos_superficie
    
    contour = ax3.contourf(vehiculos_mesh, velocidad_mesh, alerta_mesh, 
                          levels=20, cmap='RdYlGn_r')
    ax3.set_xlabel('Vehículos por km')
    ax3.set_ylabel('Velocidad promedio (km/h)')
    ax3.set_title('Mapa de Calor - Niveles de Alerta')
    
    # Añadir líneas de contorno
    contour_lines = ax3.contour(vehiculos_mesh, velocidad_mesh, alerta_mesh, 
                               levels=[3, 6], colors='white', linewidths=2, alpha=0.8)
    ax3.clabel(contour_lines, inline=True, fontsize=10, fmt='%1.0f')
    
    # Barra de colores y leyenda
    cbar = plt.colorbar(contour, ax=ax3)
    cbar.set_label('Nivel de Alerta')
    
    # Añadir puntos de referencia
    puntos_ref = [(10, 80, 'Fluido'), (45, 35, 'Congestionado'), (80, 15, 'Crítico')]
    for veh, vel, label in puntos_ref:
        ax3.plot(veh, vel, 'ko', markersize=8)
        ax3.annotate(label, (veh, vel), xytext=(5, 5), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.8))
    
    plt.tight_layout()
    
    print("• ✅ Todas las visualizaciones creadas exitosamente")
    print("• 🔍 Use plt.show() para mostrar los gráficos")
    
    return fig1, fig2, fig3


def simulacion_tiempo_real():
    """Simula el comportamiento del sistema en tiempo real"""
    print("\n🕐 SIMULACIÓN DE TIEMPO REAL")
    print("=" * 50)
    
    sistema = SistemaAlertaTrafico()
    
    # Simular 24 horas de tráfico (una lectura cada hora)
    horas = np.arange(0, 24)
    
    # Patrones realistas de tráfico durante el día
    # Basado en curvas típicas de tráfico urbano
    vehiculos_dia = 50 + 30 * (np.sin(2 * np.pi * (horas - 6) / 24) ** 2)  # Picos matutino y vespertino
    velocidad_dia = 60 - 25 * (np.sin(2 * np.pi * (horas - 6) / 24) ** 2)  # Velocidad inversa a densidad
    
    # Añadir algo de variabilidad aleatoria
    np.random.seed(42)
    vehiculos_dia += np.random.normal(0, 5, len(horas))
    velocidad_dia += np.random.normal(0, 8, len(horas))
    
    # Asegurar límites razonables
    vehiculos_dia = np.clip(vehiculos_dia, 5, 95)
    velocidad_dia = np.clip(velocidad_dia, 10, 100)
    
    # Calcular alertas
    alertas = []
    categorias = []
    
    for i in range(len(horas)):
        nivel, cat = sistema.calcular_alerta(vehiculos_dia[i], velocidad_dia[i])
        alertas.append(nivel)
        categorias.append(cat)
    
    # Mostrar resumen
    print("\n📅 RESUMEN DEL DÍA:")
    print("Hora | Veh/km | Vel(km/h) | Alerta | Categoría")
    print("-" * 50)
    
    for i in range(0, 24, 3):  # Mostrar cada 3 horas
        hora_str = f"{i:02d}:00"
        emoji = "🟢" if categorias[i] == 'baja' else "🟡" if categorias[i] == 'media' else "🔴"
        print(f"{hora_str} |  {vehiculos_dia[i]:4.0f}  |   {velocidad_dia[i]:4.0f}    | {alertas[i]:4.1f}  | {emoji} {categorias[i]}")
    
    # Estadísticas del día
    horas_criticas = sum(1 for cat in categorias if cat == 'alta')
    horas_moderadas = sum(1 for cat in categorias if cat == 'media')
    horas_normales = sum(1 for cat in categorias if cat == 'baja')
    
    print(f"\n📊 ESTADÍSTICAS DEL DÍA:")
    print(f"• Horas críticas (alerta alta): {horas_criticas}/24 ({horas_criticas/24*100:.0f}%)")
    print(f"• Horas moderadas (alerta media): {horas_moderadas}/24 ({horas_moderadas/24*100:.0f}%)")
    print(f"• Horas normales (alerta baja): {horas_normales}/24 ({horas_normales/24*100:.0f}%)")
    
    # Crear gráfico de la simulación
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
    
    # Gráfico 1: Vehículos
    ax1.plot(horas, vehiculos_dia, 'b-', linewidth=2, marker='o')
    ax1.set_ylabel('Vehículos/km')
    ax1.set_title('Simulación de Tráfico - 24 Horas')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 23)
    
    # Gráfico 2: Velocidad
    ax2.plot(horas, velocidad_dia, 'g-', linewidth=2, marker='s')
    ax2.set_ylabel('Velocidad (km/h)')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 23)
    
    # Gráfico 3: Alertas con colores
    colors = ['green' if cat == 'baja' else 'orange' if cat == 'media' else 'red' for cat in categorias]
    ax3.bar(horas, alertas, color=colors, alpha=0.7)
    ax3.set_ylabel('Nivel de Alerta')
    ax3.set_xlabel('Hora del día')
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(-0.5, 23.5)
    
    # Añadir líneas de referencia para niveles de alerta
    ax3.axhline(y=3, color='orange', linestyle='--', alpha=0.7, label='Umbral Media')
    ax3.axhline(y=6, color='red', linestyle='--', alpha=0.7, label='Umbral Alta')
    ax3.legend()
    
    # Ajustar etiquetas del eje x
    ax3.set_xticks(range(0, 24, 3))
    ax3.set_xticklabels([f"{i:02d}:00" for i in range(0, 24, 3)])
    
    plt.tight_layout()
    print("• 📈 Gráfico de simulación creado")
    
    return fig


def generar_reporte_completo():
    """Genera un reporte completo con todos los ejemplos"""
    print("\n📋 GENERANDO REPORTE COMPLETO DEL SISTEMA")
    print("=" * 70)
    
    # Ejecutar todos los ejemplos
    ejemplo_basico()
    casos_estudio_detallados()
    comparacion_con_reglas_discretas()
    
    # Generar visualizaciones
    fig1, fig2, fig3 = visualizacion_completa()
    fig4 = simulacion_tiempo_real()
    
    print(f"\n✅ REPORTE COMPLETO GENERADO")
    print("=" * 70)
    print("📁 Archivos disponibles:")
    print("• sistema_alerta_trafico.py - Código principal")
    print("• README.md - Documentación completa")
    print("• ejemplos_demostracion.py - Este archivo")
    print("\n📊 Visualizaciones creadas:")
    print("• Funciones de pertenencia")
    print("• Superficie de control 3D")
    print("• Mapa de calor de niveles de alerta") 
    print("• Simulación temporal de 24 horas")
    print("\n💡 Para visualizar los gráficos ejecute: plt.show()")
    
    return (fig1, fig2, fig3, fig4)


if __name__ == "__main__":
    # Menú interactivo
    print("🚦 SISTEMA DE ALERTA DE TRÁFICO - EJEMPLOS Y DEMOSTRACIONES")
    print("=" * 70)
    print("\nOpciones disponibles:")
    print("1. Ejemplo básico")
    print("2. Casos de estudio detallados")
    print("3. Comparación con reglas discretas")
    print("4. Generar visualizaciones")
    print("5. Simulación tiempo real")
    print("6. Reporte completo")
    print("0. Ejecutar todo automáticamente")
    
    try:
        opcion = input("\nSeleccione una opción (0-6): ").strip()
        
        if opcion == "1":
            ejemplo_basico()
        elif opcion == "2":
            casos_estudio_detallados()
        elif opcion == "3":
            comparacion_con_reglas_discretas()
        elif opcion == "4":
            visualizacion_completa()
            plt.show()
        elif opcion == "5":
            simulacion_tiempo_real()
            plt.show()
        elif opcion == "6":
            generar_reporte_completo()
            plt.show()
        elif opcion == "0":
            print("\n🚀 EJECUTANDO DEMOSTRACIÓN COMPLETA...")
            generar_reporte_completo()
            plt.show()
        else:
            print("❌ Opción no válida")
            
    except KeyboardInterrupt:
        print("\n\n👋 Demostración interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
    
    print("\n🎯 ¡Demostración completada!")