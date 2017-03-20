# Flask-Cloudant
[![Build Status](https://travis-ci.org/porthunt/flask-cloudant.svg?branch=master)](https://travis-ci.org/porthunt/flask-cloudant) [![Code Climate](https://codeclimate.com/github/porthunt/flask-cloudant/badges/gpa.svg)](https://codeclimate.com/github/porthunt/flask-cloudant)

Adds Cloudant support to Flask. Built on top of [python-cloudant](https://github.com/cloudant/python-cloudant).

### Installing

```
pip install flask-cloudant
```

### Configuring

Use your Cloudant credentials on the Flask config. Set your info like this:

```python
CLOUDANT_USER = "your-cloudant-username"
CLOUDANT_PWD = "your-cloudant-password"
CLOUDANT_ACCOUNT = "your-cloudant-account"
```

> If you don't define your `CLOUDANT_ACCOUNT`, Flask-Cloudant will use the `CLOUDANT_USER` as the account.

### Let's use it

```python
from flask import Flask
from flask_cloudant import FlaskCloudant


app = Flask(__name__)
app.config.from_object('config')
store_cloudant = FlaskCloudant(app)
```
