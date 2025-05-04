# NTU CSIE Web Programming 2025 Spring

Welcome to the GitHub repository for our assignments in the NTU CSIE Web Programming 2025 Spring course. This repository contains the source code and documentation for our group's projects, showcasing our progress in web development technologies including HTML, CSS, JavaScript, PixiJS, Django, and Docker.

## About This Project

Our assignments focus on building an online expense tracking system for roommates, progressively enhanced with front-end and back-end technologies.

### Group Members

| Name       | Student ID |
|------------|------------|
| 黃邦維 | b10902039  |
| 鄭允臻 | b11902010  |
| 黃梓宏 | b11902023  |
| 吳柏毅 | b11902127  |

## Assignments

Below are the details of our assignments, including descriptions and demo links.

### Week 3 - Fundamental HTML, CSS, and JavaScript
- **Description**: Built an online expense tracking system using HTML and CSS to maintain transparent financial records for roommates. Features include a login form (`<form>`), transaction record table (`<table>`), and interactive buttons (`<button>`) for toggling visibility. CSS enhances the UI with gradients and structured layouts. Basic JavaScript enables toggling transaction history, and the site is served over HTTPS.
- **Demo**: [Week 3 Demo](https://hsinchu-huang-147.tplinkdns.com:12345/week03)

### Week 5 - Advanced JavaScript with PixiJS
- **Description**: Enhanced the expense tracker with advanced JavaScript and PixiJS, a 2D graphics engine. Added debt summaries, roommate relationships, and a dynamic debt table using OOP, JavaScript methods (`.forEach()`, `.map()`, `async/await`), and template literals. PixiJS visualizes debts with interactive 2D graphics, creating an engaging front-end interface without backend integration.
- **Demo**: [Week 5 Demo](https://hsinchu-huang-147.tplinkdns.com:12345/week05)

### Week 7 - Backend Integration and Docker Deployment
- **Description**: Integrated the front-end with a Django REST Framework backend, adding user authentication, transaction CRUD operations, and debt calculation APIs. Connected to a MySQL database and containerized with Docker for consistent development and production environments. Optimized with Gunicorn for performance and Whitenoise for static files.
- **Demo**: [Week 7 Demo](https://hsinchu-huang-147.tplinkdns.com:12346)

### Week 11 - AJAX, WebSocket, and Django Refinement
- **Description**: Enhanced the expense tracking system with real-time updates using AJAX and WebSocket technologies. Implemented AJAX with `fetch` to dynamically update transaction history and debt relationship tables without page refreshes. Integrated WebSocket to push new transaction notifications from the server, triggering automatic data refreshes for tables and PixiJS debt visualizations. Refactored Django templates using a unified `layout.html` for consistent design and adopted Django’s `AuthenticationForm` and `UserCreationForm` for secure login and registration. The application remains containerized with Docker for seamless deployment.
- **Demo**: [Week 11 Demo](https://hsinchu-huang-147.tplinkdns.com:12347)

## Getting Started
To explore or run the projects locally, clone this repository:
```bash
git clone https://github.com/hhhhaura/NTU_WebProgramming2025_Team05.git
```

Follow these steps to view each week's project:

1. **Week 3**:
   ```bash
   cd HW_Report/week03
   python -m http.server 8000
   ```
   Then visit `http://localhost:8000` in your browser.

2. **Week 5**:
   ```bash
   cd HW_Report/week05
   python -m http.server 8000
   ```
   Then visit `http://localhost:8000` in your browser.

3. **Week 7**:
   ```bash
   cd HW_Report/week07
   docker compose build
   docker compose up -d
   ```
   Then visit `http://localhost:8000` in your browser.

4. **Week 11**:
   ```bash
   cd HW_Report/week11
   docker compose up --build -d
   ```
   Then visit `http://localhost:8001` in your browser.
