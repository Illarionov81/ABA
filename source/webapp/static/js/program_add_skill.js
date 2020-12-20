function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

async function makeRequest(url, method = 'GET', data = undefined) {
    let opts = {method, headers: {}};

    if (!csrfSafeMethod(method))
        opts.headers['X-CSRFToken'] = getCookie('csrftoken');

    if (data) {
        opts.headers['Content-Type'] = 'application/json';
        opts.body = JSON.stringify(data);
    }

    let response = await fetch(url, opts);

    if (response.ok) {  // нормальный ответ
        return response;
    } else {            // ошибка
        let error = new Error(response.statusText);
        error.response = response;
        throw error;
    }
}

function add_new_input_goal(){
    const modal_body = document.getElementById("add_new_goal");
    const input = document.createElement("input")
    input.innerHTML = '<input name ="add_goal" placeholder="Добавить цель">'
    console.log(input);
    modal_body.appendChild(input)
}

async function open_modal(event){
    event.preventDefault()
    $("#exampleModal").modal("show")

    let id = event.target.getAttribute("data-id")
    let url = event.target.getAttribute("href");
    console.log(id)
    console.log(url)
    const button = document.getElementById('save')
    const add_new_goal = document.getElementById('add_new_goal')
    add_new_goal.onclick = (e) => {
        e.preventDefault()
        const input = document.createElement("input")
        input.setAttribute("name", "add_goal")
        input.setAttribute("placeholder", "Добавить цель")
        add_new_goal.after(input)
    }
    button.onclick =  async (e) => {
        e.preventDefault()
        let modal_body = document.getElementById("modal_body")
        // let ggg = [...(modal_body.getElementsByClassName("add_goal"))]
        // console.log(ggg);
        event.target.style.backgroundColor = 'red'
        let add_creteria = document.getElementById("add_creteria")
        let add_creteria_value = add_creteria.value
        let add_goal = [...(modal_body.getElementsByTagName("input"))]
        let goals = []
        add_goal.forEach( (el) => {
            if (el.value !== add_creteria_value){
                goals.push(el.value)
            }
        })
        // console.log(goals);
        try {
            await makeRequest(url, 'POST', {'id': id, 'add_creteria': add_creteria_value, 'goals': goals});

            document.getElementById("add_creteria").value = ""
            const main_goal = document.getElementById("add_goal")
            main_goal.value = ""
            add_goal.forEach((el)=>{
                if (el !== main_goal && el !== add_creteria){
                    el.remove()
                }
            })
            $("#exampleModal").modal("hide")
        }
        catch (error) {
            console.log(error);
        }
    }
}

