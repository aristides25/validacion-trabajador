import pandas as pd
from supabase import create_client
import os
import requests
import shutil
import zipfile
from datetime import datetime

# Configuración de Supabase
supabase_url = "https://chqfivjyzmiytdnbfvna.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNocWZpdmp5em1peXRkbmJmdm5hIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkwMzk4MTgsImV4cCI6MjA1NDYxNTgxOH0.ytiUkjfQOn2214qN4iO8kkcZILGkoJguz1x5Uk-n2p8"
supabase = create_client(supabase_url, supabase_key)

def crear_directorios():
    """Crea los directorios necesarios para las imágenes"""
    os.makedirs('temp/imagenes/fotos', exist_ok=True)
    os.makedirs('temp/imagenes/qr', exist_ok=True)
    print("✓ Directorios temporales creados")

def convertir_url_google_drive(url):
    """Convierte URL de Google Drive en URL directa para descarga"""
    if not url:
        return None
    
    # Extraer ID del archivo
    file_id = None
    if '/file/d/' in url:
        file_id = url.split('/file/d/')[1].split('/')[0]
    
    if file_id:
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return url

def descargar_foto(url, id_foto, nombre, cedula):
    """Descarga la foto de perfil y la guarda con el ID como nombre"""
    if not url:
        return None
        
    # Convertir URL de Google Drive
    url_descarga = convertir_url_google_drive(url)
    if not url_descarga:
        return None
        
    try:
        # Asegurar que el nombre del archivo tenga la extensión .jpg
        nombre_archivo = f'{id_foto}.jpg'
        ruta_foto = f'temp/imagenes/fotos/{nombre_archivo}'
        
        # Descargar la foto
        response = requests.get(url_descarga, stream=True)
        if response.status_code == 200:
            with open(ruta_foto, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            
            # Verificar que el archivo se creó correctamente
            if os.path.exists(ruta_foto):
                print(f"✓ Foto de perfil descargada para {nombre} ({cedula})")
                print(f"  Archivo guardado como: {nombre_archivo}")
                # Verificar que la extensión sea visible
                if not ruta_foto.lower().endswith('.jpg'):
                    print("  ⚠ Advertencia: El archivo podría no tener la extensión .jpg visible")
                return nombre_archivo
            else:
                print(f"✗ Error: El archivo no se guardó correctamente para {nombre} ({cedula})")
                return None
        else:
            print(f"✗ Error descargando foto de perfil para {nombre} ({cedula}): {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Error procesando foto de perfil para {nombre} ({cedula}): {str(e)}")
        return None

def copiar_qr(id_foto, nombre, cedula):
    """Copia el QR generado a la carpeta temporal"""
    try:
        # Ruta del QR generado
        ruta_origen = f'codigos_qr/{id_foto}.png'
        ruta_destino = f'temp/imagenes/qr/{id_foto}.png'
        
        if os.path.exists(ruta_origen):
            shutil.copy2(ruta_origen, ruta_destino)
            print(f"✓ QR copiado para {nombre} ({cedula})")
            return True
        else:
            print(f"✗ QR no encontrado para {nombre} ({cedula})")
            return False
    except Exception as e:
        print(f"✗ Error copiando QR: {str(e)}")
        return False

def crear_readme():
    """Crea un archivo README con instrucciones"""
    readme_contenido = '''Instrucciones para Asure ID
=======================

1. Extraiga todo el contenido de este ZIP en una carpeta de su elección
   (por ejemplo: C:\\Carnets)

2. En Asure ID:
   a. Importe el archivo datos_carnets.csv
   b. Configure los enlaces de campos:
      - Enlace cada columna del CSV con su campo correspondiente en la plantilla
      - Asegúrese de enlazar 'id_foto' con 'identificador'

   c. En la plantilla del carnet, configure la foto:
      - En "Propiedades de la foto", active "Utilizar un origen de datos de carpeta"
      - En "Origen de datos", seleccione la carpeta "imagenes/fotos" donde extrajo el ZIP
      - En campo clave seleccione "identificador"

   d. Configure el campo del código QR de la misma manera:
      - En sus propiedades, active "Utilizar un origen de datos de carpeta"
      - En "Origen de datos", seleccione la carpeta "imagenes/qr"
      - En campo clave seleccione "identificador"

3. Las imágenes se encuentran en las siguientes carpetas:
   - Fotos: imagenes/fotos/
   - QRs: imagenes/qr/
   - Cada imagen tiene un ID único como nombre (ejemplo: 1.jpg, 1.png)
   - Los IDs coinciden con la columna 'id_foto' del CSV

Nota: Es importante mantener la estructura de carpetas tal como está:
- datos_carnets.csv
- imagenes/
  ├── fotos/
  │   └── (archivos .jpg)
  └── qr/
      └── (archivos .png)
'''
    
    with open('temp/README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_contenido)
    print("✓ Archivo README creado")

def crear_zip():
    """Crea un archivo ZIP con todos los archivos necesarios"""
    # Nombre del archivo ZIP con fecha
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_nombre = f'carnets_azure_{fecha}.zip'
    
    try:
        with zipfile.ZipFile(zip_nombre, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Añadir CSV y README
            zipf.write('temp/datos_carnets.csv', 'datos_carnets.csv')
            zipf.write('temp/README.txt', 'README.txt')
            
            # Añadir carpeta de fotos
            for carpeta, subcarpetas, archivos in os.walk('temp/imagenes'):
                for archivo in archivos:
                    ruta_completa = os.path.join(carpeta, archivo)
                    ruta_en_zip = os.path.join('imagenes', os.path.relpath(ruta_completa, 'temp/imagenes'))
                    print(f"Añadiendo al ZIP: {ruta_en_zip}")
                    zipf.write(ruta_completa, ruta_en_zip)
        
        print(f"\n✓ Archivo ZIP creado: {zip_nombre}")
        return zip_nombre
    except Exception as e:
        print(f"✗ Error creando ZIP: {str(e)}")
        return None

def limpiar_temporales():
    """Elimina los archivos temporales"""
    try:
        shutil.rmtree('temp')
        print("✓ Archivos temporales eliminados")
    except Exception as e:
        print(f"✗ Error eliminando temporales: {str(e)}")

def exportar_csv():
    """Exporta los datos de trabajadores pendientes a CSV y descarga las fotos"""
    print("\nIniciando exportación de datos y descarga de imágenes...")
    
    # Crear directorios necesarios
    crear_directorios()
    
    # Obtener trabajadores pendientes o por actualizar
    response = supabase.table("trabajadores").select("*").in_("estado_carnet", ["pendiente", "actualizar"]).order("nombre").execute()
    df = pd.DataFrame(response.data)
    
    if len(df) == 0:
        print("No hay trabajadores pendientes para exportar")
        return
        
    print(f"\nEncontrados {len(df)} trabajadores pendientes de carnet")
    
    # Generar IDs únicos
    df['id_foto'] = range(1, len(df) + 1)
    
    # Procesar fotos y QRs
    rutas_fotos = []
    qrs_copiados = []
    for index, row in df.iterrows():
        print(f"\nProcesando trabajador: {row['nombre']}")
        # Descargar foto de perfil usando el ID
        ruta_foto = descargar_foto(row.get('foto_url'), row['id_foto'], row['nombre'], row['cedula'])
        rutas_fotos.append(ruta_foto if ruta_foto else '')
        
        # Copiar QR usando el mismo ID
        qr_copiado = copiar_qr(row['id_foto'], row['nombre'], row['cedula'])
        qrs_copiados.append(qr_copiado)
    
    # Convertir formato de fecha de YYYY-MM-DD a DD-MM-YYYY
    df['fecha_ingreso'] = pd.to_datetime(df['fecha_ingreso']).dt.strftime('%d-%m-%Y')
    
    # Seleccionar datos para el CSV
    datos_carnets = df[[
        'id_foto',
        'nombre',
        'cedula',
        'fecha_ingreso',
        'ubicacion',
        'puesto'
    ]]
    
    # Guardar CSV en carpeta temporal
    datos_carnets.to_csv('temp/datos_carnets.csv', index=False, encoding='cp1252')
    print("\n✓ CSV generado temporalmente")
    
    # Crear archivo README
    crear_readme()
    
    # Crear ZIP con todos los archivos
    zip_generado = crear_zip()
    
    if zip_generado:
        print(f"\nInstrucciones:")
        print("1. Transfiere el archivo ZIP a la computadora con Asure ID")
        print("2. Extrae el ZIP en una carpeta de tu elección")
        print("3. En Asure ID:")
        print("   - Importa el archivo datos_carnets.csv")
        print("   - En la opción 'Importación de archivos de imágenes':")
        print("     * Para las fotos: selecciona la carpeta 'imagenes/fotos'")
        print("     * Para los QRs: selecciona la carpeta 'imagenes/qr'")
        print("     * En ambos casos, usa la columna 'id_foto' como referencia")
    
    # Limpiar archivos temporales
    limpiar_temporales()

if __name__ == "__main__":
    exportar_csv() 