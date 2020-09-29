// при загрузке страницы делаем GET запрос для получения товаров 1й страницы
// так же можно использовать $.get(url, (data) => {console.log(data);})
// так же можно использовать $.ajax(url).done((data) => {console.log(data);})
// так же можно использовать $.ajax({url: url}).done((data) => {console.log(data);})
$.getJSON('/api/v1/product/all/', (data) => {
    console.log(data);  // результат, который отдает DRF
    let product_list = data.results;  // создаем переменную со списком товаров
    let next = data.next;  // переменная с ссылкой на следующую страницу

    let app = new Vue({  // инициализируем экземпляр Vue js
        el: '#app',  // id главного <div id="app"></div> в котором будет работать vue js
        delimiters: ['[[', ']]'],  // заменяем объявление контекста в шаблоне с {{}} на [[]], что не конфликтовать с Django
        data: {  // все ключи в data будут доступны в шаблоне
            product_list: product_list,
            next: next
        },
        methods: {  // в этом словаре описывает нужные методы
            show_more: () => {  // эта функция срабатывает при нажатии на кнопку Show more
                $.getJSON(app.next, (data) => {  // делается GET запрос по URL, который прислал DRF
                    console.log(data);  // результат, который отдает DRF
                    app.product_list = app.product_list.concat(data.results);  // добавляем полученный список продуктов к имеющимся
                    // app.product_list = [...app.product_list, ...data.results];  // второй вариант объединения списков (более новый синтаксис)
                    app.next = data.next;  // обновляем ссылку на следующую страницу
                })
            },
            add: (id) => {  // эта функция добавляет продукт в корзину
                let csrftoken = $('input[name="csrfmiddlewaretoken"]').val();  // получаем значение csrftoken

                // 1 вариант POST запроса
                $.post(`/add/${id}/`, {csrfmiddlewaretoken: csrftoken})  // отправляем POST запрос, в data={} передаем csrftoken
                    .done(() => console.log('done'));

                // 2 вариант POST запроса
                // $.ajax(`/add/${id}/`, {
                //     method: 'POST',
                //     data: {csrfmiddlewaretoken: csrftoken}
                // }).done(() => console.log('done'));

                // // 3 вариант
                // $.ajax({
                //     url: `/add/${id}/`,
                //     method: 'POST',
                //     data: {csrfmiddlewaretoken: csrftoken}
                // }).done(() => console.log('done'));
            }
        }
    })
});
