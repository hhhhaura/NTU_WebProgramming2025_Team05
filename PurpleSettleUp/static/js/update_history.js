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
    const response = await fetch('/api/transactions/');
    const data = await response.json();
    const tbody = document.querySelector('#historySection tbody');
    tbody.innerHTML = '';
    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5">No transactions to display</td></tr>';
    } else {
        data.forEach(trans => {
            tbody.innerHTML += `
                <tr>
                    <td>${trans.creditor}</td>
                    <td>${trans.debtor}</td>
                    <td>${trans.amount}</td>
                    <td>${formatDate(trans.created_at)}</td>
                    <td><a href="/transaction/history/${trans.slug}">${trans.slug}</a></td>
                </tr>
            `;
        });
    }
}

async function fetchDebts() {
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
}

const wsProtocol = window.location.protocol === "https:" ? "wss" : "ws";
const wsHost = window.location.host === "localhost:8001" ? "localhost:8001" : "hhhhaura.pythonanywhere.com";
const ws = new WebSocket(`${wsProtocol}://${wsHost}/ws/transactions/`);

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === "update") {
        fetchTransactions();
        fetchDebts();
        initPixiChart();
    }
};

ws.onopen = () => {
    console.log("WebSocket connection opened.");
};

ws.onclose = () => {
    console.log("WebSocket connection closed.");
};

// Fetch immediately on load
fetchTransactions();
fetchDebts();