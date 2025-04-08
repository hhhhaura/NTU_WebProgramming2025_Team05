# Team 5 Week 7 Report

## Quick Overview  
本週主題：後端整合與 Docker部署。我們將前五週完成的前端介面（HTML/CSS/JS）與 Django REST Framework 後端結合，實作使用者系統、交易 CRUD、債務計算等 API，並以 MySQL 作為資料庫，最後使用 Docker Compose 完成本專案的容器化部署，確保開發與生產環境一致。

### 系統 Features Highlight
* 使用者登入／註冊／登出（Session + CSRF 保護）
* 交易 CRUD API（列表、建立、更新、查詢）
* 債務結算與總債務查詢 API (`/api/debt-relations/`, `/api/total-debts/`)
* MySQL 資料庫儲存與 Django ORM 操作
* Docker 容器化部署（Django + Gunicorn + MySQL）
* 靜態檔案服務與壓縮（Whitenoise）

[Week 7 Demo Link](https://hsinchu-huang-147.tplinkdns.com:12346)
[Assignment Demo Link](https://hsinchu-huang-147.tplinkdns.com:12345)


## 當週主題練習

### 使用的 Django 技術
- 使用 `@login_required`、`authenticate`、`login`、`logout` 處理使用者驗證流程  
- Django Template：`index.html`、`login.html`、`register.html`，並使用 `{% csrf_token %}`  
- Django REST Framework：`@api_view` 定義 API endpoints，回傳 JSON 與適當 HTTP status  
- Serializer：`UserSerializer`、`TransactionSerializer` 序列化使用者與交易資料  
- URL Routing：`urlpatterns` 定義前端頁面與 API 路由  

### 使用的 MySQL 與 ORM
- 在 `settings.py` 中設定 `DATABASES` 為 MySQL，並透過環境變數載入連線參數  
- Transaction Model：`ForeignKey` 連結 `User`，`DecimalField` 儲存金額，`auto_now_add` 紀錄時間  
- 債務計算邏輯：  
  - `debt_relation_get`：聚合所有交易紀錄，計算最簡結算表  
  - `total_debt_view`：計算每人淨債務  

### 使用的 Docker 技術
- **Dockerfile**：以 `python:3.13` 為基底，安裝依賴，使用 Gunicorn 啟動 Django  
- **docker-compose.yml**：定義 `web`（Django + Gunicorn）與 `db`（MySQL）服務，設定 `depends_on` 與 healthcheck  
- **Whitenoise**：在 `MIDDLEWARE` 中加入 `WhiteNoiseMiddleware`，提供壓縮後的靜態檔案  

### 前端認證與 CSRF 處理
- Login/Register 頁面使用 `fetch` 搭配 `getCookie("csrftoken")` 傳送 POST 請求  
- `.notification` 顯示失敗訊息  
- 於 logout endpoint 使用 `@csrf_exempt` 處理 CSRF  

## 分工情形  
組別：第五組  
- 黃邦維 (b10902039)：25% Dockerfile & Docker Compose 容器化部署  
- 鄭允臻 (b11902010)：25% MySQL 資料庫設定與 Django settings  
- 黃梓宏 (b11902023)：25% REST API Views 與債務計算邏輯  
- 吳柏毅 (b11902127)：25% 前端登入/註冊模板與 CSRF 整合  
