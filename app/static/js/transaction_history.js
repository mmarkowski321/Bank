async function fetchTransactionHistory() {
    const userId = new URLSearchParams(window.location.search).get('user_id');
    if (!userId) {
        document.getElementById('transaction_history').innerHTML = "<li>Error: No user ID provided</li>";
        return;
    }
    try {
        const response = await fetch(`/transactions/${userId}`);
        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const transactions = await response.json();
        const transactionList = document.getElementById('transaction_history');
        transactionList.innerHTML = "";  // Wyczyść poprzednie wpisy

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
        document.getElementById('transaction_history').innerHTML = `<li>Error: ${error.message}</li>`;
    }
}

// Automatyczne załadowanie historii transakcji po otwarciu strony
window.onload = fetchTransactionHistory;
