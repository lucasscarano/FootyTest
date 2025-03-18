new Autocomplete('#autocomplete', {
    search : input => {
        const url = `/search/?players=${input}`
        return new Promise(resolve => {
            if (input.length < 3) {
                return resolve([])
            }
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    resolve(data.data)
                })
        })
    },
    autoSelect: true,
    onSubmit : result => {
        addPlayer(result);
        const input = document.querySelector('#autocomplete .autocomplete-input');
        input.value = "";
    }

})

function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0,name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
}
let csrftoken = getToken('csrftoken')

let timer;

function addPlayer(playerName){
    fetch('/validate-club/', {
        method: 'POST',
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body: JSON.stringify({playerName: playerName})
    })
    .then((response) => {
        return response.json();
    })
    .then(data => {
        if (data.status === 200) {
            createPlayerCard(data);
            startTimer()
        } else {
            notification(data.message);
        }
    })
}

function createPlayerCard(data){
    const container = document.getElementById("players-list");

    const card = document.createElement("div");
    const club_container = document.createElement("div")

    card.classList.add("player-card");
    card.innerHTML = `<img src="${data.player.player_photo_url}" alt="Foto">
                      <div class="name">
                          <img src="${data.player.flag_url}" alt="Bandera">  
                          <p>${data.player.player_name}</p>
                      </div>`;

    club_container.classList.add("club-container");

    data.player.clubs.forEach(club => {
        const connection = document.createElement("div");

        connection.classList.add("club-connection");
        connection.innerHTML = `<img src="${club[1]}" alt="Escudo"><p>${club[0]}</p>`;
        club_container.appendChild(connection);
    });

    container.prepend(club_container);
    container.prepend(card);

    container.scrollTop = 0;
}

function startTimer(){
    clearInterval(timer);
    let timeLeft = 30;
    document.getElementById("timerValue").innerText = `${timeLeft}`;

    timer = setInterval(() => {
        timeLeft--;
        document.getElementById("timerValue").innerText = `${timeLeft}`;

        if (timeLeft <= 0){
            clearInterval(timer);
            gameOver();
        }
    }, 1000)
}

function gameOver(){
    endGame();
    const input = document.querySelector('#autocomplete .autocomplete-input');
    input.disabled = true;
    const container = document.getElementById('container');
    container.style.setProperty('-webkit-filter', 'blur(5px)')

    const body = document.body;
    const message = document.createElement("div");
    message.classList.add("message");
    message.innerHTML = `<p>Game Over</p>
                         <button class="restart-btn">Play Again</button>`;

    body.append(message);

    document.querySelector('.restart-btn').addEventListener('click', () => {
        location.reload();
    });

}

function notification(message){
    const container = document.getElementById("notification-container");
    if (container.classList.length > 0){
        // Removes notifications if it's called again while animation is still going.
        container.textContent = '';
    }
    const notification = document.createElement('div');
    notification.classList.add('notification');
    notification.innerHTML = `<p>${message}</p>`;
    container.appendChild(notification);

    notification.addEventListener('animationend', (e) => {
        if (e.animationName === 'slideUp'){
            notification.remove();
        }
    })
}

function endGame() {
    fetch('/end-game/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            }
        })
    .then((response) => {
        return response.json();
    })
}
