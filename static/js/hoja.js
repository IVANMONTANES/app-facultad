// ------------------------------------ SECCION RELOJ EN TIEMPO REAL ---------------------------------------- //

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



// ------------------------------------------ SECCION CAMBIO DE UNIDAD DE TIEMPO ----------------------------------------- //
function obtenerSegundoFormato(minutos){
    horas = Math.floor(minutos / 60);
    minutos = minutos % 60;
    return `${horas}h ${minutos}mins`;
}

// evento que espera que sea cargue el dom (arbol de nodos) //
document.addEventListener("DOMContentLoaded", () => {
    // obtenemos los elementos con el atributo data-min //
    let elementos = document.querySelectorAll("[data-mins]");

    for(let elemento of elementos){
        elemento.addEventListener("click",(event)=> {
            let elementoActual = event.currentTarget;
            let minutos = parseInt(elementoActual.dataset.mins);

            if (elementoActual.dataset.formato === "1"){
                
                let nuevoFormato = obtenerSegundoFormato(minutos);

                // actualizamos el contenido //
                // verificamos si es la media //
                if(elementoActual.hasAttribute("data-media")){
                    elementoActual.querySelector("span").textContent = "Los ultimos 7 dias estudio un total de: " + nuevoFormato;
                }else{
                    spans = elementoActual.querySelectorAll("span");
                    spans[1].textContent = nuevoFormato;
                }

                
                

                // actualizamos el estado //
                elementoActual.setAttribute("data-formato","2");
            }else{

                // actualizamos el contenido //
                // verificamos si es la media //
                if(elementoActual.hasAttribute("data-media")){
                    elementoActual.querySelector("span").textContent = "Los ultimos 7 dias estudio un total de: " + minutos + "mins";
                }else{
                    spans = elementoActual.querySelectorAll("span");
                    spans[1].textContent = minutos + "mins";
                }

                // actualizamos el estado //
                elementoActual.setAttribute("data-formato","1");
            }
        })
    }
})