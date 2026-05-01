// Archivo main.js para el Sistema POS

// Función para mostrar tooltips de Bootstrap
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar todos los tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-cerrar alertas después de 5 segundos
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Filtro rápido para la tabla
    const searchInput = document.getElementById('searchArticulo');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const tableRows = document.querySelectorAll('tbody tr');
            
            tableRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                const isMatch = text.includes(searchTerm);
                row.style.display = isMatch ? '' : 'none';
            });
        });
    }

    // Animación simple para la tarjeta de login
    const loginCard = document.querySelector('.card-login');
    if (loginCard) {
        loginCard.style.opacity = '0';
        loginCard.style.transform = 'translateY(20px)';
        loginCard.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        setTimeout(function() {
            loginCard.style.opacity = '1';
            loginCard.style.transform = 'translateY(0)';
        }, 100);
    }

    // Manejar la edición del perfil
    const editBtn = document.querySelector('.edit-profile-btn');
    const cancelBtn = document.querySelector('.cancel-edit-btn');
    const viewMode = document.querySelector('.view-mode');
    const editMode = document.querySelector('.edit-mode');
    
    if (editBtn && cancelBtn && viewMode && editMode) {
        editBtn.addEventListener('click', function() {
            viewMode.style.display = 'none';
            editMode.style.display = 'block';
            this.style.display = 'none';
        });
        
        cancelBtn.addEventListener('click', function() {
            viewMode.style.display = 'block';
            editMode.style.display = 'none';
            editBtn.style.display = 'inline-block';
        });
    }
});

// Función para confirmar eliminación
function confirmarEliminacion(event, mensaje) {
    if (!confirm(mensaje || '¿Está seguro de que desea eliminar este elemento?')) {
        event.preventDefault();
        return false;
    }
    return true;
}

// Función para actualizar el contador de caracteres en textareas
function actualizarContador(textareaId, contadorId, maxLength) {
    const textarea = document.getElementById(textareaId);
    const contador = document.getElementById(contadorId);
    
    if (textarea && contador) {
        textarea.addEventListener('input', function() {
            const caracteresRestantes = maxLength - this.value.length;
            contador.textContent = caracteresRestantes;
            
            if (caracteresRestantes < 20) {
                contador.classList.add('text-danger');
            } else {
                contador.classList.remove('text-danger');
            }
        });
    }
}

// Función para validar formularios
function validarFormulario(formId) {
    const form = document.getElementById(formId);
    
    if (form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        });
    }
}
