import pandas as pd
from supabase import create_client

# Configuración de Supabase
supabase_url = "https://szficrcajedijgqysomg.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN6ZmljcmNhamVkaWpncXlzb21nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY3Nzg2MDIsImV4cCI6MjA1MjM1NDYwMn0.CBd0mEGK5WcBoY84A1iDsvpd6CobZnaN0k2lXX6sgWk"
supabase = create_client(supabase_url, supabase_key)

def importar_trabajadores():
    # Leer el archivo Excel
    try:
        df = pd.read_excel('trabajadores.xlsx')
        print(f"Encontrados {len(df)} trabajadores en el Excel")
        
        # Procesar cada trabajador
        for index, row in df.iterrows():
            # Generar código QR único basado en la cédula
            codigo_qr = f"T{row['cedula'].replace('-', '').replace('V', '')}"
            
            # Preparar datos del trabajador
            trabajador = {
                'nombre': row['nombre'],
                'cedula': row['cedula'],
                'fecha_ingreso': row['fecha_ingreso'].strftime('%Y-%m-%d'),
                'valido_hasta': row['valido_hasta'].strftime('%Y-%m-%d'),
                'codigo_qr': codigo_qr,
                'foto_url': row['foto_url'],
                'ubicacion': row['ubicacion'],
                'puesto': row['puesto'],
                'activo': True
            }
            
            # Insertar en Supabase
            response = supabase.table('trabajadores').insert(trabajador).execute()
            print(f"Importado: {trabajador['nombre']} - {trabajador['cedula']}")
            
        print("\nImportación completada exitosamente")
        
    except Exception as e:
        print(f"Error en la importación: {e}")

if __name__ == "__main__":
    importar_trabajadores() 