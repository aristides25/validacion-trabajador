from supabase import create_client
import requests
import os
import shutil

# Configuración de Supabase
supabase_url = "https://szficrcajedijgqysomg.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN6ZmljcmNhamVkaWpncXlzb21nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY3Nzg2MDIsImV4cCI6MjA1MjM1NDYwMn0.CBd0mEGK5WcBoY84A1iDsvpd6CobZnaN0k2lXX6sgWk"
supabase = create_client(supabase_url, supabase_key)

def descargar_imagen(url, ruta):
    try:
        print(f"Intentando descargar: {url}")  # Debug
        response = requests.get(url)
        if response.status_code == 200:
            with open(ruta, 'wb') as f:
                f.write(response.content)
            print(f"Descarga exitosa: {ruta}")  # Debug
            return True
        else:
            print(f"Error HTTP {response.status_code}")  # Debug
            return False
    except Exception as e:
        print(f"Error descargando {url}: {e}")
        return False

def descargar_imagenes():
    # Crear carpetas
    if os.path.exists('imagenes'):
        shutil.rmtree('imagenes')
    os.makedirs('imagenes/fotos', exist_ok=True)
    os.makedirs('imagenes/qr', exist_ok=True)
    
    # Obtener trabajadores
    response = supabase.table("trabajadores").select("*").execute()
    
    # Descargar imágenes
    for trabajador in response.data:
        cedula = trabajador['cedula'].replace('-', '').replace('V', '')
        nombre_limpio = trabajador['nombre'].replace(' ', '_').lower()
        
        # Descargar foto
        if trabajador.get('foto_url'):
            foto_path = f"imagenes/fotos/{nombre_limpio}_{cedula}.jpg"
            if descargar_imagen(trabajador['foto_url'], foto_path):
                print(f"Foto descargada: {trabajador['nombre']} - {cedula}")
            
        # Descargar QR desde el bucket
        try:
            qr_filename = f"{trabajador['codigo_qr']}.png"
            qr_url = supabase.storage.from_('codigos-qr').create_signed_url(qr_filename, 60)
            if qr_url:
                qr_url = qr_url['signedURL']
                print(f"URL del QR: {qr_url}")
                
                qr_path = f"imagenes/qr/{nombre_limpio}_{cedula}.png"
                if descargar_imagen(qr_url, qr_path):
                    print(f"QR descargado: {trabajador['nombre']} - {cedula}")
                else:
                    print(f"Error descargando QR para {trabajador['nombre']}")
        except Exception as e:
            print(f"Error procesando QR de {cedula}: {e}")

    print("\nImágenes descargadas en carpeta 'imagenes':")
    print("- Fotos en carpeta 'fotos'")
    print("- QRs en carpeta 'qr'")

if __name__ == "__main__":
    descargar_imagenes() 