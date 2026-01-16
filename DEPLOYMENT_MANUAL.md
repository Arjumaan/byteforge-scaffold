# Deployment & Database Guide

## 1. Automatic Deployment using Blueprint (`render.yaml`)

**Recommended:** This method uses the `render.yaml` file to automatically set up your Frontend, Backend, and Database in one go.

1. In the [Render Dashboard](https://dashboard.render.com/), click **New +** $\rightarrow$ **Blueprint**.
2. Connect your repository (**`Arjumaan/byteforge-scaffold`**).
3. Render will detect the `render.yaml` file and propose:
    * **`byteforge-api`**: The Backend Service.
    * **`byteforge-ui`**: The Frontend Static Site.
    * **`byteforge-db`**: The PostgreSQL Database.
4. Click **Apply**.
    * Render will automatically inject the `DATABASE_URL` into the backend.
    * Render will automatically inject the `VITE_API_URL` into the frontend.

*Note: In the blueprint, the Frontend and Backend are defined as separate "components" (services) but managed together. This is the correct way to handle a full-stack app.*

---

## 2. Manual Deployment (Separate Services)

If you prefer to setup services manually (instead of using the Blueprint):

### Backend (Web Service)

1. Click **New +** $\rightarrow$ **Web Service**.
2. Connect **`Arjumaan/byteforge-scaffold`**.
3. Name: `byteforge-api`.
4. **Root Directory**: `backend`.
5. **Runtime**: `Docker`.
6. **Environment Variables**:
    * `JWT_SECRET`: (Random String)
    * `ENCRYPTION_KEY`: (Random 32-byte string)
    * `DATABASE_URL`: (See below)
    * `ALLOWED_HOSTS`: `*`

### Frontend (Static Site)

1. Click **New +** $\rightarrow$ **Static Site**.
2. Connect **`Arjumaan/byteforge-scaffold`**.
3. Name: `byteforge-ui`.
4. **Root Directory**: `frontend`.
5. **Build Command**: `npm install && npm run build`.
6. **Publish Directory**: `dist`.
7. **Environment Variables**:
    * `VITE_API_URL`: `https://byteforge-api.onrender.com` (Your Backend URL).
8. **Rewrites**:
    * Source: `/*` $\rightarrow$ Destination: `/index.html`

---

## 2. Choosing a Database

### Option A: Render PostgreSQL (Easiest)

1. In Render Dashboard, click **New +** $\rightarrow$ **PostgreSQL**.
2. Name it `byteforge-db`.
3. Once created, copy the **Internal Connection String**.
4. Go to your **Backend Service** $\rightarrow$ **Environment**.
5. Set `DATABASE_URL` to that connection string.

### Option B: Aiven MySQL (External)

Yes, you can use MySQL (e.g., from Aiven, PlanetScale, or Azure).

1. Create your MySQL service on Aiven.
2. Get your credentials (Host, Port, User, Password, Database Name).
3. Construct the connection string for ByteForge:

    ```
    mysql+aiomysql://USER:PASSWORD@HOST:PORT/DBNAME
    ```

    *Note: We use `mysql+aiomysql` driver for async performance.*

4. Go to your **Backend Service** $\rightarrow$ **Environment**.
5. Set `DATABASE_URL` to this MySQL string.
    * *Example:* `mysql+aiomysql://avnadmin:password123@mysql-svc.aivencloud.com:12345/defaultdb`

**Note:** Both databases work seamlessly with ByteForge.
