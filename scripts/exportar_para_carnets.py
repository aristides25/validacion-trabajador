import pandas as pd
from supabase import create_client
import unidecode
import requests
import os
import shutil

# Configuración de Supabase
supabase_url = "https://szficrcajedijgqysomg.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN6ZmljcmNhamVkaWpncXlzb21nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY3Nzg2MDIsImV4cCI6MjA1MjM1NDYwMn0.CBd0mEGK5WcBoY84A1iDsvpd6CobZnaN0k2lXX6sgWk"
supabase = create_client(supabase_url, supabase_key)

def limpiar_texto(texto):
    return unidecode.unidecode(str(texto))

def descargar_imagen(url, ruta):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(ruta, 'wb') as f:
                f.write(response.content)
            return True
    except:
        return False

def exportar_datos_carnets():
    # Crear carpeta principal
    if os.path.exists('exportacion_carnets'):
        shutil.rmtree('exportacion_carnets')
    os.makedirs('exportacion_carnets/fotos', exist_ok=True)
    os.makedirs('exportacion_carnets/qr', exist_ok=True)
    
    # Obtener trabajadores
    response = supabase.table("trabajadores").select("*").execute()
    df = pd.DataFrame(response.data)
    
    # Limpiar tildes y descargar imágenes
    for index, row in df.iterrows():
        # Limpiar textos
        df.at[index, 'nombre'] = limpiar_texto(row['nombre'])
        df.at[index, 'cedula'] = limpiar_texto(row['cedula'])
        
        cedula = row['cedula'].replace('-', '').replace('V', '')
        
        # Descargar foto
        foto_path = f"exportacion_carnets/fotos/{cedula}.jpg"
        descargar_imagen(row['foto_url'], foto_path)
            
        # Descargar QR
        qr_path = f"exportacion_carnets/qr/{cedula}.png"
        descargar_imagen(row['qr_imagen_url'], qr_path)
    
    # Guardar CSV con datos básicos
    datos_carnets = df[[
        'nombre',
        'cedula',
        'fecha_ingreso',
        'valido_hasta'
    ]]
    
    datos_carnets.to_csv('exportacion_carnets/datos_carnets.csv', index=False, encoding='ascii')
    print("Exportación completada en carpeta 'exportacion_carnets':")
    print("- CSV con datos en datos_carnets.csv")
    print("- Fotos en carpeta 'fotos'")
    print("- QRs en carpeta 'qr'")

if __name__ == "__main__":
    exportar_datos_carnets() 