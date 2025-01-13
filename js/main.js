const { createClient } = supabase;

const supabaseUrl = 'https://szficrcajedijgqysomg.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InN6ZmljcmNhamVkaWpncXlzb21nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY3Nzg2MDIsImV4cCI6MjA1MjM1NDYwMn0.CBd0mEGK5WcBoY84A1iDsvpd6CobZnaN0k2lXX6sgWk';
const supabase = createClient(supabaseUrl, supabaseKey);

document.addEventListener('DOMContentLoaded', async () => {
    const params = new URLSearchParams(window.location.search);
    const codigoQR = params.get('qr');

    if (!codigoQR) {
        mostrarError('Código QR no proporcionado');
        return;
    }

    try {
        console.log('Buscando trabajador con código:', codigoQR);
        const { data, error } = await supabase
            .from('trabajadores')
            .select('*')
            .eq('codigo_qr', codigoQR)
            .single();

        if (error) {
            console.error('Error de Supabase:', error);
            throw error;
        }

        if (data) {
            console.log('Trabajador encontrado:', data);
            mostrarTrabajador(data);
        } else {
            mostrarError('Trabajador no encontrado');
        }
    } catch (err) {
        console.error('Error general:', err);
        mostrarError('Error al verificar el trabajador');
    }
});

function mostrarTrabajador(trabajador) {
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('error').classList.add('hidden');
    
    const infoDiv = document.getElementById('trabajador-info');
    infoDiv.classList.remove('hidden');
    
    document.getElementById('foto-trabajador').src = trabajador.foto_url;
    document.getElementById('nombre').textContent = trabajador.nombre;
    document.getElementById('cedula').textContent = `C.I.: ${trabajador.cedula}`;
    document.getElementById('fecha-ingreso').textContent = `Fecha de Ingreso: ${new Date(trabajador.fecha_ingreso).toLocaleDateString()}`;
    document.getElementById('valido-hasta').textContent = `Válido hasta: ${new Date(trabajador.valido_hasta).toLocaleDateString()}`;
}

function mostrarError(mensaje) {
    document.getElementById('loading').classList.add('hidden');
    document.getElementById('trabajador-info').classList.add('hidden');
    
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = mensaje;
    errorDiv.classList.remove('hidden');
} 