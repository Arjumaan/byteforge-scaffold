# Render Deployment Setup

## 1. Backend Service (`byteforge-api`)

Go to your Dashboard > **byteforge-api** > **Environment**.
Add the following Environment Variables:

| Key | Value | Description |
|-----|-------|-------------|
| `JWT_SECRET` | `change_this_to_a_random_string` | Secret for user sessions. |
| `ENCRYPTION_KEY` | `fC07bXUlylhQmi0Jk2xqhZIjrkSUsZJWTNHfk8dBjeY=` | Key for encrypting sensitive target data. **Keep this safe!** |
| `ALLOWED_HOSTS` | `*` | Allow Render domains. |
| `ALLOWED_ORIGINS` | `*` | Allow Frontend access. |
| `Use_Threading` | `True` | (Optional) Bypass Redis/Celery if you don't have Redis service. |

> **Note:** For the database, Render usually provides a `DATABASE_URL` automatically if you attach a Postgres database. If you stay on the free tier without Postgres, it will use SQLite (data will be lost on restart).

## 2. Frontend Service (`byteforge-ui`)

Go to your Dashboard > **byteforge-ui** > **Environment**.
Add the following Environment Variable:

| Key | Value | Description |
|-----|-------|-------------|
| `VITE_API_URL` | `https://your-backend-url.onrender.com` | Link to your deployed Backend API. |

> **Important:** You must deploy the Backend FIRST to get its URL, then add it here and redeploy the Frontend.
