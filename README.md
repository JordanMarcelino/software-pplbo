<div align="center">

# Sistem Pendaftaran Antrian Klinik

</div>

### Cloning the repository

--> Clone the repository using command below :

```bash
git clone https://github.com/JordanMarcelino/software-pplbo.git
```

--> Move into the directory :

```bash
cd software-pplbo
```

--> Create a virtual environment :

```bash
# Install virtualenv first
pip install virtualenv

# Then create virtual environment
virtualenv .venv
```

--> Activate the virtual environment :

```bash
.venv\Scripts\activate
```

--> Install the requirements :

```bash
pip install -r requirements.txt
```

### Running the App

Before running the app, make sure you have downloaded <a href='https://www.postgresql.org/'>PostgreSQL</a> and created two database with name <b>sistem_antrian_klinik</b> and <b>sistem_antrian_klinik_test</b>
</br>

--> Make .env file :

```bash
touch .env
```

--> Copy this into .env file and fill it with your config :

```
DB_NAME=sistem_antrian_klinik
DB_NAME_TEST=sistem_antrian_klinik_test
DB_USER=<user>
DB_PASSWORD=<password>
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=<secret_key>
EMAIL_HOST_USER=<gmail>
EMAIL_HOST_PASSWORD=<app_password>
RECAPTCHA_PUBLIC_KEY=<site_key>
RECAPTCHA_PRIVATE_KEY=<secret_key>
```

#### User

Database user name

#### Password

Database user password

#### Secret Key

Django secret key

#### Gmail

Gmail account

#### App Password

Gmail app password, not gmail account password. To create this password go to google account settings, security, app password, create an app password and choose email option for application and others for devices, then copy the password

#### Site Key

Recaptcha site key, to get this key, register a new site at https://www.google.com/recaptcha/admin/create

#### Secret Key

Recaptcha secret key

--> To run the tailwind, we use :

```bash
# Install the dependencies
python manage.py tailwind install

# Run the tailwind
python manage.py tailwind start
```

If there is error when running the tailwind command, you need to change the NPM_BIN_PATH that is located in settings.py to your npm path

--> To run the database migrations, we use :

```bash
# Testing mode
python manage.py makemigrations --settings pendaftaran_pasien.test_settings
python manage.py migrate --settings pendaftaran_pasien.test_settings

# Production mode
python manage.py makemigrations --settings pendaftaran_pasien.settings
python manage.py migrate --settings pendaftaran_pasien.settings
```

--> To run the App, we use :

```bash
# Testing mode
python manage.py runserver [port] --settings pendaftaran_pasien.test_settings

# Production mode
python manage.py runserver [port] --settings pendaftaran_pasien.settings
```

You can now access the server at http://localhost:[port]

### TL;DR command list

```bash
git clone https://github.com/JordanMarcelino/software-pplbo.git
cd software-pplbo
pip install virtualenv
virtualenv .venv
.venv\Scripts\activate
pip install -r requirements.txt
touch .env
python manage.py tailwind install
python manage.py tailwind start
python manage.py makemigrations --settings pendaftaran_pasien.settings
python manage.py migrate --settings pendaftaran_pasien.settings
python manage.py runserver [port] --settings pendaftaran_pasien.settings
```
