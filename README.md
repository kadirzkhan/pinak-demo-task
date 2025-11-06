# Pinak Venture Demo Task — Python/Django Developer

This repository contains the completed **demo tasks** for the **Python/Django Developer** position at **Pinak Venture**.

---

## Project Overview

This project demonstrates:
1. **Web Scraping using Python**
2. **REST API Authentication using Django REST Framework**

All code is production-ready, well-documented, and tested locally using Postman.

---

## 1. Web Scraping Task — `ibps_scraper.py`

###  Objective
Scrape **public job listings** from the [official IBPS website](https://www.ibps.in) and save them into a structured CSV file.

### Extracted Fields
| Field | Description |
|--------|--------------|
| Job Title | Title of the recruitment post |
| Location | Default: India (IBPS doesn’t list cities) |
| Post/Publish Date | Date of posting |
| Details Link | URL to job page |

### Script Flow
1. Send request to IBPS homepage using `requests`
2. Parse HTML with `BeautifulSoup` and `lxml`
3. Extract announcements and job links
4. Store data in `pandas` DataFrame
5. Save results as `ibps_jobs.csv`

###  Libraries Used
- `requests`
- `beautifulsoup4`
- `lxml`
- `pandas`

### Run Command
```bash
python ibps_scraper.py

Output
File: ibps_jobs.csv
--------------------------------------------------------------------------------------------------------------------------

2. Django REST API Task — Authentication API
- Objective: Build a Django REST Framework project with a /api/login/ endpoint that authenticates users and returns an auth token.

- Endpoint
 POST /api/login/

- Request Body (JSON)
{
  "username": "testuser",
  "password": "testpass123"
}

-  Response
{
    "token": "845b5067bd289d04e1a70159a487bef764826504",
    "username": "testuser",
    "message": "Login successful"
}

- Test Credentials
  username: testuser
  password: testpass123

- Setup Instructions
1. Clone Repository
git clone https://github.com/kadirzkhan/pinak_demo_task.git
cd pinak_demo_task

2. Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate       # For Windows
# OR
source .venv/bin/activate    # For macOS/Linux

3. Install Requirements
pip install -r requirements.txt

4. Run Django Server
python manage.py runserver


Now open your browser or Postman at:
- http://127.0.0.1:8000/api/login/

Postman Collection

File: postman_collection.json

How to Use:

1. Open Postman
2. Click Import
3.Choose postman_collection.json
4.Send the POST /api/login/ request
4.View the token in the response

-------------------------------------------------------------------------------------------------------------------------
 Project Structure
pinak_demo_task/
│
├── ibps_scraper.py             # Web scraping script
├── ibps_jobs.csv               # Scraped job listings
├── postman_collection.json     # Postman API test collection
├── requirements.txt
├── manage.py
│
├── pinak_demo/                 # Django project folder
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
└── api/                        # Django app for APIs
    ├── views.py
    ├── urls.py
    ├── serializers.py
    └── ...
-----------------------------------------------------------------------------------------------------------------------

Tech Stack
Category         	Technologies
Language	         Python 3.9+
Framework	         Django 4+, Django REST Framework
API Auth	         DRF Token Authentication
Data Processing	   Pandas, NumPy
Web Scraping	     Requests, BeautifulSoup4, lxml
Testing	            Postman

-----------------------------------------------------------------------------------------------------------------------

-  Dependencies
Package	                    Purpose
Django	                    Web framework
djangorestframework	        REST API framework
requests	                  Fetch HTML data
beautifulsoup4	            HTML parsing
lxml	                      Parser backend
pandas	                    CSV export
numpy	                      Data handling
python-dotenv	              Env variables
pytz	Timezone               support

---------------------------------------------------------------------------------------------------------------------
requirements
Django>=4.0
djangorestframework>=3.14
djangorestframework-simplejwt>=5.2.2
requests>=2.31.0
beautifulsoup4>=4.12.2
lxml>=4.9.3
pandas>=2.0.3
numpy>=1.25.2
python-dotenv>=1.0.0
pytz>=2023.3

--------------------------------------------------------------------------------------------------------------------------
 Testing Steps

Run scraper:

python ibps_scraper.py


→ Generates ibps_jobs.csv

Start Django server:

python manage.py runserver


Test login API via Postman:

Import postman_collection.json

Set JSON body:

{"username": "testuser", "password": "testpass123"}


Send request → receive token.

Output:

<img width="1884" height="1058" alt="Screenshot 2025-11-06 165133" src="https://github.com/user-attachments/assets/c7e8a9af-08bf-4c91-97a6-fad81c0c2362" />

-----------------------------------------------------------------------------------------------------------------------

Author
Abdul Kadir
📧 abdulkadir5108@gmail.com 
🔗 GitHub Profile : https://github.com/kadirzkhan

Thankyou for the opportunity 

