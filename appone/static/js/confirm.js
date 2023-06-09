const btnsEli = document.querySelectorAll('.btnEli');

(function() {


    btnsEli.forEach(btn => {
        btn.addEventListener('click',function(e) {
            e.preventDefault();
            Swal.fire({
                title: "¿Desea eliminar ?",
                icon: "warning",
                showCancelButton: true,
                confirmButtonText: "Eliminar",
                confirmButtonColor:"#d33",
                backdrop: true,
                showLoaderOnConfirm: true,
                preConfirm: () => {
                    location.href = e.target.href
                },
                allowOutsideClick: () => false,
                allowEscapeKey: () => false,
            });
        });
    });
})();