// obtenemos la fecha actual //
function obtenerFecha(){
    let fechaActual = new Date();

    let fechaFormateada = fechaActual.toLocaleDateString("es-AR",{
        weekday: "long",
        day: "2-digit",
        month:"long",
        year:"numeric"
    });


    return fechaFormateada;

}


// obtenemos la hora actual //
function obtenerHora(){
    let fechaActual = new Date();

    // vamos a usar la funcion padStart que agrega caracteres al inicio de una cadena hasta llegar a cierta longitud //
    let horas = String(fechaActual.getHours()).padStart(2,"0")
    let minutos = String(fechaActual.getMinutes()).padStart(2,"0")
    let segundos = String(fechaActual.getSeconds()).padStart(2,"0")

    // devolvemos la hora //
    return `${horas}:${minutos}:${segundos}`;
}

function actualizarHora(){
    // obtenemos la fecha actual //
    fecha = obtenerFecha();
    // obtenemos la hora actual //
    hora = obtenerHora();

    // obtenemos los divs //
    let fecha_div = document.getElementById("fecha");
    let hora_div = document.getElementById("hora");

    // actualizamos dinamicamente la fecha y hora //
    fecha_div.textContent = fecha;
    hora_div.textContent = hora;
    
    return null;
}

actualizarHora()
setInterval(actualizarHora,1000);