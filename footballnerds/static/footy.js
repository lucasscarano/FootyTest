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

function addPlayer(playerName){
    fetch('/validate_club/', {
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
        } else {
            alert("There's no clubs in common between the players.");
        }
    })
}

function createPlayerCard(data){
    let container = document.getElementById("players-list");

    let card = document.createElement("div");
    let club_container = document.createElement("div")

    card.classList.add("player-card");
    card.innerHTML = `<img src="${data.player.player_photo_url}" alt="Foto"> <p>${data.player.name}</p>`;

    club_container.classList.add("club-container");

    data.player.clubs.forEach(club => {
        let connection = document.createElement("div");

        connection.classList.add("club-connection");
        connection.innerHTML = `<img src="${club[1]}" alt="Escudo"><p>${club[0]}</p>`;
        club_container.appendChild(connection);
    });

    container.prepend(club_container);
    container.prepend(card);

    container.scrollTop = 0;
}