# ⚡ ByteForge Scaffold

> A modern, production-ready Web Application Penetration Testing Framework.

ByteForge Scaffold is a high-performance, modular framework designed for automated security assessments. It combines the power of **FastAPI**, **React**, and **Celery** to provide a seamless experience from scanning to reporting.

---

## 🎨 Premium Features

-   **Modern Dashboard**: Glassmorphism UI with real-time statistics.
-   **Automated Scanning**: Integration placeholders for Nuclei, Custom Crawlers, and Active Scanners.
-   **Job Management**: Distributed task queue powered by Celery and Redis.
-   **Security First**: Built-in JWT authentication, RBAC-ready roles, and secure middleware.
-   **Responsive Design**: Fully optimized for all device sizes with a sleek dark mode.

---

## 🛠️ Technology Stack

### Backend
-   **FastAPI**: High-performance Python API framework.
-   **SQLModel**: Elegant database interaction (SQLAlchemy + Pydantic).
-   **Alembic**: Robust database migrations.
-   **Celery & Redis**: Scalable background task processing.
-   **PostgreSQL**: Reliable relational data storage.

### Frontend
-   **React & TypeScript**: Type-safe component architecture.
-   **Vite**: Lightning-fast development and build tooling.
-   **React Query**: Efficient server-state management.
-   **Framer Motion**: Smooth, premium animations.
-   **Lucide React**: Clean and consistent iconography.

---

## 🚀 Getting Started

### Option A: Docker (Recommended)
The fastest way to get started. Ensures all dependencies and infrastructure (Postgres, Redis) are ready.
```bash
docker compose up --build
```

### Option B: Local Setup (Non-Docker)
For those who prefer native installation.
1. Follow the [Local Setup Guide](./LOCAL_SETUP.md) for detailed instructions.

---

## 📍 Project Structure

```text
├── backend/            # FastAPI Application
│   ├── app/            # Core logic, routers, models
│   ├── alembic/        # DB Migrations
│   └── tests/          # Pytest suite
├── frontend/           # React Application
│   ├── src/            # Components, pages, state
│   └── public/         # Static assets
└── docker-compose.yml  # Orchestration
```

---

## 🔒 Access
-   **Frontend**: [http://localhost:5173](http://localhost:5173)
-   **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
-   **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

## 📝 License
This project is open-source. See the LICENSE for more details.

---

*Made with ❤️ by Arjumaan*
