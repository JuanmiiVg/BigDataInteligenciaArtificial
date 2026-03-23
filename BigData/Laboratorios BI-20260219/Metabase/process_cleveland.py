#!/usr/bin/env python3
"""
Script para convertir cleveland.data a formato CSV
Dataset: Cleveland Heart Disease
"""

import pandas as pd
import numpy as np

# Nombres de las columnas según la documentación del dataset Cleveland
columns = [
    'id', 'ccf', 'age', 'sex', 'painloc', 'painexer', 'relrest',
    'pncaden', 'cp', 'trestbps', 'htn', 'chol', 'smoke', 'cigs', 'years',
    'fbs', 'dm', 'famhist', 'restecg', 'ekgmo', 'ekgday', 'ekgyr',
    'dig', 'prop', 'nitr', 'pro', 'diuretic', 'proto', 'thaldur',
    'thaltime', 'met', 'thalach', 'thalrest', 'tpeakbps', 'tpeakbpd',
    'dummy', 'trestbpd', 'exang', 'xhypo', 'oldpeak', 'slope', 'rldv5',
    'rldv5e', 'ca', 'restckm', 'exerckm', 'restef', 'restwm',
    'exeref', 'exerwm', 'thal', 'thalsev', 'thalpul', 'earlobe',
    'cmo', 'cday', 'cyr', 'num', 'lmt', 'ladprox', 'laddist',
    'diag', 'cxmain', 'ramus', 'om1', 'om2', 'rcaprox', 'rcadist',
    'lvx1', 'lvx2', 'lvx3', 'lvx4', 'lvf', 'cathef', 'junk', 'name'
]

def process_cleveland_data(file_path):
    """
    Procesa el archivo cleveland.data y lo convierte a DataFrame
    """
    records = []
    current_record = []
    
    try:
        # Intentar diferentes codificaciones
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        content = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.readlines()
                print(f"Archivo leído exitosamente con codificación: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print("No se pudo leer el archivo con ninguna codificación")
            return None
        
        for line in content:
            line = line.strip()
            if not line:
                continue
                
            # Dividir la línea por espacios
            values = line.split()
            current_record.extend(values)
            
            # Si encontramos 'name', es el final de un registro
            if 'name' in values:
                # Remover 'name' del final
                if current_record[-1] == 'name':
                    current_record = current_record[:-1]
                
                # Asegurar que tenemos el número correcto de columnas
                if len(current_record) >= 75:  # Número esperado de columnas
                    records.append(current_record[:75])  # Tomar solo las primeras 75
                
                current_record = []
        
        print(f"Procesados {len(records)} registros")
        
        if records:
            # Crear DataFrame con las columnas más importantes para BI
            # Seleccionar solo las columnas más relevantes para el análisis
            important_cols = [
                'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
                'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'num'
            ]
            
            # Crear DataFrame simple con las principales variables
            simple_data = []
            for record in records:
                if len(record) >= 56:  # Asegurar que tenemos datos suficientes
                    simple_record = {
                        'patient_id': len(simple_data) + 1,
                        'age': int(float(record[2])) if record[2] != '-9' else None,
                        'sex': int(float(record[3])) if record[3] != '-9' else None,
                        'chest_pain_type': int(float(record[8])) if record[8] != '-9' else None,
                        'resting_bp': int(float(record[9])) if record[9] != '-9' else None,
                        'cholesterol': int(float(record[11])) if record[11] != '-9' else None,
                        'fasting_blood_sugar': int(float(record[15])) if record[15] != '-9' else None,
                        'max_heart_rate': int(float(record[31])) if record[31] != '-9' else None,
                        'exercise_angina': int(float(record[37])) if record[37] != '-9' else None,
                        'st_depression': float(record[39]) if record[39] != '-9' else None,
                        'heart_disease': int(float(record[57])) if len(record) > 57 and record[57] != '-9' else 0
                    }
                    simple_data.append(simple_record)
            
            return pd.DataFrame(simple_data)
        else:
            print("No se pudieron procesar los registros")
            return None
            
    except Exception as e:
        print(f"Error procesando el archivo: {e}")
        return None

# Procesar el archivo
if __name__ == "__main__":
    df = process_cleveland_data('cleveland.data')
    
    if df is not None:
        # Limpiar datos
        df = df.dropna(subset=['age', 'sex'])  # Eliminar registros sin edad o sexo
        
        # Crear categorías más descriptivas
        df['sex_desc'] = df['sex'].map({0: 'Female', 1: 'Male'})
        df['chest_pain_desc'] = df['chest_pain_type'].map({
            1: 'Typical Angina', 
            2: 'Atypical Angina', 
            3: 'Non-Anginal Pain', 
            4: 'Asymptomatic'
        })
        df['has_heart_disease'] = (df['heart_disease'] > 0).astype(int)
        df['age_group'] = pd.cut(df['age'], 
                                bins=[0, 40, 50, 60, 70, 100], 
                                labels=['<40', '40-50', '50-60', '60-70', '70+'])
        
        # Guardar como CSV
        df.to_csv('cleveland_heart_disease.csv', index=False)
        print(f"Archivo CSV creado con {len(df)} registros")
        print("\nPrimeras filas:")
        print(df.head())
        print(f"\nColumnas disponibles: {list(df.columns)}")
        
    else:
        print("No se pudo procesar el archivo")