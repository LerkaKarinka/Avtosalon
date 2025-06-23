function formatDateForMySQL(date) {
    const pad = (num) => num.toString().padStart(2, '0');
    
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ` +
           `${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
  }

function auto_status_change(id){
    let dataToSend = {
        "type" : "Статус",
        "data" : "Уважаемый клиент, Ваш автомобиль готов 🚓 \u2764 " + id,
        "datetime": formatDateForMySQL(new Date()),
        "klient_id": id
    }
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataToSend)
    };
    fetch("/event/add",options)
    .then(data => {
        console.log('Success:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });   
}