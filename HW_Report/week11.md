# Team 5 Week 11 Report

## Quick Overview

本週主題是 AJAX 和 WebSocket。在先前的專案中，我們製作了線上多人記帳網站。除了基本的記帳功能，我們也實作了視覺化呈現 (PixiJs) 和註冊及登入登出等功能。

在先前的基礎上，我們利用 AJAX 及 WebSocket 技術，在新交易產生時自動更新交易紀錄、負債關係表和 Pixi 圖示，使用戶不必頻繁重整網頁，也可以取得即時資訊。

最後，我們改寫 `layout.html` 及其他內容，使不同頁面設計語言更加一致，且符合 Django 設計慣例。

[Week 11 Demo Link](https://hsinchu-huang-147.tplinkdns.com:12347)

[Assignment Demo Link](https://hsinchu-huang-147.tplinkdns.com:12345)

## 當週主題練習
### AJAX 和 WebSocket
- 在 `update_history.js` 中，使用 AJAX 透過 `fetch` 函數從 API 獲取交易紀錄和負債關係數據，並動態更新頁面上的交易歷史表和負債關係表。
- 實作 WebSocket 連線。當伺服器端有新交易時，透過 WebSocket 接收更新訊息，觸發 `fetchTransactions` 和 `fetchDebts` 函數，確保用戶無需手動重整頁面即可看到最新數據。
- 修改 `pixi_chart.js` ，使其自動更新時清除舊的畫布並重新繪製負債總覽圖表。


### 重做部分 Django

- 使用 `layout.html` 作為統一模板，使不同頁面擁有統一的設計語言
- 將登入頁面及註冊頁面的 `form` 改為由 Django 提供的 `AuthenticationForm` 和 `UserCreationForm`，讓 Django 幫我們處理基本登入登出，並且避免註冊密碼過於簡單。

## 額外練習
我們將這次作業

## Docker 啟動方式

指令：

```bash
docker-compose up --build -d
```
這次沒有設定 super user

## 分工情形

組別：第五組

- 黃邦維 (b10902039)：25%
  - Docker 容器化部署
- 鄭允臻 (b11902010)：25%
  - 調整 Django code 
- 黃梓宏 (b11902023)：25%
  - 前端 AJAX 設計
- 吳柏毅 (b11902127)：25%
  - 後端 WebSocket 設計
