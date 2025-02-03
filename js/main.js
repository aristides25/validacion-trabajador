// Inicializar el cliente de Supabase
const supabaseUrl = 'https://szficrcajedijgqysomg.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN6ZmljcmNhamVkaWpncXlzb21nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY3Nzg2MDIsImV4cCI6MjA1MjM1NDYwMn0.CBd0mEGK5WcBoY84A1iDsvpd6CobZnaN0k2lXX6sgWk';
const supabase = window.supabase.createClient(supabaseUrl, supabaseKey);

console.log('Versión actualizada del código - v2');

document.addEventListener('DOMContentLoaded', async () => {
    const params = new URLSearchParams(window.location.search);
    const codigoQR = params.get('qr');

    if (!codigoQR) {
        mostrarError('Código QR no proporcionado');
        return;
    }

    try {
        console.log('Código QR recibido:', codigoQR);
        
        // Formatear la cédula con guiones (X-XXX-XXXX)
        const formatearCedula = (numeros) => {
            if (numeros.length !== 8) return numeros;
            return `${numeros.slice(0,1)}-${numeros.slice(1,4)}-${numeros.slice(4)}`;
        };
        
        const cedulaFormateada = formatearCedula(codigoQR);
        console.log('Buscando trabajador con cédula:', cedulaFormateada);
        
        // Construir la consulta manualmente para verificar
        const query = supabase
            .from('trabajadores')
            .select('*')
            .eq('cedula', cedulaFormateada);
            
        console.log('URL de la consulta:', query.url);
        
        let { data, error } = await query;
            
        if (error) {
            console.error('Error de Supabase:', error);
            throw error;
        }
            
        console.log('Resultado de búsqueda:', { data });
        
        if (data && data.length > 0) {
            console.log('¡Trabajador encontrado!', data[0]);
            mostrarTrabajador(data[0]);
        } else {
            console.log('No se encontró el trabajador');
            mostrarError('Trabajador no encontrado');
        }
        
    } catch (err) {
        console.error('Error detallado:', err);
        mostrarError('Error al verificar el trabajador');
    }
});

function mostrarTrabajador(trabajador) {
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
    
    const infoDiv = document.getElementById('trabajador-info');
    infoDiv.classList.remove('hidden');
    
    console.log('Mostrando datos del trabajador:', trabajador);
    
    document.getElementById('foto-trabajador').src = trabajador.foto_url;
    document.getElementById('nombre').textContent = trabajador.nombre;
    document.getElementById('cedula').textContent = `C.I.: ${trabajador.cedula}`;
    document.getElementById('ubicacion').textContent = `Ubicación: ${trabajador.ubicacion || 'No especificada'}`;
    document.getElementById('fecha-ingreso').textContent = `Fecha de Ingreso: ${new Date(trabajador.fecha_ingreso).toLocaleDateString()}`;
    if (trabajador.puesto) {
        document.getElementById('puesto').textContent = `Puesto: ${trabajador.puesto}`;
    }
}

function mostrarError(mensaje) {
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('trabajador-info').classList.add('hidden');
    
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = mensaje;
    errorDiv.classList.remove('hidden');
    
    console.error('Error mostrado al usuario:', mensaje);
} 