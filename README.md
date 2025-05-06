Starting the Application
To start the django-Godu application, follow these steps:

Clone the Repository:

Run the following command to clone the repository:
bash
git clone https://github.com/herbs61/django-Godu.git
cd django-Godu
Set Up the Environment:

Create a virtual environment and activate it:
bash
python3 -m venv venv
source venv/bin/activate  # For Linux/MacOS
venv\Scripts\activate     # For Windows
Install the required dependencies:
bash
pip install -r requirements.txt
Configure the Database:

Ensure you have MySQL installed and running.
Update the database configuration in godu/settings.py (if necessary):
Python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "db_godu",
        "USER": "root",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
Apply migrations:
bash
python manage.py makemigrations
python manage.py migrate
Run the Development Server:

Start the server:
bash
python manage.py runserver
Access the application in your browser at http://127.0.0.1:8000/.
Optional: Create a Superuser

To access the Django admin panel, create a superuser:
bash
python manage.py createsuperuser
Navigate to http://127.0.0.1:8000/admin/ and log in with the credentials.
