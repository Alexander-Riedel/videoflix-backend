# 🎬 Videoflix – Django Backend for Streaming Platform

This is the backend for **Videoflix**, a Netflix-style video streaming platform where authenticated users can browse available content and stream videos using adaptive HLS playback.

Developed as a **training project**, this backend focuses on modern API architecture, secure authentication, and efficient media delivery.

> ❗ **Note:** This project is for learning and prototyping only. It is **not** production-ready and comes **without a license**.

---

## 🔐 Authentication

All endpoints are protected using **JWT-based authentication** via [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/).

After logging in, the client receives an **access** and **refresh token** via **HTTP-only cookies**.

Use these tokens for all further requests automatically. No manual headers needed.

---

## 🚀 Features

* ✅ **User registration, activation, login & logout**
* ♻️ **Token refresh** and **password reset** via email
* 📦 **Video upload with thumbnail and metadata**
* 📺 **HLS transcoding using ffmpeg and django\_rq**
* 📂 **Efficient segmented video delivery (m3u8 & ts files)**
* 🧪 **Full pytest test suite with isolated settings**

---

## 🧱 Tech Stack

* **Python** 3.10+  
* **Django** 5.2.4  
* **Django REST Framework** 3.16.0  
* **djangorestframework-simplejwt** 5.5.1 for JWT authentication  
* **django-cors-headers** 4.7.0 for CORS support  
* **django-redis** 6.0.0 (cache backend)  
* **django-rq** 3.0.1 for background jobs  
* **redis** 6.2.0 & **rq** 2.4.1 as the RQ broker  
* **psycopg2-binary** 2.9.10 for PostgreSQL connectivity  
* **ffmpeg-python** 0.2.0 for HLS conversion  
* **Pillow** 11.3.0 for image handling  
* **Whitenoise** 6.9.0 for static file serving  
* **gunicorn** 23.0.0 as WSGI server  
* **python-dotenv** 1.1.1 for environment variable loading  
* **pytest** 8.4.1 & **pytest-django** 4.11.1 for testing  
* **tzdata** 2025.2 for timezone support  
* **Miscellaneous**: asgiref, click, colorama, future, packaging, pluggy, iniconfig, Pygments, sqlparse

---

## ⚙️ Project Setup (Docker)

This project uses Docker and docker-compose for easy setup. The default web service is named **web**.

### 1. Clone the repository

```bash
git clone https://github.com/yourorg/videoflix-backend.git
cd videoflix-backend
```

### 2. Copy and configure environment variables

Create a `.env` file in the project root, based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` and fill in your values (e.g. database credentials, EMAIL_HOST, SECRET_KEY, FRONTEND_URL, etc.).

### 3. Build and start services

```bash
docker-compose up --build
```

This will:

1. Build the Docker images  
2. Start the **web** (Django) service  
3. Start the **db** (PostgreSQL) service  
4. Start the **redis** service for caching and RQ  

### 4. Apply database migrations

In a new terminal, run:

```bash
docker-compose exec web python manage.py migrate
```

### 5. (Optional) Create a superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

Follow the prompts to set email and password.

### 6. Access the application

- **API**: http://localhost:8000/api/  
- **Admin**: http://localhost:8000/admin/  

Stop the services with **CTRL+C** in the `docker-compose` terminal, or:

```bash
docker-compose down
```

---

## 📚 Endpoints

| Endpoint                                                  | Method | Description                          |
| --------------------------------------------------------- | ------ | ------------------------------------ |
| `/api/register/`                                          | POST   | Register new user                    |
| `/api/activate/<uidb64>/<token>/`                         | GET    | Activate new user                    |
| `/api/login/`                                             | POST   | Log in (returns JWT in cookies)      |
| `/api/logout/`                                            | POST   | Logout and clear cookies             |
| `/api/token/refresh/`                                     | POST   | Refresh access token via cookie      |
| `/api/password_reset/`                                    | POST   | Send password reset mail             |
| `/api/password_confirm/<uidb64>/<token>/`                 | POST   | Confirm new password                 |
| `/api/video/`                                             | GET    | List all available videos            |
| `/api/video/<int:movie_id>/<str:resolution>/index.m3u8`   | GET    | Fetch master playlist for streaming  |
| `/api/video/<int:movie_id>/<str:resolution>/<str:segment>/`   | GET    | Fetch video segment for HLS playback |

---

## 🧪 Testing

Tests are implemented using **pytest** with a separate `settings_test.py` and an in-memory database.

### Run tests:

```bash
pytest
```

### Sample tested features:

* Video listing
* Manifest retrieval (m3u8)
* Segment retrieval (ts)
* Auth flow

---

## 📁 Project Structure

```
videoflix-backend/
├── auth_app/          # Registration, login, activation, reset
├── video_app/         # Video models, views, streaming logic
├── core/              # Main Django settings + URLs
├── templates/         # Email templates
├── media/             # Uploaded and transcoded files
├── manage.py          # Django CLI entry point
├── requirements.txt   # Dependencies
├── settings_test.py   # Pytest test configuration
└── pytest.ini         # Pytest environment config
```

---

## ❌ License

This repository is for educational use only. **No license is provided.**

---

## 🙋 Contributing

This is a training repository. Contributions are welcome but not expected.
