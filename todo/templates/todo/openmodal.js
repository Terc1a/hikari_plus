document.addEventListener('DOMContentLoaded', function () {
    function initModals() {
        // открытие
        document.querySelectorAll('.task-button').forEach(button => {
            button.addEventListener('click', function () {
                const modalId = this.getAttribute('data-modal-id');
                const modal = document.getElementById(modalId);
                if (modal) {
                    modal.style.display = 'block';
                    document.body.style.overflow = 'hidden';
                }
            });
        });

        // крестик
        document.querySelectorAll('.modal-close').forEach(closeBtn => {
            closeBtn.addEventListener('click', function () {
                const modal = this.closest('.modal-overlay');
                if (modal) {
                    modal.style.display = 'none';
                    document.body.style.overflow = '';
                }
            });
        });

        // оверлей
        document.querySelectorAll('.modal-overlay').forEach(modal => {
            modal.addEventListener('click', function (event) {
                if (event.target === this) {
                    this.style.display = 'none';
                    document.body.style.overflow = '';
                }
            });
        });

        // по Escape
        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape') {
                document.querySelectorAll('.modal-overlay').forEach(modal => {
                    modal.style.display = 'none';
                    document.body.style.overflow = '';
                });
            }
        });
    }

    if (typeof CKEDITOR !== 'undefined') {
        for (var instance in CKEDITOR.instances) {
            if (CKEDITOR.instances.hasOwnProperty(instance)) {
                CKEDITOR.instances[instance].config.versionCheck = false;
            }
        }
    }

    initModals();
});