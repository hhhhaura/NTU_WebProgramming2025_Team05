function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit' 
    };
    return new Date(dateString).toLocaleString(undefined, options);
}

async function fetchTransactions() {
    try {
        const response = await fetch('/api/transactions/');
        const data = await response.json();
        updateTransactionTable(data);
    } catch (error) {
        console.error('Error fetching transactions:', error);
    }
}

async function fetchDebts() {
    try {
        const response = await fetch('/api/debts/');
        const data = await response.json();
        const tbody = document.querySelector('#debtSection tbody');
        tbody.innerHTML = '';
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3">No debts to display</td></tr>';
        } else {
            data.forEach(debt => {
                tbody.innerHTML += `
                    <tr>
                        <td>${debt.debtor}</td>
                        <td>${debt.creditor}</td>
                        <td>$${debt.amount}</td>
                    </tr>
                `;
            });
        }
    } catch (error) {
        console.error('Error fetching debts:', error);
    }
}

function updateTransactionTable(transactions) {
    const tbody = document.querySelector('#historySection tbody');
    tbody.innerHTML = '';
    if (transactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5">No transactions to display</td></tr>';
    } else {
        transactions.forEach(transaction => {
            tbody.innerHTML += `
                <tr>
                    <td>${transaction.creditor}</td>
                    <td>${transaction.debtor}</td>
                    <td>$${transaction.amount}</td>
                    <td>${new Date(transaction.created_at).toLocaleString()}</td>
                    <td>${transaction.id}</td>
                </tr>
            `;
        });
    }
}

// Poll for updates every 5 seconds
async function pollForUpdates() {
    try {
        await Promise.all([
            fetchTransactions(),
            fetchDebts(),
            initPixiChart()
        ]);
    } catch (error) {
        console.error('Error polling for updates:', error);
    }
}

// Initial load
document.addEventListener('DOMContentLoaded', () => {
    pollForUpdates();
    // Set up polling interval
    setInterval(pollForUpdates, 5000);
});