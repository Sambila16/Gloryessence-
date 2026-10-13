# Shop Ledger (Django)

Setup
1. python -m venv venv  &&  venv\Scripts\activate   (Windows)
2. pip install django
3. python manage.py migrate
4. python manage.py createsuperuser   (this account is the Admin)
5. python manage.py runserver  ->  open http://127.0.0.1:8000

Admin logs in, registers products, then adds cashiers on the Cashiers page.
Set SECRET_KEY and DEBUG=0 in the environment before putting it online.


# Glory Essence

**A mini shop management system for women's valuable jewelry.**

Glory Essence helps a jewelry seller manage products, set prices, track sales, and automatically split profit between business capital and new profit. It replaces a handwritten notebook with a clean, professional web system.

> Brand identity: a gold "G" logo topped with a perfume-bottle cap and a rose.

---

## Table of Contents

1. [Features](#features)
2. [How the Profit Split Works](#how-the-profit-split-works)
3. [Data Tracked](#data-tracked)
4. [User Roles](#user-roles)
5. [Design](#design)
6. [Tech Stack](#tech-stack)
7. [Installation](#installation)
8. [Usage](#usage)
9. [Deployment (Free Hosting)](#deployment-free-hosting)
10. [Project Structure](#project-structure)
11. [Roadmap](#roadmap)
12. [Author](#author)

---

## Features

- **Product management**: add products by type (rings, necklaces, bracelets, earrings, and more women's jewelry categories), each with a picture.
- **Delete option**: remove products that are no longer sold.
- **Pricing**: the seller sets the selling price for every product.
- **Automatic profit calculation**: profit is the selling price minus the buying price.
- **70/30 profit split**: profit is divided automatically into capital and new profit.
- **Daily sales record**: payment method and customer location for every sale.
- **Regular customers list**: names, contacts, and location.
- **Automatic login page**: users are directed to login before using the system.
- **Admin page**: add items and manage users.
- **Monthly evaluation**: a summary of performance at the end of each month.
- **Professional welcome page** (`index.html`) leading to login.

---

## How the Profit Split Works

For every sale:

```
Profit          = Selling Price - Buying Price
New Capital     = 70% of Profit    (reinvested into the business)
Business Profit = 30% of Profit    (new profit for the owner)
```

**Example**

| Item | Amount |
|------|--------|
| Buying price | 50,000 |
| Selling price | 80,000 |
| Profit | 30,000 |
| 70% to capital | 21,000 |
| 30% new profit | 9,000 |

---

## Data Tracked

The system follows the layout of the original handwritten notebook.

**Products table**

| Field | Description |
|-------|-------------|
| Product type / name | Category and item name |
| Picture | Product image |
| Quantity | Stock available |
| Buying price | Cost price |
| Sales price | Selling price |
| New capital | 70% of profit |
| Business profit | 30% of profit |
| Total | Overall total |

**Daily sales**

| Field | Description |
|-------|-------------|
| Date | Day of sale |
| Product | Item sold |
| Payment method | Cash, mobile money, etc. |
| Customer location | Where the customer is from |

**Regular customers**

| Field | Description |
|-------|-------------|
| Name | Customer name |
| Contact | Phone number |
| Location | Customer location |

**Monthly evaluation**: totals for sales, capital, and profit at the end of each month.

---

## User Roles

| Role | Can do |
|------|--------|
| **Seller** | Log in, add products with pictures, delete products, set selling prices, record sales, view profit and capital |
| **Admin** | Everything the seller can do, plus add items and create or manage users |

---

## Design

- Professional, elegant, English-language interface.
- Inspired by modern jewelry-store websites.
- Dark editorial model photo on the login page.
- Logo shown in the navbar.
- Welcome page with a jewelry photo leading into login.
- Wide range of women's product categories.
- Simple frontend built with HTML, CSS, and JavaScript.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django (Python) |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite (development) |
| Media | Django media files for product pictures |
| Hosting | Free hosting (see below) |

---

## Installation

**Requirements:** Python 3.10 or newer, and pip.

```bash
# 1. Clone the repository
git clone <your-repository-url>
cd glory-essence

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install django pillow

# 4. Apply database migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create the admin account
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

---

## Usage

1. Open the welcome page and click through to **Login**.
2. Sign in with your seller or admin account.
3. **Add products**: choose the type, upload a picture, enter quantity, buying price, and selling price.
4. **Record sales**: enter the product, payment method, and customer location.
5. **Review profit**: see the automatic 70% capital and 30% profit split.
6. **Manage customers**: save regular customers with their contacts and location.
7. **Admin only**: add items and users from the admin page.
8. At the end of the month, review the **monthly evaluation**.

---

## Deployment (Free Hosting)

The project can run live on a free Django-friendly host such as PythonAnywhere or Render.

Before deploying:

1. Set `DEBUG = False` and configure `ALLOWED_HOSTS` in `settings.py`.
2. Keep the `SECRET_KEY` out of the repository (use an environment variable).
3. Configure static files (`STATIC_ROOT`) and run `python manage.py collectstatic`.
4. Configure media storage so uploaded product pictures are kept.
5. Add a `requirements.txt` (`pip freeze > requirements.txt`).
6. Run migrations on the server and create the admin account.

---

## Project Structure

```
glory-essence/
├── manage.py
├── requirements.txt
├── glory_essence/        # Project settings and URLs
├── shop/                 # Products, sales, customers, profit logic
├── templates/            # index.html, login, dashboard pages
├── static/               # CSS, JavaScript, logo
├── media/                # Uploaded product pictures
└── README.md
```

> Adjust folder names to match your actual project.

---

## Roadmap

- [x] Product management with pictures and delete option
- [x] 70/30 profit split
- [x] Login page and admin page
- [x] Professional redesign with welcome page
- [ ] Deploy live on free hosting
- [ ] Monthly evaluation report (printable)
- [ ] Sales charts and low-stock alerts

---

## Author

**Denisi Sambila**
Information Systems Management, Ardhi University, Dar es Salaam, Tanzania
GitHub: [Sambila16](https://github.com/Sambila16)

---

*Glory Essence: elegance in every piece.*
