from supabase import create_client

# Configuración de Supabase
supabase_url = "https://szficrcajedijgqysomg.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN6ZmljcmNhamVkaWpncXlzb21nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY3Nzg2MDIsImV4cCI6MjA1MjM1NDYwMn0.CBd0mEGK5WcBoY84A1iDsvpd6CobZnaN0k2lXX6sgWk"
supabase = create_client(supabase_url, supabase_key)

def limpiar_bucket():
    """Limpia todos los archivos del bucket de códigos QR"""
    try:
        response = supabase.storage.from_("codigos-qr").list()
        for file in response:
            supabase.storage.from_("codigos-qr").remove([file['name']])
        print("✓ Bucket de QRs limpiado exitosamente")
    except Exception as e:
        print(f"✗ Error al limpiar bucket: {e}")

def limpiar_urls_qr():
    """Limpia las URLs de QR en la tabla trabajadores"""
    try:
        supabase.table("trabajadores").update({"qr_imagen_url": None}).execute()
        print("✓ URLs de QR limpiadas exitosamente en la tabla trabajadores")
    except Exception as e:
        print(f"✗ Error al limpiar URLs de QR: {e}")

def formatear_cedulas():
    """Formatea las cédulas al formato correcto X-XXX-XXXX"""
    try:
        # Obtener todos los trabajadores
        response = supabase.table("trabajadores").select("*").execute()
        for trabajador in response.data:
            # Limpiar la cédula dejando solo números
            numeros = ''.join(filter(str.isdigit, trabajador['cedula']))
            if len(numeros) == 8:  # Verificar que tenga el largo correcto
                # Formatear al formato X-XXX-XXXX
                cedula_formateada = f"{numeros[0]}-{numeros[1:4]}-{numeros[4:]}"
                # Actualizar en la base de datos
                supabase.table("trabajadores").update(
                    {"cedula": cedula_formateada}
                ).eq("id", trabajador["id"]).execute()
        print("✓ Cédulas formateadas exitosamente")
    except Exception as e:
        print(f"✗ Error al formatear cédulas: {e}")

def limpiar_todo():
    """Ejecuta todas las funciones de limpieza"""
    print("\nIniciando proceso de limpieza...")
    limpiar_bucket()
    limpiar_urls_qr()
    formatear_cedulas()
    print("\nProceso de limpieza completado")

if __name__ == "__main__":
    opcion = input("""
Seleccione una opción:
1. Limpiar solo bucket de QRs
2. Limpiar solo URLs de QR en tabla trabajadores
3. Formatear cédulas
4. Ejecutar todas las limpiezas
Opción (1-4): """)
    
    if opcion == "1":
        limpiar_bucket()
    elif opcion == "2":
        limpiar_urls_qr()
    elif opcion == "3":
        formatear_cedulas()
    elif opcion == "4":
        limpiar_todo()
    else:
        print("Opción no válida") 