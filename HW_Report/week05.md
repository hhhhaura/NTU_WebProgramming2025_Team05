# Team 5 Week 5 Report

## Quick Overview
本週的主題是 Javascript，我們延續製作上次的線上多人記帳網站來練習這些技術，確保室友之間的借貸記錄清晰、透明，減少財務上的混亂。另外，我們使用 PixiJS，一個基於 WebGL 技術用來建立 2D 圖形與動畫的網頁繪圖引擎。

### 系統 Features Highlight
* 每個人的總債務表
* 人與人之間債務關係表
* 更新債務功能
* 金錢借還歷史紀錄
* 登入、新增、驗證使用者
* PixJS 直觀的債務視覺化

[Demo Link](https://hsinchu-huang-147.tplinkdns.com:12345/week03)

## 當週主題練習
### 使用的 JavaScript 技術
#### 基礎 JavaScript
- 使用物件導向程式設計（OOP）
  - `Roommate` 類別管理債務資料與互動
  - `History` 類別紀錄與顯示交易紀錄

- 使用常見陣列方法
  - `.forEach()`, `.map()`, `.reduce()`, `.sort()`

- 解構與展開運算子 `...`
  - 用於複製與排序陣列

- 使用模板字串（Template Literals）
  - 範例： `` `${roommate.name} - $${debt}` ``

- 使用三元運算子處理邏輯
  - 範例：`amount > 0 ? 'borrowed' : 'repaid'`


#### DOM 操作與互動控制

- 使用 `getElementById` 和 `querySelector` 查找元素
- 動態建立表格與下拉選單項目
- 使用 `addEventListener` 綁定事件
  - 登入按鈕點擊事件
  - 債務更新表單提交事件
  - Show/Hide History 按鈕切換事件


#### 非同步處理

- 使用 `async`/`await` 確保 PixiJS 初始化後再進行畫面渲染與邏輯處理


#### 使用者介面與流程邏輯 (無後端)

- 登入驗證流程
  - 若帳號存在 → 驗證密碼
  - 若帳號不存在 → 新增帳號並登入

- 債務更新流程
  - 透過表單選取債權人、債務人、輸入金額後更新資料

- 歷史紀錄動態顯示
  - 加入、清空、更新 `<ul>` 列表內容


## 額外練習
### PixiJS 技術 
- 建立 `PIXI.Application` 應用實例
- 使用 `PIXI.Graphics` 繪製圓形代表債務大小
- 使用 `PIXI.Text` 顯示名字與債務金額
- 使用 `PIXI.Container` 組合圖形與文字
- 使用 `interactive`、`pointerdown`、`pointermove` 實作拖曳互動
- 加入 `resolveCircleCollisions` 避免圓形重疊
- 使用 `scaleToFitContainer` 自動縮放畫面內容以符合容器

### HTTPS demo
考慮到本專案未來可能需要整合後端伺服器，僅使用系上工作站 `https://www.csie.ntu.edu.tw/~[student ID]` 可能無法完成，因此我們將本週作業放在 [這裡](https://hsinchu-huang-147.tplinkdns.com:12345) demo。

## 分工情形
組別：第五組
- 黃邦維 (b10902039)：
    - 25% PixiJS 債務視覺化
- 鄭允臻 (b11902010)：
    - 25% 主要 OOP 架構與功能 - 1
- 黃梓宏 (b11902023)：
    - 25% CSS styling + Code refactoring + 報告撰寫
- 吳柏毅 (b11902127)：
    - 25% 主要 OOP 架構與功能 - 2
