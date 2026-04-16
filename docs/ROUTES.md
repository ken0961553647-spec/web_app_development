# 路由設計文件 (API Design)

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 / 食譜列表 | GET | `/` | `recipes/list.html` | 顯示所有公開食譜或使用者的食譜 |
| 搜尋食譜 | GET | `/recipes/search` | `recipes/list.html` | 根據關鍵字搜尋食譜 |
| 食譜詳情 | GET | `/recipes/<int:id>` | `recipes/detail.html` | 顯示單筆食譜完整內容 |
| 新增食譜頁面 | GET | `/recipes/new` | `recipes/form.html` | 顯示新增食物的表單 |
| 建立食譜 | POST | `/recipes/new` | — | 接收表單並寫入資料庫，轉址回首頁 |
| 編輯食譜頁面 | GET | `/recipes/<int:id>/edit` | `recipes/form.html` | 顯示預填舊資料的編輯表單 |
| 更新食譜 | POST | `/recipes/<int:id>/edit` | — | 接收表單並更新紀錄，轉址回食譜詳情 |
| 刪除食譜 | POST | `/recipes/<int:id>/delete` | — | 刪除食譜並轉址回首頁 |
| 註冊頁面 | GET | `/register` | `auth/register.html` | 顯示註冊表單 |
| 執行註冊 | POST | `/register` | — | 新增帳號，成功後轉址至登入頁 |
| 登入頁面 | GET | `/login` | `auth/login.html` | 顯示登入表單 |
| 執行登入 | POST | `/login` | — | 驗證帳密，成功後記錄 Session 並轉址至首頁 |
| 執行登出 | POST或GET| `/logout` | — | 清除 Session 並轉址至首頁 |

## 2. 每個路由的詳細說明

### Auth 模組 (`app/routes/auth.py`)

- **GET `/register`**
  - **輸入**：無
  - **處理邏輯**：無特殊處理。
  - **輸出**：渲染 `auth/register.html`。
  
- **POST `/register`**
  - **輸入**：表單欄位 `username`, `email`, `password_hash` (實務上表單輸入 password 並由後端 bcrypt 加密)。
  - **處理邏輯**：呼叫 `User.create(...)` 建立帳戶。若帳號或 Email 重複需拋出錯誤回傳。
  - **輸出**：成功後轉址至 `/login`，若有誤則重新渲染 `register.html` 並顯示錯誤訊息。

- **GET `/login`**
  - **輸入**：無
  - **處理邏輯**：無特殊處理。
  - **輸出**：渲染 `auth/login.html`。

- **POST `/login`**
  - **輸入**：表單欄位 `email` 或 `username`, `password`。
  - **處理邏輯**：呼叫 `User.get_by_email` 或 username 找出記錄，對比密碼是否正確。正確則將使用者資訊存入 session。
  - **輸出**：成功後轉址至 `/`，失敗則重新渲染 `login.html` 並顯示錯誤訊息。

- **GET / POST `/logout`**
  - **輸入**：無
  - **處理邏輯**：從 session 中移除帳號登入狀態。
  - **輸出**：轉址至 `/`。

### Recipes 模組 (`app/routes/recipes.py`)

- **GET `/`**
  - **輸入**：無
  - **處理邏輯**：判斷若有登入狀態，呼叫 `Recipe.get_by_user_id(session['user_id'])` 取得個人食譜；若無登入則顯示未登入情境。
  - **輸出**：渲染 `recipes/list.html` 帶入食譜清單。

- **GET `/recipes/search`**
  - **輸入**：URL Query String `?q=keyword`
  - **處理邏輯**：呼叫 `Recipe.search_by_title_or_ingredient(keyword)` 進行模糊比對。
  - **輸出**：渲染 `recipes/list.html` 帶入搜尋結果。

- **GET `/recipes/<int:id>`**
  - **輸入**：`id` 參數
  - **處理邏輯**：呼叫 `Recipe.get_by_id(id)`，並透過 `Tag.get_by_recipe_id(id)` 取出相關標籤。
  - **輸出**：若存在則渲染 `recipes/detail.html` 帶入食譜與標籤；若不存在則回傳 404 錯誤。

- **GET `/recipes/new`**
  - **輸入**：無
  - **處理邏輯**：確認使用者已登入。
  - **輸出**：渲染 `recipes/form.html`。

- **POST `/recipes/new`**
  - **輸入**：表單欄位 `title`, `ingredients`, `steps`, `image_url`, `tags` (選填，可逗號分隔)。
  - **處理邏輯**：呼叫 `Recipe.create()` 寫入食譜，如有標籤一併處理。
  - **輸出**：成功後轉址至 `/`。

- **GET `/recipes/<int:id>/edit`**
  - **輸入**：`id` 參數
  - **處理邏輯**：確認是否為該食譜擁有者。取出舊資料。
  - **輸出**：渲染 `recipes/form.html` 並傳遞舊資料供預填。

- **POST `/recipes/<int:id>/edit`**
  - **輸入**：`id` 參數，表單欄位。
  - **處理邏輯**：確認是否為擁有者，呼叫 `Recipe.update()` 進行變更。
  - **輸出**：轉址至 `/recipes/<id>`。

- **POST `/recipes/<int:id>/delete`**
  - **輸入**：`id` 參數
  - **處理邏輯**：確認是否為擁有者，呼叫 `Recipe.delete(id)` 刪除食譜。
  - **輸出**：轉址至 `/`。

## 3. Jinja2 模板清單

所有的模板檔案會建立在 `app/templates/` 中。

1. **`base.html`**：共通的基底 Layout 模板，包含網站導覽列 (Navbar)、Flash 訊息顯示區域、Footer 等，供其他頁面繼承。
2. **`auth/login.html`**：登入頁面表單。
3. **`auth/register.html`**：註冊頁面表單。
4. **`recipes/list.html`**：食譜列表（首頁與搜尋結果）。
5. **`recipes/detail.html`**：單一食譜的詳細閱讀。
6. **`recipes/form.html`**：食譜的新增/編輯表單，可依傳入的資料決定是新增還是編輯邏輯。

## 4. 路由骨架程式碼
請參考 `app/routes/` 內的 `.py` 檔案。
