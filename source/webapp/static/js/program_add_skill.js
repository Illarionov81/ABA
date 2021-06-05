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

let colorDict = {}

async function pr_skill(event) {
    event.preventDefault();
    let skill_lvl = event.target;
    let id = skill_lvl.id;
    let url = skill_lvl.href;
    console.log(skill_lvl)
    console.log(id)
    console.log(url)
    // let code = document.getElementById('codes')
    // let row = skill_lvl.parentElement  //ряд
    // let colorCode = row.childNodes[1].textContent  //ключ(код)
    //

    // colorDict[colorCode] = choice
    // console.log(colorDict)
    // Object.keys(colorDict).forEach(function (key) {
    //     if (key === colorCode && colorDict[key].style.backgroundColor === 'lightgreen') {
    //         colorDict[colorCode].style.backgroundColor = 'white'
    //     }
    //     else if(key === colorCode && colorDict[key].style.backgroundColor !== 'lightgreen'){
    //         for (let i = 0; i < row.childElementCount - 1; i++) {
    //             row.querySelectorAll('a')[i].style.backgroundColor = 'white'
    //         }
    //         colorDict[colorCode].style.backgroundColor = 'lightgreen'
    //     }
    // });

    try {
        let response = await makeRequest(url, 'POST', {'id': id});
    } catch (error) {
        console.log(error);
    }
}
