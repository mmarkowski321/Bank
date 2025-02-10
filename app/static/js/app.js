async function login(event) {
    event.preventDefault();

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



function displayRegistration() {
    window.location.href = '/register';
}

async function register(event) {
    event.preventDefault();

    // Check if passwords match
    if (document.getElementById('password').value === document.getElementById('confirm_password').value) {
        // Retrieve form values
        const firstName = document.getElementById('first_name').value;
        const middleName = document.getElementById('middle_name').value;
        const lastName = document.getElementById('last_name').value;
        const dateOfBirth = document.getElementById('birth_date').value;
        const email = document.getElementById('email').value;

        // Get the selected country code and phone number
        const countryCode = document.getElementById('country_code').value;
        const phone = document.getElementById('phone').value;
        const fullPhoneNumber = `${countryCode}${phone}`;

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
                    phone: fullPhoneNumber,
                    password: password,
                    pin: pin,
                    account_type: accountType
                })
            });

            const result = await response.json();

            if (response.ok) {
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

function logout() {
    window.location.href = '/';
}
function goToTransactionHistory() {
    const userId = new URLSearchParams(window.location.search).get('user_id');
    if (userId) {
        window.location.href = `/transactions/${userId}`;
    } else {
        alert("User ID not found");
    }
}

function profileSettings() {
    const userId = new URLSearchParams(window.location.search).get('user_id');
    if (userId) {
        window.location.href = `/profile.html?user_id=${userId}`;
    } else {
        alert("User ID not found");
    }
}
async function changePassword(event) {
    event.preventDefault();

    const currentPasswordFromHTML = document.getElementById('current_password').value;
    const newPassword = document.getElementById('new_password').value;
    const confirmNewPassword = document.getElementById('confirm_new_password').value;
    const userId = new URLSearchParams(window.location.search).get('user_id');

    console.log("User ID:", userId);
    console.log("Current Password:", currentPasswordFromHTML);
    console.log("New Password:", newPassword);

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

        if (currentPasswordFromDatabase !== currentPasswordFromHTML) {
            alert("Wrong Current Password");
            return;
        }

        if (newPassword !== confirmNewPassword) {
            alert("New passwords do not match");
            return;
        }

        const updateResponse = await fetch('/update_password', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, current_password: currentPasswordFromHTML, new_password: newPassword })
        });

        const result = await updateResponse.json();
        alert(result.message || result.error);
    } catch (error) {
        console.error("Error during password change:", error);
        alert(`Error: ${error.message}`);
    }
}



async function updateData(event) {
    event.preventDefault();

    const newEmail = document.getElementById('new_email').value;
    const newPhone = document.getElementById('new_phone').value;
    const userId = new URLSearchParams(window.location.search).get('user_id');

    let dataToUpdate = { user_id: userId };
    if (newEmail) dataToUpdate.email = newEmail;
    if (newPhone) dataToUpdate.phone = newPhone;

    if (!newEmail && !newPhone) {
        alert("Please fill out at least one field to update.");
        return;
    }

    try {
        const response = await fetch('/update_user_details', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dataToUpdate)
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
function populateCountryCodes() {
    const countryCodes = [
        { name: "United States", code: "+1" },
        { name: "United Kingdom", code: "+44" },
        { name: "India", code: "+91" },
        { name: "Australia", code: "+61" },
        { name: "Japan", code: "+81" },
        { name: "Germany", code: "+49" },
        { name: "China", code: "+86" },
        { name: "France", code: "+33" },
        { name: "Italy", code: "+39" },
        { name: "Spain", code: "+34" },
        { name: "Brazil", code: "+55" },
        { name: "Russia", code: "+7" },
        { name: "South Africa", code: "+27" },
        { name: "Nigeria", code: "+234" },
        { name: "Mexico", code: "+52" },
        { name: "Netherlands", code: "+31" },
        { name: "Poland", code: "+48" },
    ];

    const select = document.getElementById('country_code');
    countryCodes.forEach(country => {
        const option = document.createElement('option');
        option.value = country.code;
        option.textContent = `${country.name} (${country.code})`;
        select.appendChild(option);
    });
}

document.addEventListener("DOMContentLoaded", populateCountryCodes);

async function fetchTransactionHistory() {
    const userId = new URLSearchParams(window.location.search).get('user_id');
    const transactionList = document.getElementById('transaction_history');

    if (!userId) {
        transactionList.innerHTML = "<li>Error: No user ID provided</li>";
        return;
    }

    try {
        const response = await fetch(`/transactions/${userId}`);
        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const transactions = await response.json();
        transactionList.innerHTML = "";

        if (transactions.length > 0) {
            transactions.forEach(transaction => {
                const listItem = document.createElement('li');
                listItem.textContent = `Type: ${transaction.type}, Amount: ${transaction.amount} zł, Date: ${transaction.date}`;
                transactionList.appendChild(listItem);
            });
        } else {
            transactionList.innerHTML = "<li>No transactions found.</li>";
        }
    } catch (error) {
        transactionList.innerHTML = `<li>Error: ${error.message}</li>`;
    }
}

window.onload = fetchTransactionHistory;
