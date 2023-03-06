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

#

### Running the App

--> To run the App in testing mode, we use :

```bash
python manage.py runserver --settings pendaftaran_pasien.test_settings
```

--> To run the App in production mode, we use :

```bash
python manage.py runserver --settings pendaftaran_pasien.settings
```

--> To run the tailwind, we use :

```bash
python manage.py tailwind start
```

If there is error when running the tailwind command, you need to change the NPM_BIN_PATH that is located in settings.py to your npm path
