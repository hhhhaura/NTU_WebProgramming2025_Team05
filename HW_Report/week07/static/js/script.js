// ===============================
// Roommate Class
// ===============================
class Roommate {
    constructor(name, password = '') {
        this.name = name;
        this.password = password;
        this.edgeTo = {}; // Stores debts as weighted edges
    }

    updateDebt(other, amount) { // this needs to give other an amount of money
        if (this.edgeTo[other.name] === undefined) {
            this.edgeTo[other.name] = 0;
            other.edgeTo[this.name] = 0;
        }
        this.edgeTo[other.name] += amount;
        other.edgeTo[this.name] -= amount;
        history.addTransaction(this, other, amount);
    }

    getTotalDebt() {
        return Object.values(this.edgeTo).reduce((acc, val) => acc + val, 0);
    }

    getDebtTo(other) {
        return this.edgeTo[other.name] || 0;
    }
}

// ===============================
// History Class
// ===============================
class History {
    constructor() {
        this.transactions = [];
    }

    addTransaction(from, to, amount) {
        const action = amount > 0 ? 'borrowed' : 'repaid';
        const entry = {
            action,
            from: from.name,
            to: to.name,
            amount: Math.abs(amount),
            settled: action === 'repaid' ? this.isSettled(from, to) : false
        };
        this.transactions.push(entry);
    }

    isSettled(from, to) {
        return from.getDebtTo(to) === 0;
    }

    displayHistory() {
        const historyList = historySection.querySelector("ul");
        historyList.innerHTML = "";

        this.transactions.forEach((t, i) => {
            const item = document.createElement("li");
            item.textContent = `${t.from} ${t.action} $${t.amount} to ${t.to}. Settled: ${t.settled}`;
            historyList.appendChild(item);
        });
    }
}

// ===============================
// Globals and DOM Setup
// ===============================
let app = new PIXI.Application();
let roommates = [new Roommate("Alice", '123'), new Roommate("Bob"), new Roommate("Charlie")];
let history = new History();
let loginButton, usernameInput, passwordInput;
let circleContainer;
const toggleHistoryBtn = document.getElementById("toggleHistoryBtn");
const historySection = document.getElementById("historySection");

// ===============================
// UI Update Functions
// ===============================
function updateTotalDebtTable() {
    const table = document.getElementById("totalDebtTable");
    table.innerHTML = "<tr><th>Name</th><th>Total Debt</th></tr>";
    roommates.forEach(r => {
        const row = table.insertRow();
        row.insertCell(0).textContent = r.name;
        row.insertCell(1).textContent = `$ ${r.getTotalDebt()}`;
    });
    updateDebtVisualization();
}

function updateDebtRelationsTable() {
    const table = document.getElementById("debtRelationsTable");
    table.innerHTML = "<tr><th>From</th><th>To</th><th>Payback</th></tr>";
    roommates.forEach(from => {
        roommates.forEach(to => {
            if (from !== to) {
                const debt = from.getDebtTo(to);
                if (debt > 0) {
                    const row = table.insertRow();
                    row.insertCell(0).textContent = from.name;
                    row.insertCell(1).textContent = to.name;
                    row.insertCell(2).textContent = `$ ${debt}`;
                }
            }
        });
    });
}

function renderDebtorCreditorOptions() {
    const debtorSelect = document.getElementById("debtor");
    const creditorSelect = document.getElementById("creditor");
    debtorSelect.innerHTML = "";
    creditorSelect.innerHTML = "";
    roommates.forEach(r => {
        [debtorSelect, creditorSelect].forEach(select => {
            const opt = document.createElement("option");
            opt.value = r.name;
            opt.textContent = r.name;
            select.appendChild(opt.cloneNode(true));
        });
    });
}

// ===============================
// Visualization
// ===============================
function radiusScale(debt, maxDebt, base = 1.8, scale = 20, minR = 25, maxR = 80) {
    const magnitude = -debt / maxDebt;
    return Math.min(minR + Math.pow(base, magnitude) * scale, maxR);
}

function updateDebtVisualization() {
    if (circleContainer) app.stage.removeChild(circleContainer);
    circleContainer = new PIXI.Container();
    app.stage.addChild(circleContainer);
    const maxDebt = Math.max(...roommates.map(r => Math.abs(r.getTotalDebt())), 1);

    const sorted = [...roommates].sort((a, b) => Math.abs(a.getTotalDebt()) - Math.abs(b.getTotalDebt()));
    const circles = [];

    sorted.forEach(r => {
        const debt = r.getTotalDebt();
        const radius = radiusScale(debt, maxDebt);
        const color = debt < 0 ? 0x991f9f : 0x1c98a5;

        const circle = new PIXI.Graphics();
        circle.beginFill(color).drawCircle(0, 0, radius).endFill();

        const label = new PIXI.Text(`${r.name}\n$${debt}`, {
            fontFamily: 'Poppins', fontSize: 14, fill: debt < 0 ? '#fff' : '#000', align: 'center'
        });
        label.anchor.set(0.5);

        const group = new PIXI.Container();
        group.addChild(circle);
        group.addChild(label);
        group.x = app.screen.width / 2 + (Math.random() * 10 - 5);
        group.y = app.screen.height / 2 + (Math.random() * 10 - 5);
        group.radius = radius;
        group.interactive = true;
        group.buttonMode = true;
        group.on('pointerdown', onDragStart).on('pointerup', onDragEnd).on('pointermove', onDragMove);

        circles.push(group);
        circleContainer.addChild(group);
    });

    resolveCircleCollisions(circles);
    scaleToFitContainer(circleContainer, app.screen.width, app.screen.height);
}

function resolveCircleCollisions(circles, iterations = 30) {
    for (let i = 0; i < iterations; i++) {
        for (let a = 0; a < circles.length; a++) {
            for (let b = a + 1; b < circles.length; b++) {
                const A = circles[a], B = circles[b];
                const dx = B.x - A.x, dy = B.y - A.y;
                const dist = Math.hypot(dx, dy);
                const minDist = A.radius + B.radius + 4;
                if (dist < minDist) {
                    const angle = Math.atan2(dy, dx);
                    const shift = (minDist - dist) / 2;
                    A.x -= Math.cos(angle) * shift;
                    A.y -= Math.sin(angle) * shift;
                    B.x += Math.cos(angle) * shift;
                    B.y += Math.sin(angle) * shift;
                }
            }
        }
    }
}

function scaleToFitContainer(container, maxW, maxH) {
    const bounds = container.getLocalBounds();
    const scale = Math.min(maxW / bounds.width, maxH / bounds.height, 1);
    container.scale.set(scale);
    container.x = (maxW - bounds.width * scale) / 2 - bounds.x * scale;
    container.y = (maxH - bounds.height * scale) / 2 - bounds.y * scale;
}

function onDragStart(e) { this.data = e.data; this.dragging = true; this.alpha = 0.7; }
function onDragEnd() { this.alpha = 1; this.dragging = false; this.data = null; }
function onDragMove() { if (this.dragging) { const p = this.data.getLocalPosition(this.parent); this.x = p.x; this.y = p.y; } }

// ===============================
// Application Entry
// ===============================
async function startApplication() {
    await app.init({ width: 800, height: 400, backgroundColor: 0xf4f4f4, resolution: window.devicePixelRatio || 1 });
    document.getElementById("pixiCanvasContainer").appendChild(app.canvas);

    loginButton = document.querySelector(".login-box button");
    usernameInput = document.getElementById("username");
    passwordInput = document.getElementById("password");

    loginButton.addEventListener("click", async e => {
        e.preventDefault();
        const username = usernameInput.value;
        const password = passwordInput.value;

        const res = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
            credentials: "include"  // 這很重要：允許 cookie 存在
        });

        const data = await res.json();
        if (data.success) {
            alert("Login successful as " + data.username);
            usernameInput.value = "";
            passwordInput.value = "";
            updateTotalDebtTable();
            updateDebtRelationsTable();
            renderDebtorCreditorOptions();
            history.displayHistory();
        } else {
            alert(data.error || "Login failed");
        }
    });

    document.getElementById("debtUpdateForm").addEventListener("submit", e => {
        e.preventDefault();
        const debtorName = document.getElementById("debtor").value;
        const creditorName = document.getElementById("creditor").value;
        const amount = parseFloat(document.getElementById("amount").value);
        if (debtorName !== creditorName && !isNaN(amount)) {
            const debtor = roommates.find(r => r.name === debtorName);
            const creditor = roommates.find(r => r.name === creditorName);
            debtor.updateDebt(creditor, amount);
            updateTotalDebtTable();
            updateDebtRelationsTable();
            history.displayHistory();
        }
    });

    updateTotalDebtTable();
    updateDebtRelationsTable();
    renderDebtorCreditorOptions();
    history.displayHistory();
}

window.addEventListener("DOMContentLoaded", () => startApplication());

toggleHistoryBtn.addEventListener("click", () => {
    const isVisible = historySection.style.display === "block";
    historySection.style.display = isVisible ? "none" : "block";
    toggleHistoryBtn.textContent = isVisible ? "Show History" : "Hide History";
});
