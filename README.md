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

* **Python** 3.12+
* **Django** 5.x
* **Django REST Framework**
* **SimpleJWT** for authentication
* **django\_rq** for background jobs
* **ffmpeg** for media conversion
* **pytest** for testing
* **SQLite** for dev DB (easy to swap)

---

## ⚙️ Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourname/videoflix-backend.git
cd videoflix-backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 6. Run the dev server

```bash
python manage.py runserver
```

---

## 📚 API Endpoints (selected)

| Endpoint                                    | Method | Description                          |
| ------------------------------------------- | ------ | ------------------------------------ |
| `/api/registration/`                        | POST   | Register new user                    |
| `/api/login/`                               | POST   | Log in (returns JWT in cookies)      |
| `/api/logout/`                              | POST   | Logout and clear cookies             |
| `/api/token/refresh/`                       | POST   | Refresh access token via cookie      |
| `/api/video/`                               | GET    | List all available videos            |
| `/api/video/<id>/<resolution>/index.m3u8`   | GET    | Fetch master playlist for streaming  |
| `/api/video/<id>/<resolution>/<segment>.ts` | GET    | Fetch video segment for HLS playback |

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
