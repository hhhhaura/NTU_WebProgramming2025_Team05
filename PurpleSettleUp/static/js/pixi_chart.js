async function initPixiChart() {
    const app = new PIXI.Application({
        height: 300,
        backgroundColor: 0xf4f4f4,
        resolution: window.devicePixelRatio || 1,
        width: document.getElementById('pixiCanvasContainer').clientWidth
    });

    // Clear the container before appending the new canvas
    const container = document.getElementById('pixiCanvasContainer');
    container.innerHTML = ''; // Remove any existing canvases
    container.appendChild(app.view);

    try {
        const response = await fetch('/api/debts/total/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Debt data:', data);  // Debug log

        if (app.stage.children.length > 0) app.stage.removeChildren();

        const maxDebt = Math.max(...data.map(u => Math.abs(parseFloat(u.net_balance))), 1);
        const circles = [];

        data.forEach(user => {
            const debt = parseFloat(user.net_balance);
            const radius = radiusScale(debt, maxDebt);
            const color = debt < 0 ? 0x991f9f : 0x1c98a5;
        
            const circle = new PIXI.Graphics();
            circle.beginFill(color).drawCircle(0, 0, radius).endFill();
        
            const label = new PIXI.Text(`${user.user}\n$${debt}`, {
                fontFamily: 'Poppins',
                fontSize: Math.max(8, radius * 0.25),
                fill: debt < 0 ? '#fff' : '#000',
                align: 'center'
            });
            label.anchor.set(0.5);
        
            const group = new PIXI.Container();
            group.addChild(circle);
            group.addChild(label);
            group.x = app.screen.width / 2 + (Math.random() * 80 - 40);
            group.y = app.screen.height / 2 + (Math.random() * 80 - 40);
            group.radius = radius;
            circles.push(group);
            app.stage.addChild(group);
        });
        resolveCircleCollisions(circles);
        scaleToFitContainer(app.stage, app.screen.width, app.screen.height);
    } catch (error) {
        console.error('Error in initPixiChart:', error);
        throw error; // Re-throw the error for proper error handling
    }
}

function radiusScale(debt, maxDebt, base = 1.6, scale = 14, minR = 20, maxR = 50) {
    const magnitude = -debt / maxDebt;
    return Math.min(minR + Math.pow(base, magnitude) * scale, maxR);
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