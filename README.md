You can clone the project and run the below command to install the packages needed in the requirements.txt But it is recommended you create a virtual environment before running the pip install command

#To create virtual enviroment, py -m venv
>>py -m venv venv

#activate virtual environment
>>venv\Scripts\activate.bat

#Now you can run the pip install command
>>pip install -r requirements.txt

#to run your project, you need to start your application
>>py manage.py runserver

#to create database migration, sqlite is been used so you won't need db credentials settings
>>py manage.py makemigrations

#then migrate
>>py manage.py migrate

To manage your database with the default sqlite database, visit /admin in your admin panel #create a default user account to access admin panel
>>py manage.py createsuperuser

