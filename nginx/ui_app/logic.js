window.addEventListener('load', function() {
    fetchAndDisplayTeamMembers();
});
// Funkcja pobierająca i wyświetlająca członków zespołu
function fetchAndDisplayTeamMembers() {
    // Pobierz listę członków zespołu z serwera
    fetch('http://localhost:8080/data', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })  // Analizuje odpowiedź jako JSON
    .then(data => {
        // Czyści bieżącą listę członków zespołu
        const teamMembersList = document.getElementById('team-members');
        teamMembersList.innerHTML = ''; // Czyści listę

        // Dodaj wszystkich członków zespołu na podstawie danych z serwera
        data.forEach((member) => {
            addTeamMember(member.first_name, member.last_name, member.role, member.id);
        });
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}


// Obsługa formularza dodawania członków zespołu
document.getElementById('team-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const formData = new FormData(this); // Towrzenie obiektu FormData z formularza
    // Konwertuje dane formularza na zwykły obiekt JavaScript
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    // Wyślij dane jako JSON do serwera
    fetch('http://localhost:8080/team', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data) // Konwertuj obiekt danych na JSON
    })
    .then(response => {
        if (response.ok) {
            // Ponowne pobranie i wyświetlanie listy członków po dodaniu
            fetchAndDisplayTeamMembers();
        } else {
            console.error('Failed to submit form:', response.statusText);
        }
        this.reset(); // Czyszczenie formularza
    })
    .catch(error => {
        console.error('Error submitting form:', error);
    });
});


// Funkcja dodająca członka zespołu do listy HTML
function addTeamMember(firstName, lastName, role, id) {
    const teamMembersList = document.getElementById('team-members');

    const listItem = document.createElement('li');
    listItem.classList.add('team-members-item');

    const info = document.createElement('div');
    info.innerHTML = `<p><strong>${firstName} ${lastName}</strong></p><p class='gray-text'>${role}</p>`;

    const deleteButton = document.createElement('button');
    deleteButton.classList.add('delete-button');
    deleteButton.innerHTML = '🗑️';

    // Obsługa przycisku usuwania członka zespołu
    deleteButton.addEventListener('click', function () {
        fetch(`http://localhost:8080/delete/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.ok) {
            // Ponownie pobierz i wyświetl listę członków po dodaniu                
            fetchAndDisplayTeamMembers();
            } else {
                console.error('Failed to delete member:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error deleting member:', error);
        });
    });

    listItem.appendChild(info);
    listItem.appendChild(deleteButton);
    teamMembersList.appendChild(listItem);
}
