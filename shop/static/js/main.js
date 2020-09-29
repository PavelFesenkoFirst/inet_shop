let result;
let a;
if (a < 5) {
    result = true;
} else if (a < 10) {
    result = 'unexpected';
} else {
    result = false;
}

result = (a < 5) ? true :
    (a < 10) ? 'unexpected' :
    false;

// 1
function summ (a, b) {
    return a + b
}

function func () {
    confirm('some qs?');
    alert('qwe');
    let ans = prompt('qqqqq', 'qwe');
}

// switch (value) {
//     case 'some': {
//         ...
//         break
//     }
//     case 'two': {
//         ...
//     }
//     default {
//         ...
//     }
// }

// // 2
// let summ = function (a, b) {return a + b}

// // 3
// let summ = (a, b) => a + b;

// summ(1, 2);


// ============================================================================

// text()
// val()
// addClass('btn-primary')
// removeClass()
// attr('disabled', true)
// append('<button></button>')
// html()

function showNextPage (page='http://localhost:8000/api/v1/product/all/?page=2') {
    console.log('its working');
    $('#nextPage').text('Waiting...');
    $('#nextPage').attr('disabled', true);

    // делаем GET запрос на url в переменно page
    // так же можно использовать $.get(page).done(data => {console.log(data);})
    // так же можно использовать $.getJSON(page, data => {console.log(data);})
    $.ajax(page)
        .done(data => {
            console.log(data);
            // получаем ответ от DRF и добавляем все товары из data.results на страницу
            for (let item of data.results) {
                $('#products').append(`
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="card h-100">
                        <a href="${item.link}">
                            <img class="card-img-top" src="/static/img/no_img.png" alt="${item.title}">
                        </a>
                        <div class="card-body">
                            <h4 class="card-title">
                                <a href="${item.link}">${item.title}</a>
                            </h4>
                            <h5>
                                ${item.actual_price} грн
                            </h5>
                            <p class="card-text">${item.description}</p>
                        </div>
                        <form class="card-footer" method="POST">
                            <button class="btn btn-success">Купить</button>
                            <button type="submit" class="btn btn-warning">В корзину</button>
                        </form>
                    </div>
                </div>
                `)
            }

            if (data.next) {
                $('#nextPage').text('Show more');
                $('#nextPage').attr('disabled', false);
                $('#nextPage').attr('onclick', `showNextPage(page='${data.next}');`);
            } else {
                $('#nextPage').remove();
            }
        })
}

$('#loginBtn').click(event => {
    event.preventDefault();  // отключаем валидацию и отправку формы с помощью HTML

    $('#login-error').text('');
    $('input').removeClass('is-invalid');

    let username = $('#username').val();
    let password = $('#password').val();
    let csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

    if (username && password) {
        // $.ajax({
        //     url: 'url',
        //     data: {username: username, password: password}
        // }).done()

        $.post('/users/login/', data={
            username: username,
            password: password,
            csrfmiddlewaretoken: csrftoken,
        })
        .done(data => {
            // $('#login').modal('toggle')
            // $('#login').modal('show')
            $('#login').modal('hide');

            $('button.login-modal').remove();
            $('button.register-modal').remove();
            $('#navbarResponsive').append('<a href="/users/profile/" class="btn btn-primary my-2 my-sm-0 ml-auto">Личный кабинет</a>');
            $('#navbarResponsive').append('<a href="/users/logout/" class="btn btn-danger my-2 my-sm-0 ml-sm-2">Выйти</a>');
        })
        .fail(xhr => {
            console.log(xhr.responseJSON);
            $('#login-error').text(xhr.responseJSON.__all__[0]);
            $('#username').addClass('is-invalid');
            $('#password').addClass('is-invalid');
        })

    } else {
        $('#login-error').text('error');
        $('#username').addClass('is-invalid');
        $('#password').addClass('is-invalid');
    }

})
