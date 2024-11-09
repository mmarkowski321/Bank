// Funkcja logowania
async function login(event) {
    event.preventDefault(); // Prevents the default form submission

    const userId = document.getElementById('user_id').value;
    const password = document.getElementById('password').value; // Corrected reference

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, password: password })
        });

        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const result = await response.json();
        if (result.user_id) {
            window.location.href = `/dashboard?user_id=${result.user_id}`;
        } else {
            document.getElementById('message').innerText = result.error || "Login failed";
        }
    } catch (error) {
        document.getElementById('message').innerText = `Login error: ${error.message}`;
    }
}


// Funkcja przekierowania do strony rejestracji
function displayRegistration() {
    window.location.href = '/register';
}

// Funkcja rejestracji
// Function to handle user registration
async function register(event) {
    event.preventDefault();

    if (document.getElementById('password').value === document.getElementById('confirm_password').value) {
        const firstName = document.getElementById('first_name').value;
        const middleName = document.getElementById('middle_name').value;
        const lastName = document.getElementById('last_name').value;
        const dateOfBirth = document.getElementById('birth_date').value;
        const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;
        const password = document.getElementById('password').value;
        const pin = document.getElementById('pin').value;
        const accountType = document.querySelector('input[name="account_type"]:checked').value;

        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    first_name: firstName,
                    middle_name: middleName,
                    last_name: lastName,
                    date_of_birth: dateOfBirth,
                    email: email,
                    phone: phone,
                    password: password,
                    pin: pin,
                    account_type: accountType
                })
            });

            const result = await response.json();

            if (response.ok) {
                // Hide the form and show the success message
                document.getElementById('register').classList.add('hidden');
                document.getElementById('success-message').classList.remove('hidden');
            } else {
                alert(result.error || "Registration failed. Please try again.");
            }
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    } else {
        alert("Passwords do not match");
    }
}


// Funkcja pobierania salda
async function getBalance() {
    const userId = new URLSearchParams(window.location.search).get('user_id');
    const response = await fetch(`/balance/${userId}`);
    const result = await response.json();
    document.getElementById('balance').innerText = result.balance ? `${result.balance} zł` : result.error;
}

// Funkcja wpłaty
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

// Funkcja wypłaty
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

// Funkcja przelewu
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

// Funkcja wylogowania
function logout() {
    window.location.href = '/';
}
function goToTransactionHistory() {
    const userId = new URLSearchParams(window.location.search).get('user_id');
    if (userId) {
        window.location.href = `/transaction_history?user_id=${userId}`;
    } else {
        alert("User ID not found");
    }
}
function profileSettings() {
    const userId = new URLSearchParams(window.location.search).get('user_id');
    if (userId) {
        window.location.href = `/profile.html?user_id=${userId}`;
    } else {
        alert("User ID not found. Please log in again.");
    }
}
async function changePassword(event) {
    event.preventDefault();

    const currentPasswordFromHTML = document.getElementById('current_password').value;
    const newPassword = document.getElementById('new_password').value;
    const confirmNewPassword = document.getElementById('confirm_new_password').value;
    const userId = new URLSearchParams(window.location.search).get('user_id');

    try {
        // Fetch the current password from the database
        const passwordResponse = await fetch('/get_current_password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId })
        });

        if (!passwordResponse.ok) {
            throw new Error(`Error ${passwordResponse.status}: ${passwordResponse.statusText}`);
        }

        const passwordData = await passwordResponse.json();
        const currentPasswordFromDatabase = passwordData.current_password;

        // Compare the passwords
        if (currentPasswordFromDatabase !== currentPasswordFromHTML) {
            alert("Wrong Current Password");
            return;
        }

        if (newPassword !== confirmNewPassword) {
            alert("New passwords do not match");
            return;
        }

        // Proceed to update the password
        const updateResponse = await fetch('/update_password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, current_password: currentPasswordFromHTML, new_password: newPassword })
        });

        const result = await updateResponse.json();
        alert(result.message || result.error);
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}



async function updateData(event) {
    event.preventDefault();

    const newEmail = document.getElementById('new_email').value;
    const newPhone = document.getElementById('new_phone').value;
    const userId = new URLSearchParams(window.location.search).get('user_id');

    try {
        const response = await fetch('/update_user_details', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, email: newEmail, phone: newPhone })
        });

        const result = await response.json();
        alert(result.message || result.error);
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

function togglePasswordVisibility(inputId, icon) {
    const input = document.getElementById(inputId);
    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        input.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
}
function validatePinLength(input) {
    if (input.value.length > 4) {
        input.value = input.value.slice(0, 4); // Limit to 4 characters
    }
}
