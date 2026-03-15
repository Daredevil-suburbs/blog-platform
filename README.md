# 📝 Blog Platform

A full-featured blog platform built with **Django** and **PostgreSQL**. Users can register, write, edit, and publish blog posts with rich text editing, comments, likes, categories, and tags.

---

## ✨ Features

- **User Authentication** — Register, login, logout with profile pages
- **Rich Text Editor** — Summernote WYSIWYG editor for writing posts
- **Post Management** — Create, edit, delete posts with draft/published status
- **Categories & Tags** — Organize posts with categories and django-taggit tags
- **Comments** — Authenticated users can comment on posts
- **Likes** — AJAX-powered like/unlike with live count updates
- **Search & Filter** — Search posts by title/body, filter by category
- **Dashboard** — Personal dashboard to manage your posts
- **Public Profiles** — View any author's profile and posts
- **Pagination** — Posts paginated across all views
- **Admin Panel** — Full Django admin with Summernote integration
- **Docker Ready** — `docker-compose.yml` included for easy setup
- **WhiteNoise** — Static file serving for production

---

## 🗂️ Project Structure

```
blog-platform/
├── blog/                   # Core blog app
│   ├── models.py           # Post, Category, Comment, Like
│   ├── views.py            # All blog views
│   ├── forms.py            # PostForm, CommentForm
│   ├── urls.py             # Blog URL patterns
│   └── admin.py            # Admin config with Summernote
├── users/                  # Auth & profile app
│   ├── models.py           # Profile (extends User)
│   ├── views.py            # Register, profile, public profile
│   ├── forms.py            # Register, update forms
│   └── urls.py             # User URL patterns
├── blog_platform/          # Project config
│   ├── settings.py
│   └── urls.py
├── templates/              # All HTML templates
│   ├── base.html
│   ├── blog/
│   └── users/
├── static/css/main.css     # Custom styles
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

---

## 🚀 Quick Start

### Option 1 — Local Setup

```bash
# 1. Clone and enter the repo
git clone https://github.com/yourusername/blog-platform.git
cd blog-platform

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your DB credentials and secret key

# 5. Create PostgreSQL database
createdb blogdb

# 6. Run migrations
python manage.py migrate

# 7. Create superuser
python manage.py createsuperuser

# 8. Start the server
python manage.py runserver
```

Visit: http://127.0.0.1:8000

### Option 2 — Docker Compose

```bash
# Copy and edit .env
cp .env.example .env

# Start all services (PostgreSQL + Django)
docker-compose up --build

# In another terminal, create superuser
docker-compose exec web python manage.py createsuperuser
```

Visit: http://localhost:8000

---

## ⚙️ Environment Variables

| Variable      | Description              | Default       |
|---------------|--------------------------|---------------|
| `SECRET_KEY`  | Django secret key        | (required)    |
| `DEBUG`       | Debug mode               | `True`        |
| `DB_NAME`     | PostgreSQL database name | `blogdb`      |
| `DB_USER`     | PostgreSQL user          | `postgres`    |
| `DB_PASSWORD` | PostgreSQL password      | (required)    |
| `DB_HOST`     | PostgreSQL host          | `localhost`   |
| `DB_PORT`     | PostgreSQL port          | `5432`        |

---

## 🛠️ Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Backend    | Django 5.0              |
| Database   | PostgreSQL + psycopg2   |
| Frontend   | Bootstrap 5 + Font Awesome |
| Rich Text  | Summernote              |
| Tags       | django-taggit           |
| Forms      | django-crispy-forms     |
| Static     | WhiteNoise              |
| Server     | Gunicorn                |
| Container  | Docker + docker-compose |

---

## 📌 API Endpoints

| URL                        | View            | Auth Required |
|----------------------------|-----------------|---------------|
| `/`                        | Home feed       | No            |
| `/post/new/`               | Create post     | Yes           |
| `/post/<slug>/`            | Post detail     | No            |
| `/post/<slug>/edit/`       | Edit post       | Yes (author)  |
| `/post/<slug>/delete/`     | Delete post     | Yes (author)  |
| `/post/<slug>/like/`       | Toggle like     | Yes           |
| `/post/<slug>/comment/`    | Add comment     | Yes           |
| `/dashboard/`              | User dashboard  | Yes           |
| `/users/register/`         | Register        | No            |
| `/users/login/`            | Login           | No            |
| `/users/profile/`          | Edit profile    | Yes           |
| `/users/profile/<username>/` | Public profile | No           |
| `/admin/`                  | Admin panel     | Staff only    |

---

## 📄 License

MIT License — free to use and modify.
