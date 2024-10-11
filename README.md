<p align="center"><img width=100% src="src/static/images/logo.png"></p>

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![CI](https://github.com/Ferlola/auction/actions/workflows/ci.yml/badge.svg)](https://github.com/Ferlola/auction/actions/workflows/ci.yml)

<p align="center">
  <a href="README.md#-features">Features</a> 🔸
  <a href="README.md#-requirements">Requirements</a> 🔸
  <a href="README.md#-configuration">Configuration</a> 🔸
  <a href="README.md#-installation">Installation</a>
</p>

Contributions are welcome! ❤️

### 📈 <span style="color: blue;">Purpose</span>:
------------------------------------------------------
This is a personal project with the purpose to improve my skills with Django, as I was building it I was adding more features and for now this is the result, I really appreciate if someone is interested in contributing to this project, as it helps me improve my skills.<br />
If I can also help someone in some way with this project, all the better.<br />

Fernando Lozano<br />
fer.lozano10@hotmail.com

### 📎 <span style="color: blue;">Features</span>:
-------------------------------------------------------
#### Control Panel.
- Set site name.
- Set site domain.
- Set site theme.
- Set if auctioneer can update item.
- Set if auctioneer can choose start and end date.
- Set maximum number of image uploads.
- Set auto-increment of bids or let bidder choose bid amount for each item.
- Set rate.
- Set day and time of weekly email report of new items and completed payments.
- Set time of daily email report of new items and completed payments.
- Create and delete categories.
- Create and delete subcategories.
- Update and delete items.
- Get bidding history.
- Get list of unsubscribed to newsletters.
- Get list of registered users.
- Get payments details of winning bidders.
#### Users.
- Search field for items, categories and subcategories.
- Automatic creation of pdf invoice.
- Download of item details on pdf.
- Get bidding history.
- Seller inquiry form about the item.
- Admin inquiry form.
- Buy now option.
- Slideshow.
- Profile settings.
- Forgot passsword.
- Auction end countdown.
- User badges.
- Like and dislike button.
- Email to confirm email address when user registers.
- Email to admin to review item before posting.
- Email to bidder to confirm bid.
- Email to seller to inform about new bid.
- Email to other bidders about last bid on the same item.
- Email informing bidder that they have won the auction.
- Email to seller if item has not had any bids, when auction has ended.
- Email to all registered users with information about new items.
- Payments via Stripe.
- Payments via Paypal.


### 🔍 <span style="color: blue;">Requirements</span>:
--------------------------------------------------------
- virtual environment (highly recommended)<br />
- python<=3.12<br />
- docker <br />
- (optional), stripe developers account<br />
- (optional), paypal developers account<br />
- (optional), test email account (I have used mailtrap.io)<br />

### 📃 <span style="color: blue;">Configuration</span>:
---------------------------------------------------------
- Open a terminal window in your favorite folder and clone project.
```
$ git clone https://www.github.com/Ferlola/auction.git
```
<details>
    <summary> .envs/.local/.django file configuration. </summary>

```
#email, only if you had chosen to receive email through the email testing service
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_PORT = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
#EMAIL_USE_SSL = False
#EMAIL_TIMEOUT = None

#Paypal
PAYPAL_CLIENT_ID = Your paypal client id
PAYPAL_SECRET_ID = Your secret id

#stripe
STRIPE_SECRET_KEY = 'Your stripe secret key'
STRIPE_PUBLIC_KEY = 'Your stripe public key'
```
</details>
<details>
    <summary>.envs/.local/.postgres file configuration. </summary>

```
POSTGRES_HOST=postgres
POSTGRES_DB=auction  # or select another data base name
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password  # change your_password with your real password
```
</details>
<details>
    <summary>Receive email by email testing. </summary>

```
# config/settings/local.py
#"DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend",
"DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
```
</details>

### 🚀 <span style="color: blue;">Installation</span>:
- Create virtual environment.
```
# change 'python3.12' with your python version
$ python3.12 -m venv .venv
```

- Activate virtual environment.
```
$ source .venv/bin/activate
```
- Install cookiecutter and requeriments.
```
(.venv) $ pip install "cookiecutter>=1.7.0"
(.venv) $ pip3 install -r requirements/local.txt
```
- Create database.<br />

```
# Change 'auction' if you had selected another database name.
(.venv) $ createdb --username=postgres auction
```
- Export data base and celery.<br />

```
# Change 'your_password' with your real password
# Change 'auction' if you had selected another database name
(.venv) $ export DATABASE_URL=postgres://postgres:your_password@127.0.0.1:5432/auction
(.venv) $ export CELERY_BROKER_URL=redis://localhost:6379/0
```
- Create image and containers, (this will take a while).
```
# create image, optional, note the dot at the of the line
(.venv) $ docker build -t test_auction:0.0.1 -f ./compose/local/django/Dockerfile .
# build the container
(.venv) $ docker compose -f docker-compose.local.yml up -d --build
```
- Create super user.
```
(.venv) $ docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser
```
- Run the project.
```
(.venv) $ docker compose -f docker-compose.local.yml up -d
(.venv) $ docker compose -f docker-compose.local.yml logs -f
```
- Open browser.

<pre><a href="http://localhost:8000">http://localhost:8000</a></pre>

- Stop service.
```
(.venv) $ Ctrl + c
(.venv) $ docker compose -f docker-compose.local.yml down
(.venv) $ deactivate
$
```
