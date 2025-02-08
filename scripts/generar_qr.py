import qrcode
from supabase import create_client
import os

# Configuración de Supabase
supabase_url = "https://szficrcajedijgqysomg.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN6ZmljcmNhamVkaWpncXlzb21nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY3Nzg2MDIsImV4cCI6MjA1MjM1NDYwMn0.CBd0mEGK5WcBoY84A1iDsvpd6CobZnaN0k2lXX6sgWk"
supabase = create_client(supabase_url, supabase_key)

def crear_directorio_qr():
    """Crea el directorio para guardar los códigos QR"""
    os.makedirs('codigos_qr', exist_ok=True)
    print("✓ Directorio de QRs creado")

def generar_qr_para_trabajador(trabajador, id_foto):
    """Genera y guarda el código QR para un trabajador"""
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
        print(f"Generando QR para: {trabajador['nombre']} (cédula: {trabajador['cedula']})")
        
        # URL que contendrá el QR (usando el subdominio y solo la cédula)
        qr_data = f"https://qr.gestionhbc.com?qr={cedula_limpia}"
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Crear la imagen QR
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Guardar el QR usando el ID
        nombre_archivo = f"{id_foto}.png"
        ruta_qr = f"codigos_qr/{nombre_archivo}"
        qr_image.save(ruta_qr)
        print(f"✓ QR guardado como: {ruta_qr}")
        
        return True
    except Exception as e:
        print(f"✗ Error generando QR: {str(e)}")
        return False

def generar_todos_los_qr():
    """Genera códigos QR para todos los trabajadores pendientes en la base de datos"""
    try:
        # Crear directorio para QRs
        crear_directorio_qr()
        
        # Obtener trabajadores pendientes o por actualizar
        response = supabase.table("trabajadores").select("*").in_("estado_carnet", ["pendiente", "actualizar"]).order("nombre").execute()
        total_trabajadores = len(response.data)
        print(f"\nEncontrados {total_trabajadores} trabajadores pendientes de generar QR")
        
        # Contador de QRs generados
        qrs_generados = 0
        
        # Generar QR para cada trabajador con ID secuencial
        for index, trabajador in enumerate(response.data, start=1):
            if generar_qr_para_trabajador(trabajador, index):
                qrs_generados += 1
                
        print(f"\nResumen:")
        print(f"✓ QRs generados exitosamente: {qrs_generados}")
        print(f"✗ QRs con error: {total_trabajadores - qrs_generados}")
        print(f"\nLos códigos QR han sido guardados en la carpeta 'codigos_qr'")
                
    except Exception as e:
        print(f"Error en el proceso: {str(e)}")
        raise e

if __name__ == "__main__":
    print("Iniciando generación de códigos QR...")
    generar_todos_los_qr()