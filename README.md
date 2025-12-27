# PlanGo Project

PlanGo is a full-stack web application that combines a Django backend and an Angular frontend. The backend handles data management and API services, while the frontend provides a dynamic and interactive user interface.

---

## Project Structure

### Backend (Django)

The backend is built with Django and provides API services and database management.

#### Setup

1. Navigate to the backend directory:
    ```bash
    cd PlanGo_backend
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the development server:
    ```bash
    python manage.py runserver
    ```

4. Access the backend at: [http://localhost:8000/](http://localhost:8000/)

#### Exporting Database Data

To export your database data to a JSON file, use Django's `dumpdata` command:

```bash
python manage.py dumpdata --indent 4 > initial_data.json
```

#### Importing Data into the Database (Optional)

If you need to load data from `initial_data.json` into the database, use the `loaddata` command:

```bash
python manage.py loaddata initial_data.json
```

---

### Frontend (Angular)

The frontend is built with Angular and provides a dynamic user interface.

#### Setup

1. Navigate to the frontend directory:
    ```bash
    cd PlanGo_frontend
    ```

2. Install dependencies:
    ```bash
    npm install
    ```

3. Run the development server:
    ```bash
    npm start
    ```

4. Access the frontend at: [http://localhost:4200/](http://localhost:4200/)