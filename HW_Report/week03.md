# Team 5 Week 3 Report

## Quick Overview
本週的主題是 HTML 和 CSS，我們透過製作一個線上多人記帳網站來練習這些技術，確保室友之間的借貸記錄清晰、透明，減少財務上的混亂。另外，我們找了基礎 Javascript 和 HTTPS 連線作為課外練習。

[Demo Link](https://hsinchu-huang-147.tplinkdns.com:12345/week03)

## 當週主題練習

### 使用的 HTML 技術
`index.html` 使用以下 HTML 元素：
- `<form>`：建立登入系統，包含使用者名稱和密碼欄位，不過目前沒有實際登入功能。
- `<table>`：顯示室友間的借貸記錄以及各自的總欠款。
- `<button>`：用於切換交易紀錄區塊的顯示狀態。
- 語義化標籤：
  - `<h1>`：網頁標題。
  - `<p>`：描述表格內容。
  - `<div>`：用於區塊分隔，例如登入框與歷史紀錄區塊。
  - `<ul>` & `<li>`：列出交易紀錄。

### 使用的 CSS 技術
`styles.css` 使用以下 CSS 元素：
- `body`：
  - `font-family` 設定統一字體。
  - `background-color` 設定背景色提升對比度。
  
- `h1`：
  - `background: linear-gradient(to right, #4CAF50, #2e7d32);` 創造 漸層背景。
  - `text-transform: uppercase;` 讓標題全大寫，提高可讀性。
  
- `table`：
  - `border-collapse: collapse;` 讓邊框合併，看起來更整齊。
  - `th { background-color: #4CAF50; color: white; }` 讓標題列更加突出。

- `.login-box`：
  - `position: absolute; top: 100px; right: 20px;` 讓登入框固定在右上角。
  - `box-shadow` 增加陰影效果，使其更有層次。

- `.history-section`：
  - 預設 `display: none;` 隱藏，透過 JavaScript 切換顯示狀態。
  - `border-bottom: 1px solid #ddd;` 在清單項目間加入 分隔線，讓資訊更易讀。

## 額外練習

### JavaScript 功能
- 交易紀錄顯示切換功能：
  - `#toggleHistoryBtn` 控制 `#historySection` 顯示與隱藏。
  - `addEventListener("click", function() {...}` 追蹤點擊事件。
  - 使用 `style.display` 切換狀態。

### HTTPS demo
考慮到本專案未來可能需要整合後端伺服器，僅使用系上工作站 `https://www.csie.ntu.edu.tw/~[student ID]` 可能無法完成，因此我們將本週作業放在 [這裡](https://hsinchu-huang-147.tplinkdns.com:12345) demo。

## 分工情形
組別：第五組
- 黃邦維 (b10902039)：
    - 25%
    - HTTPS 及 Javascript
- 鄭允臻 (b11902010)：
    - 25%
    - CSS
- 黃梓宏 (b11902023)：
    - 25%
    - HTML part 1
- 吳柏毅 (b11902127)：
    - 25%
    - HTML part 2
