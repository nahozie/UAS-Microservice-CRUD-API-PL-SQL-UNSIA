Kelompok 7

# Aplikasi Microservices CRUD API PL/SQL UNSIA
Aplikasi Microservice CRUD Employee dengan Trigger Log

# Deskripsi Aplikasi
Aplikasi Flask ini menyediakan API sederhanan untuk mengelola informasi karyawan / employee dengan operasi CRUD (Create, Update, Update, Delete), termasuk didalamnya otentikasi pengguna dengan sandi yang terenkripsi. didalam aplikasi ini menggunakan database PostgreSQL untuk menyimpan data dan SQLAlchemy untuk interaksi dengan database. 

# Fitur Aplikasi 
- Otentikasi pengguna dengan sandi yang terenkripsi
- fitur logging sebagai riwayat kejadian dalam aplikasi
- Operasi CRUD Employee
  
# Persyaratan Aplikasi 
sebelum menjalankan aplikasi ini, perlu dipastikan anda memiliki hal-hal berikut terinstall 
- Python 3.11.3
- PostgreSQL
- VS Code
 
# Dokumentasi Aplikasi 
- Dokumentasi dan SDLC     : https://drive.google.com/file/d/1Yv_vI5rPGNnyN-JP8XPU6-w158XQxKxq/view?usp=sharing
- Postman                  : https://drive.google.com/file/d/1hK67DvXeDZBvEPwvsxYCjeKmm61glK3C/view?usp=drive_link

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
## Trigger Log 
Menyimpan aktivitas dari user berupa Insert, Update, dan Delete 
```bash
class UserActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    activity_type = db.Column(db.String(15))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
```
## Create User
```bash
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT, 
    username VARCHAR(80) NOT NULL UNIQUE,
    password VARCHAR(256) NOT NULL, 
    first_name VARCHAR(25) NOT NULL,
    last_name VARCHAR(35) NOT NULL,
    gender CHAR(15), NOT NULL,
    status VARCHAR(15) NOT NULL 
);
```
## Update User
```bash
UPDATE users
SET 
    first_name = 'NewFirstName',
    last_name = 'NewLastName',
    gender = 'NewGender',
    status = 'NewStatus'
WHERE
    username = 'existing_username';
```
## Read User
```bash
SELECT * FROM users;
```
## Delete User
```bash
DELETE FROM users WHERE username = 'username_to_delete';
```


