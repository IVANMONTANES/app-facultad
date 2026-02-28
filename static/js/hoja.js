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
    /* 
            -------------- FORMATOS DISPONIBLES -------------
            1: Lunes, 27 de febrero de 2026
            2: 27/02/2026
            3: 27-02-2026
            4: 02/27/2026
            5: 02-27-2026
        
    */

    // fechas en diferentes formatos //
    let fecha_actual = new Date();
    // formato 1 //
    let formato1 = fecha_actual.toLocaleDateString("es-AR",{
        weekday: "long",
        day: "2-digit",
        month: "long",
        year: "numeric"
    });

    // formato 2 //
    let formato2 = fecha_actual.toLocaleDateString("es-AR",{
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
    });

    // formato 3 //
    let arreglo_formato3 = formato2.split("/");
    let formato3 = arreglo_formato3.join("-");
        
    // formato 4 //
    let formato4 = fecha_actual.toLocaleDateString("en-US",{
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
    });

    // formato 5 //
    let arreglo_formato5 = formato4.split("/");
    let formato5 = arreglo_formato5.join("-");

    // objeto literal con los diferentes formatos //
    const formatos = {
        "1": formato1,
        "2": formato2,
        "3": formato3,
        "4": formato4,
        "5": formato5,
    };

    // obtenemos los divs //
    let fecha_div = document.getElementById("fecha");
    let hora_div = document.getElementById("hora");

    // obtenemos el formato en el que se encuentra actualmente //
    formato_actual = fecha_div.dataset.formato;

    // actualizamos dinamicamente la fecha y hora //
    fecha_div.textContent = formatos[formato_actual];
    hora_div.textContent = obtenerHora();
    
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

// ------------------------------------------ SECCION CAMBIO DE RELOJ ----------------------------------------- //
document.addEventListener("DOMContentLoaded", () => {
    // obtenemos el div que almacena la fecha //
    let fecha = document.getElementById("fecha");

    // escuchamos el evento click //
    fecha.addEventListener("click",(event) => {
        

        // objeto literal tipo diccionario que indica cual es el siguiente formato //
        const siguiente_formato = {
            "1": "2",
            "2": "3",
            "3": "4",
            "4": "5",
            "5":"1",
        };

        // obtenemos el formato actual //
        let formato_actual = fecha.dataset.formato;
        // obtenemos el nuevo formato //
        let nuevo_formato = siguiente_formato[formato_actual];
        // actualizamos el atributo //
        fecha.setAttribute("data-formato",nuevo_formato);
        // llamamos a la funcion para actualizar la hora //
        actualizarHora();
    })
})