## This is the Server for CrowdCur Project. 

## How to run :
To run this project on `localhost` first you need to install `PostgreSQL 10.3`
then follow the list below : 
1. Install PostgreSQL
2. Make sure it works 
3. Create a Database using `psql`
    - Open up `cmd`
    - Run `psql -U <username> -d postgres`
    - Run the following command one line at a time: 

    ```sql
    CREATE USER <username> WITH ENCRYPTED PASSWORD '' CREATEDB;
    CREATE DATABASE crowdcur_server WITH ENCODING 'UTF-8' OWNER "<username>";
    GRANT ALL PRIVILEGES ON DATABASE crowdcur_server TO <username>;
    ```
    **replace `<username>` with your user name!**
    
    - Go to `crowdcur_server/crowdcur_server/settings.py` and replace :
    ```python
       DATABASES = {
        'default': {
                 'ENGINE': 'django.db.backends.sqlite3',
                 'NAME': '/Users/Payam/PycharmProjects/crowdcur_server/db.sqlite3',
             }
        }
    ```
    with :
    ```python
   DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'crowdcur_server',
        'USER': '<username>',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    },
   }
    ```
    
    **be careful about `<username>`**
    
4. Using `cmd` again, go to the root folder of the project (`crowcur_server/`) and run this : 
    ```bash
       pip install -r requirements.txt 
    ```
    make sure everything is installed correctly. 
    
5. run 
    ```bash
    python manage.py check
    ```
    everything must be fine. 
6. run 
    ```bash
    python manage.py makemigrations
    ```
7. run 
    ```bash
    python manage.py migrate
    ```
8. run 
    ```bash
    python manage.py runscript -v 2 scripts.workinterface_data_dump
    ```
        

