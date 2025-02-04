import qrcode
from supabase import create_client
import os

# Configuración de Supabase
supabase_url = "https://szficrcajedijgqysomg.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN6ZmljcmNhamVkaWpncXlzb21nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY3Nzg2MDIsImV4cCI6MjA1MjM1NDYwMn0.CBd0mEGK5WcBoY84A1iDsvpd6CobZnaN0k2lXX6sgWk"
supabase = create_client(supabase_url, supabase_key)

def generar_qr_para_trabajador(trabajador):
    try:
        # Crear el código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Limpiar la cédula de todo excepto números para el QR
        cedula_limpia = ''.join(filter(str.isdigit, trabajador['cedula']))
        print(f"Generando QR para cédula: {cedula_limpia}")
        
        # URL que contendrá el QR (usando el subdominio)
        qr_data = f"https://qr.gestionhbc.com?qr={cedula_limpia}"
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Crear la imagen QR
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Guardar temporalmente
        temp_path = f"temp_qr_{cedula_limpia}.png"
        qr_image.save(temp_path)
        print(f"QR guardado temporalmente como: {temp_path}")
        
        # Subir nuevo QR
        with open(temp_path, "rb") as f:
            file_path = f"{cedula_limpia}.png"
            # Intentar eliminar el archivo existente si existe
            try:
                supabase.storage.from_("codigos-qr").remove([file_path])
            except:
                pass
            # Subir el nuevo archivo
            supabase.storage.from_("codigos-qr").upload(file_path, f)
        
        # Obtener URL pública
        qr_url = supabase.storage.from_("codigos-qr").get_public_url(file_path)
        print(f"QR subido a Supabase: {qr_url}")
        
        # Eliminar archivo temporal
        os.remove(temp_path)
        
        return qr_url
    except Exception as e:
        print(f"Error generando QR: {str(e)}")
        raise e

def procesar_trabajadores_sin_qr():
    try:
        # Obtener trabajadores sin QR
        response = supabase.table("trabajadores").select("*").is_("qr_imagen_url", "null").execute()
        print(f"Encontrados {len(response.data)} trabajadores sin QR")
        
        for trabajador in response.data:
            print(f"\nProcesando trabajador: {trabajador['nombre']}")
            # Generar y subir QR
            qr_url = generar_qr_para_trabajador(trabajador)
            
            # Actualizar el registro con la URL del QR
            supabase.table("trabajadores").update({"qr_imagen_url": qr_url}).eq("id", trabajador["id"]).execute()
            
            print(f"✓ QR generado y actualizado para: {trabajador['nombre']}")
    except Exception as e:
        print(f"Error en el proceso: {str(e)}")
        raise e

if __name__ == "__main__":
    print("Procesando trabajadores sin QR...")
    procesar_trabajadores_sin_qr()