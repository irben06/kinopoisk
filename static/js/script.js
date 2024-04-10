
// Add star rating
// Получаем значение рейтинга из локального хранилища при загрузке страницы
document.addEventListener("DOMContentLoaded", function() {
    const storedRating = localStorage.getItem('userRating');
    if (storedRating) {
        document.querySelector(`input[value="${storedRating}"]`).checked = true;
    }
});

// Обработчик события change для формы рейтинга
const ratingForm = document.querySelector('form[name=rating]');

ratingForm.addEventListener("change", function (e) {
    // Получаем данные из формы
    const data = new FormData(this);
    const selectedRating = data.get('star');
    
    // Сохраняем выбранный рейтинг в локальное хранилище
    localStorage.setItem('userRating', selectedRating);
    
    // Отправляем данные на сервер
    fetch(`${this.action}`, {
        method: 'POST',
        body: data
    })
    .then(response => {
        if (response.ok) {
            alert("Рейтинг установлен");
        } else {
            throw new Error("Ошибка при установке рейтинга");
        }
    })
    .catch(error => {
        alert(error.message);
    });
});