   document.addEventListener('DOMContentLoaded', (event) => {
       var socket = io();

       socket.on('connect', function() {
           console.log('Connected to server');
       });

       socket.on('disconnect', function() {
           console.log('Disconnected from server');
       });

       socket.on('update', function(data) {
           console.log('Update received:', data);
           var notification = document.getElementById('notification');
           var alertMessage = document.getElementById('alert-message');
           var timerGif = document.getElementById('timer-gif');

           // Обновляем сообщение
           alertMessage.textContent = data.message;
           // Показываем уведомление
           notification.classList.remove('hidden-notification');

           // Скрываем уведомление с таймером через 5 секунд и перезагружаем страницу
           setTimeout(() => {
               notification.classList.add('hidden-notification');
               location.reload();
           }, 5000);
       });
   });