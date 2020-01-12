# csc3065_assignment_3

Deployed using docker for GCP
Deployed with docker and github build for heroku
Pipeline with azure

Code:
Spider crawler is located in SpiderBot file
Tests for the application can be found in the tests folder
HTML pages can be found in the templates folder
The main code is located in app.py
Database connections can be found in the database_connect.py file
Requirements are found in the requirements.txt file
Use of uwsgi can be found in the uwsgi file
All the URLs currently in the system is stored as a list in urls.py

Scripting:
For the azure pipeline and deployment this can be found in the azure-pipeline.yml file
For deploying on gcp without kubernates is the app.yaml file which can be run in the gcp console
Dockerfile is used to create a docker image
Cloudbuild.yaml works along wide the yml files in the k8s folder to deploy a kubernates pipeline to gcp and deployment
Docker-compose.yml is used in order to deploy a docker container on the local machine and hit localhost to view search engine
To deploy with semaphore and to heroku the yml files are in .semaphore folder. One yml file for the semaphore pipeline and the other for heroku.
Procfile is also used for heroku as it is needed to open the designated port and run the app

Storage:
MongoDB is used for the database to hold the information and so providing a large storage area (multiple) and also quick for performance

Ads:
Ads are provided by a adserver ad glare thats information is stored in the database and passed to the HTML to deploy correct ads based on search results


