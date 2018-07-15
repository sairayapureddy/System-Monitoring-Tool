# System-Monitoring-Tool
This project can be used to monitor system utilization stats like CPU Usage, Memory Usage, Disk Usage with visualizations.

# Steps to run the project
The best way to run projects is to create virtual environment so that it won't affect the installables related to other python projects

1. Create a virtual environment with python.
      - pip install virtualenv
      - virtualenv <project_name>
      - <project_name>\Scripts\activate
      - cd <project_name>

2. Clone the reposiory into your <project_name> folder (git clone https://github.com/sairayapureddy/System-Monitoring-Tool.git)
3. Open command prompt and install packages related to project which are listed in req.txt file.
      - pip install -r req.txt

4. Project is created using mongoDB as backend database. So install MongoDB Community version from https://www.mongodb.com/download-center
5. Run the mongo database and by default it listens on 27017 port
6. From our <project_name> folder run following
      - python manage.py migrate (For creating initial collections related to User, Sessions etc)
      - python manage.py runserver
