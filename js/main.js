// Inicializar el cliente de Supabase
const supabaseUrl = 'https://szficrcajedijgqysomg.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN6ZmljcmNhamVkaWpncXlzb21nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY3Nzg2MDIsImV4cCI6MjA1MjM1NDYwMn0.CBd0mEGK5WcBoY84A1iDsvpd6CobZnaN0k2lXX6sgWk';
const supabase = window.supabase.createClient(supabaseUrl, supabaseKey);

console.log('Versión actualizada del código - v4');

// Función para convertir URL de Google Drive en URL directa
function convertirUrlGoogleDrive(url) {
    if (!url) return '';
    
    console.log('URL original:', url);
    
    // Extraer ID del archivo
    let fileId = null;
    
    // Formato: https://drive.google.com/file/d/YOUR_FILE_ID/view
    const match = url.match(/\/file\/d\/(.*?)(\/|$)/);
    if (match) {
        fileId = match[1];
        console.log('ID del archivo encontrado:', fileId);
        
        // Construir URL para previsualización
        const embedUrl = `https://drive.google.com/file/d/${fileId}/preview`;
        console.log('URL de previsualización:', embedUrl);
        
        return embedUrl;
    }
    
    console.log('No se pudo extraer el ID del archivo');
    return url;
}

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
    
    // Convertir la URL de Google Drive y crear un iframe
    const fotoUrl = convertirUrlGoogleDrive(trabajador.foto_url);
    console.log('URL de foto convertida:', fotoUrl);
    
    const fotoContainer = document.getElementById('foto-trabajador');
    fotoContainer.style.display = 'none'; // Ocultar la imagen original
    
    // Crear contenedor para el iframe
    const iframeContainer = document.createElement('div');
    iframeContainer.style.width = '150px';
    iframeContainer.style.height = '150px';
    iframeContainer.style.borderRadius = '50%';
    iframeContainer.style.overflow = 'hidden';
    iframeContainer.style.position = 'relative';
    iframeContainer.style.margin = '0 auto';
    iframeContainer.style.border = '3px solid #007bff';
    iframeContainer.style.boxShadow = '0 0 10px rgba(0, 123, 255, 0.2)';
    
    // Crear y mostrar el iframe
    const iframe = document.createElement('iframe');
    iframe.src = fotoUrl;
    iframe.style.width = '100%';
    iframe.style.height = '100%';
    iframe.style.border = 'none';
    iframe.style.position = 'absolute';
    iframe.style.top = '50%';
    iframe.style.left = '50%';
    iframe.style.transform = 'translate(-50%, -50%) scale(1.5)';
    iframe.style.backgroundColor = 'transparent';
    
    // Agregar iframe al contenedor
    iframeContainer.appendChild(iframe);
    
    // Insertar el contenedor después de la imagen original
    fotoContainer.parentNode.insertBefore(iframeContainer, fotoContainer.nextSibling);
    
    document.getElementById('nombre').textContent = trabajador.nombre;
    document.getElementById('cedula').textContent = `C.I.: ${trabajador.cedula}`;
    document.getElementById('ubicacion').textContent = `Ubicación: ${trabajador.ubicacion || 'No especificada'}`;
    
    // Formatear la fecha correctamente
    const fecha = new Date(trabajador.fecha_ingreso);
    // Formatear manualmente la fecha en DD/MM/YYYY
    const dia = fecha.getUTCDate().toString().padStart(2, '0');
    const mes = (fecha.getUTCMonth() + 1).toString().padStart(2, '0');
    const año = fecha.getUTCFullYear();
    document.getElementById('fecha-ingreso').textContent = `Fecha de Ingreso: ${dia}/${mes}/${año}`;
    
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