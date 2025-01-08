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
