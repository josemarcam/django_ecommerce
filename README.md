
## 📝 Table of Contents

- [Getting Started](#getting_started)
- [Usage](#usage)

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes

### Prerequisites

To install all dependences of this project, you just need to run:

```
pip install -r requirements.txt
```

### Installing

So first of all, you need to change your DB settings in pystore/settings.py. It`s very important that you create the DB with the same name as you put on settings.py. After that you just need to run the command below and the sistem will create the required tables on your DB.

```
python manage.py migrate
```

Last but not least, we need to create a super user, so we can login as admin, just run:

```
python manage.py createsuperuser
```

Now you can start the server with the command:

```
python manage.py runserver
```