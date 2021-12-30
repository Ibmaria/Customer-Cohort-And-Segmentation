# Author Ibrahim Koné 
# Cdiscount-Customer-Reviews-Analysis

This app helps businesses identify, segment, and understand customers better. The companies can provide their frequent customer’s free merchandise, rewards, coupons, to encourage loyalty. They can also identify potential & promising customers, make suitable engagement programs to encourage/improve loyalty and long-term business. The app also shows Customer LifeTime Value and Cohort Analysis.

<br />

## How to use it

```bash
$ # Get the code
$ git clone https://github.com/Ibmaria/Customer-Cohort-And-Segmentation.git
$ cd Customer-Cohort-And-Segmentation
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$ # Virtualenv modules installation (Anaconda)
$ conda create -n yourvirtualenname
$ activate yourvirtualenname

$
$ # Install modules - SQLite Storage
$ pip3 install -r requirements.txt or pip install -r requirements.txt
$
$ # Create tables
$ python manage.py makemigrations
$ python manage.py migrate
$
$ # Start the application (development mode)
$ python manage.py runserver # default port 8000
$
$ # Start the app - custom port
$ # python manage.py runserver 0.0.0.0:<your_port>
$
$ # Access the web app in browser: http://127.0.0.1:8000/
```

> Note: To use the app, please access the registration page and create a new user. After authentication, the app will unlock the private pages.

<br />

## Inscription SnapShot
![App screenshot](https://github.com/Ibmaria/Cdiscount-Customer-Feedback-Analysis/blob/master/screenshot/inscription.PNG)

## Login SnapShot
![App screenshot](https://github.com/Ibmaria/Customer-Cohort-And-Segmentation/blob/master/screenshot/login.png)
<br /> 

## Content One
![Content 1](https://github.com/Ibmaria/Customer-Cohort-And-Segmentation/blob/master/screenshot/app1.png)
<br />

## Content 2
![Content 2](https://github.com/Ibmaria/Customer-Cohort-And-Segmentation/blob/master/screenshot/app2.png)
<br />

## Content 3
![Content 3](https://github.com/Ibmaria/Customer-Cohort-And-Segmentation/blob/master/screenshot/app3.png)
<br />

## Cohort Analysis
![Cohort](https://github.com/Ibmaria/Customer-Cohort-And-Segmentation/blob/master/screenshot/cohort.png)
<br />

## Segmentation Analysis
![Cohort](https://github.com/Ibmaria/Customer-Cohort-And-Segmentation/blob/master/screenshot/segmentation.png)
<br />

## Download Video App Here
![App Video](https://github.com/Ibmaria/Customer-Cohort-And-Segmentation/blob/master/videoapp.gif)
<br />


## Codebase structure

The project is coded using a simple and intuitive structure presented below:

```bash
< PROJECT ROOT >
   |-- Airflow/
        |--Automat
   |      
   |-- autentification/                              
   |    |-- migrations                  
   |    |-- static/
   |    |
   |    |-- templates/                     
   |         *.html 
   |                       
   |    |--fichierspython/
   |         *.py
   |-- Aws/
   |    |--cloud                            
   |
   |-- chat/  
   |     |--migrations
   |     |--static
   |     |--templates
   |
   |    |--fichierspython/
   |         *.py                       
   |
   |-- customer/  App Kernel                              
   |    |--fichierspython/
   |         *.py                             
   |
   |--customerservice/
   |    
   |    |--fichierspython
   |          *.py
   |--data/
   |     |*.csv
   |     |*.ipynb
   |--model
   |    |--dashapps
          *.py
   |    |--migrations
   |    |--static
   |    |--templates
   |    |   *.html
   |
   |-- requirements.txt                    # Development modules - SQLite  storage                               
   |-- manage.py                           # Start the app - Django default start script
   |
   |-- ************************************************************************
```

<br />





