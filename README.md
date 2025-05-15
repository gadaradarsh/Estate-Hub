# 🏡 Estate-Hub : Your Real Estate Hub

Welcome to **Estate**, the ultimate Django-powered platform where real estate dreams meet cutting-edge technology! Whether you’re a **Buyer** exploring your next dream home, a **Seller** listing your prized property, or an **Admin** managing it all seamlessly, Estate has got you covered. 🚀

---

## 🌟 Features You'll Love

### 🔑 **Role-Based User Management**
- **Admins**: Manage listings, users, and everything in between.
- **Sellers**: Showcase properties with stunning details and images.
- **Buyers**: Browse listings, leave reviews, and save your favorites.

### 🏘️ **Property Listings**
- Add detailed property information: 🛏️ bedrooms, 🛁 bathrooms, 📏 square footage, and 📍 addresses.
- Upload high-quality images to make listings stand out.

### ⭐ **Reviews & Ratings**
- Share your thoughts with star-based ratings and comments.
- One property, one review per user. Fair and square!

### ❤️ **Favorites**
- Save your favorite properties for later. Never lose track of that dream home.

---

## 🛠️ Tech Stack: Built to Impress

- **Backend**: Django 4.2.19
- **Database**: SQLite (Ready for PostgreSQL in production 🚀)
- **Frontend**: Django Templates (Customizable!)
- **Media Handling**: User-uploaded property images with Django’s media management.

---

## 🚀 Quick Start: Get Estate Running in Minutes

### Step 1️⃣: Clone and Navigate
```bash
git clone https://github.com/username/estate.git
cd estate
```
### Step 2️⃣: Install the Magic

```bash

pip install -r requirements.txt
```
### Step 3️⃣: Configure Secrets


```base
SECRET_KEY=your_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```
### Step 4️⃣: Set Up the Database
```bash

python manage.py migrate
``` 
###  Step 5️⃣: Fire Up the Server
```bash
python manage.py runserver
```
---
Estate/<br>
├── Estate/                     # Main project directory<br>
│   ├── __init__.py             # Marks this as a Python package<br>
│   ├── asgi.py                 # ASGI configuration for async support<br>
│   ├── settings.py             # Project settings (database, installed apps, middleware, etc.)<br>
│   ├── urls.py                 # Root URL configurations<br>
│   ├── wsgi.py                 # WSGI configuration for deployment<br>
│<br>
├── hub/                        # Main application directory<br>
│   ├── migrations/             # Database migration files<br>
│   ├── static/                 # Static files (CSS, JavaScript, images)<br>
│   ├── templates/              # HTML templates for views<br>
│   ├── admin.py                # Admin interface customizations<br>
│   ├── apps.py                 # App configuration<br>
│   ├── models.py               # Application models (CustomUser, Listing, Review, Favorite)<br>
│   ├── tests.py                # Unit tests for the app<br>
│   ├── views.py                # View logic for handling requests<br>
│<br>
├── static/                     # Project-wide static files<br>
│<br>
├── template/                   # Project-wide HTML templates<br>
│<br>
├── db.sqlite3                  # SQLite database file<br>
│<br>
├── manage.py                   # Django's command-line utility<br>

# Key Components
## Estate:<br>

Core project settings, URLs, and configuration files for deployment.<br>

## hub:<br>

Main app that manages all functionalities like listings, reviews, user management, and favorites.<br>

## static:<br>

Holds static assets like CSS, JavaScript, and images used across the project.<br>

## template:<br>

Stores HTML templates for rendering views.<br>

## manage.py:<br>


---

## 🙋‍♂️ Author
Made with 🧠&🫀 by Darsh Gadara
---
## 📄LICENSE
 This project is licensed for free for personal and commercial use. See LICENSE for details.
