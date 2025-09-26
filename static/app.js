const socket = io();
const form = document.getElementById('complaintForm');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    
    // POPRAWIONE: obsługa checkbox - dodaj wartość tylko jeśli zaznaczony
    const haveCode = document.getElementById('haveCode').checked;
    if (!haveCode) {
        formData.delete('code'); // Usuń kod produktu jeśli checkbox nie zaznaczony
    }

    try {
        const response = await fetch('/api/complaints', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            document.getElementById('message').innerHTML =
                'Reklamacja wysłana! Numer: ' + result.id;
            form.reset();
        } else {
            document.getElementById('message').innerHTML =
                'Błąd: ' + result.error;
        }
    } catch (error) {
        console.error('Błąd:', error);
        document.getElementById('message').innerHTML =
            'Błąd połączenia: ' + error.message;
    }
});

// POPRAWIONE: pokazuj/ukryj pole kodu w zależności od checkbox
document.getElementById('haveCode').addEventListener('change', function() {
    const codeField = document.querySelector('input[name="code"]');
    codeField.style.display = this.checked ? 'block' : 'none';
    if (!this.checked) {
        codeField.value = ''; // Wyczyść pole gdy ukryte
    }
});

// Ukryj pole kodu na starcie
document.querySelector('input[name="code"]').style.display = 'none';