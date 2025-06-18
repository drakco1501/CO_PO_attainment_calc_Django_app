COPO Attainment System

The COPO Attainment System is a web-based platform designed for colleges to calculate and manage Course Outcomes (CO) and Program Outcomes (PO) mappings.

Features
- User-friendly interface for CO and PO calculation.
- Admin panel for managing teachers and data.
- Secure login for teachers.

---

Installation

Follow these steps to set up and run the project:

1. Create a Python Virtual Environment
To isolate dependencies and ensure smooth setup:

    python -m venv env

Activate the virtual environment:
- Windows:
    .\env\Scripts\activate
- Linux/Mac:
    source env/bin/activate

---

2. Install Required Dependencies

Download the necessary libraries listed in `requirements.txt`:

    pip install -r requirements.txt

---

3. Apply Migrations

Run the following commands to apply database migrations:

    python manage.py makemigrations
    python manage.py migrate

---

4. Create a Superuser

Create an admin user for accessing the Django admin panel:

    python manage.py createsuperuser

Follow the prompts to set the username, email, and password.

---

5. Add Teachers in the Admin Panel

1. Log in to the admin panel at:
    http://127.0.0.1:8000/admin/

2. Use the superuser credentials to log in.

3. Navigate to the Teachers section and add teachers with their credentials.

---

6. Teacher Login

1. Go to the login page:
    http://127.0.0.1:8000/login/

2. Enter the credentials for a teacher account.

3. Start using the platform for COPO calculation!

---

Contributing

If you'd like to contribute, please fork the repository and create a pull request.

---

License

This project is licensed under the MIT License.
