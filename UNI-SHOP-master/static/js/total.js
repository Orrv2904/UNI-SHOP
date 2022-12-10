cantidad=document.querySelector("#cantidad")
precio=document.querySelector("#precio")
total = document.querySelector("#preciototal")

async function request() {
    const res = await cantidad.value;
    console.log(res)
    Total = parseFloat(precio.textContent) * parseInt(res);
    console.log(Total)
    total.textContent = "C$" +Total;

}

function bounce(callback, wait) {
    let timerId;
    return(...args) => {
        clearTimeout(timerId);
        timerId = setTimeout(() => {
            callback(...args);
        }, wait);
        };
    }

cantidad.addEventListener('keyup', bounce(() => {
    if(!(cantidad.value == "")) {
        request()
    }
}, 1000));

