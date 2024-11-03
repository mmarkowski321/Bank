async function login() {
    const userId = document.getElementById('login_user_id').value;
    const pin = document.getElementById('login_pin').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, pin: pin })
    });

    const result = await response.json();
    if (result.user_id) {
        window.location.href = `/dashboard?user_id=${userId}`;
    } else {
        document.getElementById('message').innerText = result.error || "Błąd logowania";
    }
}

async function register() {
    const userId = document.getElementById('register_user_id').value;
    const name = document.getElementById('register_name').value;
    const pin = document.getElementById('register_pin').value;

    const response = await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, name: name, pin: pin })
    });

    const result = await response.json();
    document.getElementById('message').innerText = result.message || result.error;
}

async function getBalance() {
    const userId = new URLSearchParams(window.location.search).get('user_id');
    const response = await fetch(`/balance/${userId}`);
    const result = await response.json();
    document.getElementById('balance').innerText = result.balance ? `${result.balance} zł` : result.error;
}

async function deposit() {
    const userId = new URLSearchParams(window.location.search).get('user_id');
    const amount = parseFloat(document.getElementById('deposit_amount').value);

    const response = await fetch('/deposit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, amount: amount })
    });

    const result = await response.json();
    document.getElementById('message').innerText = result.message || result.error;
    getBalance();
}

async function withdraw() {
    const userId = new URLSearchParams(window.location.search).get('user_id');
    const amount = parseFloat(document.getElementById('withdraw_amount').value);

    const response = await fetch('/withdraw', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, amount: amount })
    });

    const result = await response.json();
    document.getElementById('message').innerText = result.message || result.error;
    getBalance();
}

async function transfer() {
    const userId = new URLSearchParams(window.location.search).get('user_id');
    const userIdTo = document.getElementById('transfer_to_user_id').value;
    const amount = parseFloat(document.getElementById('transfer_amount').value);

    const response = await fetch('/transfer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id_from: userId, user_id_to: userIdTo, amount: amount })
    });

    const result = await response.json();
    document.getElementById('message').innerText = result.message || result.error;
    getBalance();
}

async function getTransactionHistory() {
    const userId = new URLSearchParams(window.location.search).get('user_id');

    const response = await fetch(`/transactions/${userId}`);
    const transactions = await response.json();

    const transactionList = document.getElementById('transaction_history');
    transactionList.innerHTML = transactions.map(
        (t) => `<li>Typ: ${t.type}, Kwota: ${t.amount} zł, Data: ${t.date}</li>`
    ).join('') || '<li>Brak historii transakcji.</li>';
}

function logout() {
    window.location.href = '/';
}
