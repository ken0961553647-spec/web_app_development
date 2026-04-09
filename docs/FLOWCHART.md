# 食譜收藏夾 流程圖與路由設計

本文件根據 `docs/PRD.md` 中定義的系統功能需求與 `docs/ARCHITECTURE.md` 制定的技術架構，繪製了對應的系統流程邏輯，包含使用者視角的頁面流轉、伺服器端的資料寫入序列，以及功能與路由對照表。

---

## 1. 使用者流程圖（User Flow）

此流程圖涵蓋了一般使用者從進入網站開始，所能進行的所有主要操作路徑（包含瀏覽、尋找、管理自身食譜及會員登入登出操作）。

```mermaid
flowchart LR
    Start([使用者進入首頁]) --> Auth{是否已登入？}
    
    Auth -- 否 --> VisitList[首頁：瀏覽公開/精選食譜]
    VisitList --> ActionGuest{訪客動作}
    ActionGuest -->|想登入| Login[進入登入頁面]
    ActionGuest -->|想註冊| Register[進入註冊頁面]
    ActionGuest -->|查看| ViewDetail[觀看單一食譜內容]
    Login --> Auth
    Register --> Login
    
    Auth -- 是 --> Home[首頁：個人食譜列表]
    Home --> ActionUser{要執行什麼操作？}
    
    ActionUser -->|搜尋| Search[輸入關鍵字搜尋食譜]
    ActionUser -->|瀏覽| ViewDetail[觀看單一食譜內容]
    ActionUser -->|新增| Add[進入新增食譜頁面]
    ActionUser -->|登出| Logout[執行登出操作並回首頁]
    
    ViewDetail --> ActionDetail{單一食譜操作}
    ActionDetail -->|編輯| Edit[進入編輯食譜頁面]
    ActionDetail -->|刪除| Delete[確認並刪除此食譜]
    ActionDetail -->|回列表| Home
    
    Search --> Home
    Add -->|提交表單| Home
    Edit -->|提交修改| ViewDetail
    Delete -->|完成刪除| Home
```

---

## 2. 系統序列圖（Sequence Diagram）

以下序列圖展示了 PRD 中「儲存食譜」這項核心功能，在內部元件（瀏覽器、Flask、SQLite）之間是如何流動與處理的。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 網頁瀏覽器
    participant Flask Route as Flask 路由 (Controller)
    participant Model as Recipe 模型
    participant DB as SQLite 資料庫

    User->>Browser: 在新增食譜頁面填寫食材與步驟並點擊送出
    Browser->>Flask Route: HTTP POST /recipes/new (攜帶表單資料)
    
    Flask Route->>Flask Route: 驗證是否登入及權限
    Flask Route->>Flask Route: 驗證表單欄位是否完整 (防呆)
    
    Flask Route->>Model: 呼叫 Recipe.create(data)
    Model->>DB: INSERT INTO recipes (title, ingredients, steps, user_id)
    
    alt 儲存成功
        DB-->>Model: 回傳新紀錄 ID 等確認資訊
        Model-->>Flask Route: 傳回成功狀態
        Flask Route-->>Browser: HTTP 302 導向回「首頁列表」<br/>(並附帶成功提示訊息)
        Browser-->>User: 顯示已更新的個人食譜清單
    else 儲存失敗 (例如發生錯誤)
        DB-->>Model: 回傳錯誤 (如資料型態或連線問題)
        Model-->>Flask Route: 拋出例外或傳回失敗狀態
        Flask Route-->>Browser: 重新渲染新增表單頁<br/>(並顯示錯誤提示以免重新填寫)
        Browser-->>User: 看到錯誤訊息並可重新修改
    end
```

---

## 3. 功能清單對照表

將上述操作路徑對應至 Flask 路由設計中，初步規劃出以下 URL Endpoint 及 HTTP Methods：

| 功能項目 | URL 路徑 | HTTP 方法 | 對應的 Jinja2 模板 (View) |
| --- | --- | --- | --- |
| 瀏覽首頁 (食譜列表) | `/` | GET | `recipes/list.html` |
| 瀏覽食譜細節 | `/recipes/<id>` | GET | `recipes/detail.html` |
| 搜尋食譜 | `/recipes/search` | GET | `recipes/list.html` |
| 進入新增食譜頁面 | `/recipes/new` | GET | `recipes/form.html` |
| 提交新增食譜表單 | `/recipes/new` | POST | (轉址至 `/`) |
| 進入編輯食譜頁面 | `/recipes/<id>/edit` | GET | `recipes/form.html` |
| 提交編輯食譜表單 | `/recipes/<id>/edit` | POST | (轉址至 `/recipes/<id>`) |
| 執行刪除食譜 | `/recipes/<id>/delete` | POST | (轉址至 `/`) |
| 進入登入頁面 | `/login` | GET | `auth/login.html` |
| 執行登入驗證 | `/login` | POST | (轉址至 `/`) |
| 進入註冊頁面 | `/register` | GET | `auth/register.html` |
| 執行註冊帳號 | `/register` | POST | (轉址至 `/login`) |
| 執行登出系統 | `/logout` | GET (或 POST) | (轉址至 `/`) |
