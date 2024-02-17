Kelompok 7

# nama aplikasi
Aplikasi Login Employee dan Manajemen User

# Deskrpsi applikasi

Aplikasi Microservice Login dan Manajemen USER
di dalam aplikasi terdapat sistem CRUD / Create, Read, Update, Delete

## Login
terdapat dua inputan yang dimasukkan yakni :
Username dan Password

## Manajemen User
Terdapat enam inputan yakni :
- username
- password
- first_name
- last_name
- gender
- status

## Create User
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT, 
    username VARCHAR(80) NOT NULL UNIQUE,
    password VARCHAR(256) NOT NULL, 
    first_name VARCHAR(25) NOT NULL,
    last_name VARCHAR(35) NOT NULL,
    gender CHAR(15), NOT NULL,
    status VARCHAR(15) NOT NULL 
);

## Update User
UPDATE users
SET 
    first_name = 'NewFirstName',
    last_name = 'NewLastName',
    gender = 'NewGender',
    status = 'NewStatus'
WHERE
    username = 'existing_username';

## Read User
SELECT * FROM users;

# Delete User
DELETE FROM users WHERE username = 'username_to_delete';


## Langkah-Langkah Running Aplikasi

1. Setelah clone projek dan membukanya
2. Buat Database dengan nama db_employee
3. Sesuaikan config database anda di app.py
    ```bash
      app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/db_employee'
    ```

4. Install Python 3

   [Download python](https://www.python.org/downloads/0)


5. Install Virtual Environment

    ```bash
    Set-ExecutionPolicy Unrestricted -Scope Process
    pip3 install virtualenv
    ```

6. Create Virtual Environment di path ini

    ```bash
    python -m venv venv
    ```


7. Aktifasikan Virtual Environment

    ```bash
    venv\Scripts\activate
    ```

    Nonaktifkan
    ```bash
    deactivate
    ```

8. Install requirement dengan command:
    ```bash
    pip install -r requirements.txt
    ```
    
9. Makemigrations Database
    ```bash
    flask db stamp head
    flask db migrate -m 'your descriptive message'
    flask db upgrade
    ```
    
10. Jalan kan server
    ```bash
    flask run
    ```
