function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

async function makeRequest(url, method='GET', data=undefined) {
    let opts = {method, headers: {}};
    if (!csrfSafeMethod(method))
        opts.headers['X-CSRFToken'] = getCookie('csrftoken');

    if (data) {
        opts.headers['Content-Type'] = 'application/json';
        opts.body = JSON.stringify(data);
        console.log(opts.body);
    }
    let response = await fetch(url, opts);
    if (response.ok) {  // нормальный ответ
        return response.json();
    }
    else {            // ошибка
        let error = new Error(response.statusText);
        error.response = response;
        throw error;
    }
}

async function ChoiceCategory(event) {
    event.preventDefault()
    let SkillBox = event.target;
    const AllSkillBox = document.getElementsByClassName('box_category');
    console.log(SkillBox)
    const Code = SkillBox.id
    console.log(Code)
    for (let i=0; i<AllSkillBox.length; i++){
        AllSkillBox[i].style.display = '';
        if (AllSkillBox[i].id !== Code){
            AllSkillBox[i].style.display = 'none';
            }
        }
    }
