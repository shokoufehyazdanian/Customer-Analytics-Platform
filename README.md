# Customer Analytics Platform
![Docker](https://img.shields.io/badge/Docker-enabled-blue)
![Python](https://img.shields.io/badge/Python-3.12-yellow)
![dbt](https://img.shields.io/badge/dbt-analytics-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)

End-to-End Data Analytics & Machine Learning Platform

This project demonstrates an end-to-end analytics platform
built with modern data engineering, analytics and machine learning tools.

The goal is to analyze customer behavior, generate business insights,
and predict customer churn.

## Business Problem

E-commerce companies need to understand:

- Which customers generate the most value?
- Which products drive revenue?
- Which customers are at risk of churn?
- How can data support business decisions?

This project builds a complete analytics pipeline
to answer these questions.


## Architecture
```mermaid
flowchart LR

    A[Olist CSV Dataset<br/>data/raw] --> B[Docker Data Loader<br/>Python + Pandas]

    B --> C[(PostgreSQL<br/>Raw Layer)]

    C --> D[Great Expectations<br/>Data Validation]

    C --> E[dbt Transformation Layer]

    E --> E1[Staging Models]
    E --> E2[Analytics Marts]

    E2 --> F[Power BI Dashboard]

    E2 --> G[Feature Engineering]

    G --> H[ML Pipeline<br/>Scikit-learn/XGBoost]

    H --> I[MLflow<br/>Experiment Tracking]

    H --> J[FastAPI<br/>Churn Prediction API]

    K[Airflow Scheduler<br/>Workflow Orchestration] --> B
    K --> D
    K --> E
    K --> H
```


.
├── data
│   └── raw
│       └── dataset files
│
├── data_loader
│   ├── Dockerfile
│   ├── requirements.txt
│   └── load_data.py
│
├── src
│   └── data ingestion
│
├── customer_analytics_dbt
│   └── transformation models
│
├── ml
│   ├── feature engineering
│   ├── training
│   └── models
│
├── api
│   └── FastAPI service
│
├── dashboard
│   └── Power BI dashboard
│
└── docker-compose.yml
Data Pipeline
Data ingestion
Raw datasets are loaded into PostgreSQL using a dedicated Docker data loader service.

The loader reads CSV files from:

data/raw/

Expected files:

data/raw/

├── olist_orders_dataset.csv
├── olist_order_items_dataset.csv
├── olist_products_dataset.csv
└── olist_order_reviews_dataset.csv
The data_loader container automatically imports these files into PostgreSQL.

Data validation
Great Expectations validates data quality.

Data transformation
dbt creates analytical models.

Analytics
Business KPIs are generated.

Machine Learning
Customer churn prediction model is trained.

Dashboard Preview
Executive Overview
Dashboard

Products
Products

Machine Learning Model
Problem
Customer churn prediction.

Features
Recency
Frequency
Monetary Value
Average Order Value
Models Tested
Logistic Regression
Random Forest
XGBoost
Evaluation Metrics
Accuracy
Precision
Recall
ROC-AUC
Best Model:

Random Forest

ROC-AUC: 0.67

How To Run
Clone repository:

git clone REPOSITORY

Dataset Setup:

Raw datasets are not included in this repository because of their size.

Download the Brazilian E-Commerce Public Dataset by Olist from Kaggle:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

After downloading, extract the CSV files into:

data/raw/

After placing the files, Docker will automatically load them into PostgreSQL.

Create environment:

python -m venv venv

Install dependencies:

pip install -r requirements.txt

Start services:

docker compose up -d

Run dbt:

cd customer_analytics_dbt

dbt run

Start API:

uvicorn api.app.main:app --reload

in proje mane readme, mikham runnesh konam in error ro dad: 


(venv) PS C:\Users\PC\Downloads\Project> docker compose up -d
>> 
>> 
validating C:\Users\PC\Downloads\Project\docker-compose.yml:  additional properties 'api' not allowed

What's next:
    Debug this Compose error with Gordon → docker ai "help me fix this compose error"
(venv) PS C:\Users\PC\Downloads\Project> 

خطایی که داری:

validating C:\Users\PC\Downloads\Project\docker-compose.yml:
additional properties 'api' not allowed
یعنی فایل docker-compose.yml ساختارش اشتباه است. Docker Compose یک کلید به نام api را در سطح اصلی فایل قبول نمی‌کند. معمولاً این اتفاق وقتی می‌افتد که سرویس‌ها را مستقیم زیر ریشه نوشته باشی، در حالی که باید زیر services: باشند.

احتمالاً فایل تو چیزی شبیه این است:

version: "3.8"

api:
  build: ./api
  ports:
    - "8000:8000"

postgres:
  image: postgres
ولی باید این شکلی باشد:

version: "3.8"

services:

  api:
    build: ./api
    ports:
      - "8000:8000"
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics
    ports:
      - "5432:5432"

  data_loader:
    build: ./data_loader
    depends_on:
      - postgres
یعنی همه کانتینرها باید زیر services: قرار بگیرند.

کاری که الان انجام بده:
فایل را باز کن:

C:\Users\PC\Downloads\Project\docker-compose.yml
کل محتویاتش را بفرست اینجا، یا حداقل ۳۰ خط اولش را.

من دقیق اصلاحش می‌کنم.

برای تست بعد از اصلاح:
در همان فولدر پروژه اجرا کن:

docker compose config
اگر درست باشد، باید یک خروجی YAML بزرگ ببینی و دیگر error ندهد.

بعد:

docker compose up -d
یک نکته دیگر: در README نوشته:

docker compose up -d
اما این فقط وقتی کار می‌کند که docker-compose.yml کامل باشد. چون پروژه شامل:

PostgreSQL

data_loader

API

احتمالاً dbt

است، باید همه آنها در بخش services تعریف شده باشند.

فایل docker-compose.yml را بفرست تا دقیق با ساختار پروژه‌ات هماهنگش کنیم.


version: "3.8"

services:

  postgres:
    image: postgres:16

    container_name: customer_postgres

    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics

    ports:
      - "5432:5432"

    volumes:
      - postgres_data:/var/lib/postgresql/data


  airflow:
    build: .

    container_name: customer_airflow

    depends_on:
      - postgres

    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor

      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://postgres:postgres@postgres:5432/customer_analytics

      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics

    ports:
      - "8080:8080"

    volumes:
      - ./airflow/dags:/opt/airflow/dags
      - ./src:/opt/airflow/src
      - ./customer_analytics_dbt:/opt/customer_analytics_dbt
      - ./data:/opt/airflow/data

    command:
      airflow standalone

api:

  build:
    context: ./api

  container_name:
    churn_api

  ports:
    - "8000:8000"

  volumes:
    - ./ml:/app/ml
volumes:
  postgres_data:

مشکل دقیقاً همین‌جاست. بخش api را بعد از services بسته‌ای و خارج از آن قرار داده‌ای:

الان فایل تو این قسمت را دارد:

services:

  postgres:
    ...

  airflow:
    ...

api:
  build:
    context: ./api
در YAML، api در سطح ریشه قرار گرفته و Docker Compose فقط کلیدهایی مثل services, volumes, networks را در آن سطح قبول می‌کند. برای همین می‌گوید:

additional properties 'api' not allowed
باید api را داخل services: منتقل کنی.

نسخه اصلاح‌شده:

version: "3.8"

services:

  postgres:
    image: postgres:16

    container_name: customer_postgres

    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics

    ports:
      - "5432:5432"

    volumes:
      - postgres_data:/var/lib/postgresql/data


  airflow:
    build: .

    container_name: customer_airflow

    depends_on:
      - postgres

    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor

      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://postgres:postgres@postgres:5432/customer_analytics

      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics

    ports:
      - "8080:8080"

    volumes:
      - ./airflow/dags:/opt/airflow/dags
      - ./src:/opt/airflow/src
      - ./customer_analytics_dbt:/opt/customer_analytics_dbt
      - ./data:/opt/airflow/data

    command:
      airflow standalone


  api:
    build:
      context: ./api

    container_name: churn_api

    ports:
      - "8000:8000"

    volumes:
      - ./ml:/app/ml


volumes:
  postgres_data:
حالا این دستورات را اجرا کن:

1. اول validate کن:
docker compose config
اگر بدون error تمام شد:

2. کانتینرها را بالا بیاور:
docker compose up -d
3. وضعیت را ببین:
docker compose ps
باید چیزی شبیه این ببینی:

NAME                 STATUS
customer_postgres    running
customer_airflow     running
churn_api            running
اما احتمالاً یک مشکل بعدی هم داری: سرویس airflow:

build: .
یعنی Docker دنبال این فایل می‌گردد:

Project/
 ├── Dockerfile
 ├── docker-compose.yml
اگر در ریشه پروژه Dockerfile نداری، مرحله بعدی خطا می‌دهد.

همچنین برای API:

build:
  context: ./api
باید این ساختار وجود داشته باشد:

Project/
│
├── api/
│   ├── Dockerfile
│   ├── app/
│   │   └── main.py
│
├── airflow/
├── customer_analytics_dbt/
├── ml/
└── docker-compose.yml
بعد از اجرای docker compose up -d اگر خطای بعدی آمد، متن کاملش را بفرست. احتمالاً یکی از این‌ها خواهد بود:

Dockerfile پیدا نمی‌شود

Airflow initialization مشکل دارد

API dependency مشکل دارد

PostgreSQL connection مشکل دارد


(venv) PS C:\Users\PC\Downloads\Project> docker compose up -d
time="2026-07-20T18:29:21+02:00" level=warning msg="C:\\Users\\PC\\Downloads\\Project\\docker-compose.yml: the attribute version is obsolete, it will be ignored, please remove it to avoid potential confusion"
#1 [internal] load local bake definitions
#1 reading from stdin 953B done
#1 DONE 0.0s

#2 [api internal] load build definition from Dockerfile
#2 transferring dockerfile: 218B 0.0s done
#2 DONE 0.0s

#3 [airflow internal] load build definition from Dockerfile
#3 transferring dockerfile: 106B 0.0s done
#3 DONE 0.1s

#4 [airflow internal] load metadata for docker.io/apache/airflow:2.9.0
#4 DONE 0.1s

#5 [api internal] load metadata for docker.io/library/python:3.12-slim
#5 ...

#6 [airflow internal] load .dockerignore
#6 transferring context: 2B done
#6 DONE 0.0s

#7 [airflow 1/2] FROM docker.io/apache/airflow:2.9.0@sha256:2b0695195cf0cedd02a8d71401750a7739f3f10e82ee7b5a4e3fbd9a19452a8d
#7 resolve docker.io/apache/airflow:2.9.0@sha256:2b0695195cf0cedd02a8d71401750a7739f3f10e82ee7b5a4e3fbd9a19452a8d 0.0s done
#7 DONE 0.0s

#8 [airflow 2/2] RUN pip install dbt-postgres
#8 CACHED

#9 [airflow] exporting to image
#9 exporting layers 0.0s done
#9 exporting manifest sha256:16075e58472ef770d34ffa7ff03b86bb25dd56c2bfdb0f5ac30a9ca074e32b85 0.0s done
#9 exporting config sha256:c083073b48332c42c3080df45b874d9401eaaa7146c70953480d5a9423b52a84 0.0s done
#9 exporting attestation manifest sha256:a91de4edc8090f97dde014f24cd064ab06f9cbb4ec464f7b5188a576a75e43a9
#9 exporting attestation manifest sha256:a91de4edc8090f97dde014f24cd064ab06f9cbb4ec464f7b5188a576a75e43a9 0.0s done
#9 exporting manifest list sha256:7557a9b508e138d7f48de9ebec2e53c688df3b94ee12ca81be1e432e296d09f7 0.0s done
#9 naming to docker.io/library/project-airflow:latest done
#9 unpacking to docker.io/library/project-airflow:latest 0.0s done
#9 DONE 0.3s

#5 [api internal] load metadata for docker.io/library/python:3.12-slim
#5 ...

#10 [airflow] resolving provenance for metadata file
#10 DONE 0.0s

#5 [api internal] load metadata for docker.io/library/python:3.12-slim
#5 ...

#11 [auth] library/python:pull token for registry-1.docker.io
#11 DONE 0.0s

#5 [api internal] load metadata for docker.io/library/python:3.12-slim
#5 DONE 2.9s

#12 [api internal] load .dockerignore
#12 transferring context: 2B done
#12 DONE 0.0s

#13 [api 1/5] FROM docker.io/library/python:3.12-slim@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de
#13 resolve docker.io/library/python:3.12-slim@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de 0.0s done
#13 DONE 0.0s

#14 [api internal] load build context
#14 transferring context: 1.58kB 0.0s done
#14 DONE 0.0s

#15 [api 2/5] WORKDIR /app
#15 CACHED

#16 [api 3/5] COPY requirements.txt .
#16 CACHED

#17 [api 4/5] RUN pip install -r requirements.txt
#17 CACHED

#18 [api 5/5] COPY . .
#18 CACHED

#19 [api] exporting to image
#19 exporting layers done
#19 exporting manifest sha256:18a2fcc0508bf52dfb10c0cd9d1982d0408171f7962697980877cfc4689102df 0.0s done
#19 exporting config sha256:617ac5bdd8812dcb8f672334b58c98dc7c5f40ce5b62efd9ded4c6a6cfbf6bc0 0.0s done
#19 exporting attestation manifest sha256:2f957678de55fb4e0cd19c927f11a84474bdc983d11fa5cdd34160ae7e472712
#19 exporting attestation manifest sha256:2f957678de55fb4e0cd19c927f11a84474bdc983d11fa5cdd34160ae7e472712 0.0s done
#19 exporting manifest list sha256:5b247ba10b6bb0a66764b045f6e9d717f3c4acbd106a3ff66ef22a0950e6d753 0.0s done
#19 naming to docker.io/library/project-api:latest done
#19 unpacking to docker.io/library/project-api:latest done
#19 DONE 0.1s

#20 [api] resolving provenance for metadata file
#20 DONE 0.0s
[+] up 5/7
 ✔ Image p... Built                                                                                                                                                                                  3.9s
 ✔ Image p... Built                                                                                                                                                                                  3.9s
 ✔ Network... Created                                                                                                                                                                                0.1s
 ✔ Volume ... Created                                                                                                                                                                                0.0s
 - Contain... Creating                                                                                                                                                                               0.0s
 - Contain... Creating                                                                                                                                                                               0.0s
 ✘ service... Error response from daemon: Conflict. The container name "/churn_api" is already in use by container "8e96384291f97783d1f491d0d8954a45d73547c38d516688b0a348639403b106". You have to remove (or rename) that container to be able to reuse that name. 0.0s
Error response from daemon: Conflict. The container name "/churn_api" is already in use by container "8e96384291f97783d1f491d0d8954a45d73547c38d516688b0a348639403b106". You have to remove (or rename) that container to be able to reuse that name.

What's next:
    Debug this Compose error with Gordon → docker ai "help me fix this compose error"
(venv) PS C:\Users\PC\Downloads\Project> docker compose ps
time="2026-07-20T18:29:31+02:00" level=warning msg="C:\\Users\\PC\\Downloads\\Project\\docker-compose.yml: the attribute version is obsolete, it will be ignored, please remove it to avoid potential confusion"
NAME      IMAGE     COMMAND   SERVICE   CREATED   STATUS    PORTS

خوب، مشکل قبلی حل شده و Docker الان توانسته imageها را بسازد. خطای جدید کاملاً مشخص است:

Conflict. The container name "/churn_api" is already in use
یعنی قبلاً یک کانتینر با نام churn_api ساخته شده و هنوز وجود دارد. چون در docker-compose.yml داری:

container_name: churn_api
Docker اجازه نمی‌دهد دوباره یک کانتینر با همین نام بسازی.

راه‌حل ۱ (پیشنهادی): کانتینر قبلی را حذف کن
اجرا کن:

docker rm -f churn_api
بعد دوباره:

docker compose up -d
اگر می‌خواهی همه چیز را تمیز از اول بالا بیاوری:
docker compose down
بعد:

docker compose up -d
برای دیدن کانتینرهای موجود:
docker ps -a
احتمالاً چیزی مثل این می‌بینی:

CONTAINER ID   NAME          STATUS
8e96384291f9   churn_api     Exited
همان را باید پاک کنی.

یک اصلاح کوچک هم انجام بده
این warning:

the attribute `version` is obsolete, it will be ignored
خطا نیست. در Docker Compose جدید دیگر نیاز به:

version: "3.8"
نداری.

پس اول فایل را از:

version: "3.8"

services:
به:

services:
تغییر بده.

بعد از بالا آمدن موفق:

docker compose ps
باید چیزی شبیه این ببینی:

NAME                 SERVICE     STATUS
customer_postgres    postgres    running
customer_airflow     airflow     running
churn_api            api         running
بعد تست API:

در مرورگر:

http://localhost:8000
یا اگر FastAPI داری:

http://localhost:8000/docs
برای Airflow:

http://localhost:8080
یک نکته: خروجی docker compose ps تو خالی است چون up وسط کار fail شده و هیچ سرویسی کامل بالا نیامده. بعد از حذف churn_api دوباره اجرا کن.


 ✘ service... Error response from daemon: Conflict. The container name "/customer_postgres" is already in use by container "49f67a870817b329e5b2bc85b00b87c9649e688e4d70f7cd734a677b04c95d62". You have to remove (or rename) that container to be able to reuse that name. 0.0s
 - Contain... Creating                                                       

الان همان مشکل قبلی برای PostgreSQL اتفاق افتاده. یک کانتینر قدیمی با این نام وجود دارد:

/customer_postgres
و در docker-compose.yml هم داری:

container_name: customer_postgres
Docker نمی‌تواند یک کانتینر جدید با همان نام بسازد.

سریع‌ترین راه:
اجرا کن:

docker rm -f customer_postgres
بعد:

docker compose up -d
اما چون قبلاً هم churn_api مشکل داشت، احتمالاً چند کانتینر قدیمی از اجرای قبلی مانده‌اند. بهتر است یک بار همه را تمیز کنی:

docker compose down
اگر باز هم conflict داشتی:

docker rm -f churn_api customer_postgres customer_airflow
بعد:

docker compose up -d
برای اینکه ببینی چه کانتینرهایی باقی مانده‌اند:

docker ps -a
اگر چیزی مثل این دیدی:

customer_postgres
customer_airflow
churn_api
همان‌ها باید حذف شوند.

یک پیشنهاد برای آینده: بهتر است container_name را از docker-compose.yml حذف کنی. مثلاً:

postgres:
  image: postgres:16
به جای:

postgres:
  image: postgres:16
  container_name: customer_postgres
Docker خودش اسم‌هایی مثل:

project-postgres-1
project-api-1
project-airflow-1
می‌سازد و دیگر مشکل conflict پیش نمی‌آید.

فعلاً فقط حذف کانتینرهای قبلی کافی است. بعد از docker compose up -d خروجی docker compose ps را بفرست تا ببینیم Airflow و API درست بالا آمده‌اند یا نه.


(venv) PS C:\Users\PC\Downloads\Project\customer_analytics_dbt> dbt run
>> 
>> 
dbt : The term 'dbt' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was included, verify that the path is correct 
and try again.
At line:1 char:1
+ dbt run
+ ~~~
    + CategoryInfo          : ObjectNotFound: (dbt:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
 

این خطا یعنی dbt در محیط فعلی ویندوزت نصب نیست یا در PATH نیست:

dbt : The term 'dbt' is not recognized...
در پروژه تو، طبق docker-compose.yml، dbt-postgres داخل کانتینر Airflow نصب شده:

RUN pip install dbt-postgres
ولی تو الان داری از PowerShell ویندوز اجرا می‌کنی:

(venv) PS C:\Users\PC\Downloads\Project\customer_analytics_dbt> dbt run
این venv پایتون ویندوز است و ارتباطی با محیط Airflow Docker ندارد.

راه ۱ (پیشنهادی): اجرای dbt داخل کانتینر Airflow
اول ببین کانتینر Airflow بالا است:

docker ps
احتمالاً چیزی مثل این داری:

customer_airflow
بعد وارد کانتینر شو:

docker exec -it customer_airflow bash
حالا داخل کانتینر:

cd /opt/customer_analytics_dbt
تست کن:

dbt --version
باید چیزی شبیه:

Core:
  - installed: 1.x.x
Plugins:
  - postgres: 1.x.x
ببینی.

بعد:

dbt run
راه ۲: نصب dbt روی ویندوز
اگر می‌خواهی مستقیم از PowerShell اجرا کنی:

داخل venv:

pip install dbt-postgres
بعد:

dbt --version
و:

dbt run
اما برای معماری پروژه تو راه ۱ بهتر است
چون README تو نوشته:

Docker
PostgreSQL
Airflow
dbt
یعنی انتظار این است:

Windows
   |
Docker
   |
Airflow container
   |
dbt
   |
PostgreSQL container
نه:

Windows venv
   |
dbt
   |
Docker PostgreSQL
بعد از ورود به Airflow ممکن است یک خطای جدید بگیری:

profiles.yml not found
یا:

Database connection failed
که مربوط به تنظیم dbt profile است.

اگر بعد از اجرای:

dbt run
خطایی آمد، کل خروجی را بفرست.


(venv) PS C:\Users\PC\Downloads\Project\customer_analytics_dbt> docker exec -it customer_airflow bash
airflow@958b7722c5c0:/opt/airflow$ cd /opt/customer_analytics_dbt
airflow@958b7722c5c0:/opt/customer_analytics_dbt$ dbt --version
Core:
  - installed: 1.12.0-rc2
  - latest:    1.12.0     - Update available!

  Your version of dbt-core is out of date!
  You can find instructions for upgrading here:
  https://docs.getdbt.com/docs/installation

Plugins:
  - postgres: 1.10.2 - Update available!

  At least one plugin is out of date with dbt-core.
  You can find instructions for upgrading here:
  https://docs.getdbt.com/docs/installation


airflow@958b7722c5c0:/opt/customer_analytics_dbt$ dbt run
16:35:00  Running with dbt=1.12.0-rc2
16:35:00  Registered adapter: postgres=1.10.2
16:35:00  Unable to do partial parsing because saved manifest not found. Starting full parse.
16:35:02  Found 11 models, 13 data tests, 1 source, 475 macros
16:35:02  
16:35:02  Concurrency: 1 threads (target='dev')
16:35:02  
16:35:02  
16:35:02  Finished running  in 0 hours 0 minutes and 0.14 seconds (0.14s).
16:35:02  [ERROR]: Encountered an error:
Database Error
  connection to server at "localhost" (::1), port 5432 failed: Connection refused
        Is the server running on that host and accepting TCP/IP connections?
  connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
        Is the server running on that host and accepting TCP/IP connections?
  

خوب، تا اینجا تقریباً همه‌چیز درست است. dbt داخل Airflow پیدا شده و مدل‌ها را هم خوانده:

Found 11 models, 13 data tests, 1 source
مشکل فقط اتصال dbt به PostgreSQL است.

خطا:

connection to server at "localhost", port 5432 failed
Connection refused
یعنی dbt داخل کانتینر customer_airflow دنبال PostgreSQL روی خود همان کانتینر می‌گردد.

اما PostgreSQL تو داخل یک کانتینر جداست:

customer_airflow  --->  customer_postgres
در Docker باید به جای localhost از نام سرویس استفاده کنی:

postgres
1. فایل profiles.yml را پیدا کن
داخل کانتینر Airflow اجرا کن:

find / -name profiles.yml 2>/dev/null
احتمالاً چیزی شبیه این پیدا می‌شود:

/home/airflow/.dbt/profiles.yml
یا:

/opt/customer_analytics_dbt/profiles.yml
2. فایل profiles.yml را باز کن
مثلاً:

cat ~/.dbt/profiles.yml
احتمالاً الان چیزی شبیه این داری:

customer_analytics_dbt:
  target: dev
  outputs:

    dev:
      type: postgres
      host: localhost
      user: postgres
      password: postgres
      port: 5432
      dbname: customer_analytics
      schema: public
مشکل این خط است:

host: localhost
3. تغییر بده به:
customer_analytics_dbt:
  target: dev

  outputs:

    dev:
      type: postgres
      host: postgres
      user: postgres
      password: postgres
      port: 5432
      dbname: customer_analytics
      schema: public
یعنی فقط:

- host: localhost
+ host: postgres
4. دوباره تست کن
داخل کانتینر:

dbt debug
باید ببینی:

Connection test: [OK connection ok]
بعد:

dbt run
اگر فایل profiles.yml وجود ندارد
چک کن:

ls -la ~/.dbt
اگر پوشه خالی بود، بساز:

mkdir -p ~/.dbt
nano ~/.dbt/profiles.yml
و محتویات بالا را قرار بده.

یک نکته دیگر: در docker-compose.yml تو این بخش درست است:

AIRFLOW__DATABASE__SQL_ALCHEMY_CONN:
  postgresql+psycopg2://postgres:postgres@postgres:5432/customer_analytics
پس Docker network درست کار می‌کند. فقط dbt هنوز از تنظیم قدیمی localhost استفاده می‌کند.

بعد از تغییر profiles.yml خروجی dbt debug را بفرست.


(venv) PS C:\Users\PC\Downloads\Project\customer_analytics_dbt> docker exec -it customer_airflow bash
airflow@958b7722c5c0:/opt/airflow$ cd /opt/customer_analytics_dbt
airflow@958b7722c5c0:/opt/customer_analytics_dbt$ dbt --version
Core:
  - installed: 1.12.0-rc2
  - latest:    1.12.0     - Update available!

  Your version of dbt-core is out of date!
  You can find instructions for upgrading here:
  https://docs.getdbt.com/docs/installation

Plugins:
  - postgres: 1.10.2 - Update available!

  At least one plugin is out of date with dbt-core.
  You can find instructions for upgrading here:
  https://docs.getdbt.com/docs/installation


airflow@958b7722c5c0:/opt/customer_analytics_dbt$ dbt run
16:35:00  Running with dbt=1.12.0-rc2
16:35:00  Registered adapter: postgres=1.10.2
16:35:00  Unable to do partial parsing because saved manifest not found. Starting full parse.
16:35:02  Found 11 models, 13 data tests, 1 source, 475 macros
16:35:02  
16:35:02  Concurrency: 1 threads (target='dev')
16:35:02  
16:35:02  
16:35:02  Finished running  in 0 hours 0 minutes and 0.14 seconds (0.14s).
16:35:02  [ERROR]: Encountered an error:
Database Error
  connection to server at "localhost" (::1), port 5432 failed: Connection refused
        Is the server running on that host and accepting TCP/IP connections?
  connection to server at "localhost" (127.0.0.1), port 5432 failed: Connection refused
        Is the server running on that host and accepting TCP/IP connections?
  
airflow@958b7722c5c0:/opt/customer_analytics_dbt$ dbt run
16:36:24  Running with dbt=1.12.0-rc2
16:36:25  Registered adapter: postgres=1.10.2
16:36:25  Unable to do partial parsing because profile has changed
16:36:26  Found 11 models, 13 data tests, 1 source, 475 macros
16:36:26  
16:36:26  Concurrency: 1 threads (target='dev')
16:36:26  
16:36:27  1 of 11 START sql table model public.stg_customers ............................. [RUN]
16:36:27  1 of 11 ERROR creating sql table model public.stg_customers .................... [ERROR in 0.09s]
16:36:27  2 of 11 START sql table model public.stg_order_items ........................... [RUN]
16:36:27  2 of 11 ERROR creating sql table model public.stg_order_items .................. [ERROR in 0.04s]
16:36:27  3 of 11 START sql table model public.stg_orders ................................ [RUN]
16:36:27  3 of 11 ERROR creating sql table model public.stg_orders ....................... [ERROR in 0.04s]
16:36:27  4 of 11 START sql table model public.stg_products .............................. [RUN]
16:36:27  4 of 11 ERROR creating sql table model public.stg_products ..................... [ERROR in 0.04s]
16:36:27  5 of 11 START sql table model public.stg_reviews ............................... [RUN]
16:36:27  5 of 11 ERROR creating sql table model public.stg_reviews ...................... [ERROR in 0.04s]
16:36:27  6 of 11 SKIP relation public_analytics.fact_orders ............................. [SKIP]
16:36:27  7 of 11 SKIP relation public_analytics.mart_customer_rfm ....................... [SKIP]
16:36:27  8 of 11 SKIP relation public_analytics.mart_customer_segments .................. [SKIP]
16:36:27  9 of 11 SKIP relation public_analytics.mart_sales_summary ...................... [SKIP]
16:36:27  10 of 11 SKIP relation public_analytics.mart_product_performance ............... [SKIP]
16:36:27  11 of 11 SKIP relation public_analytics.mart_daily_sales ....................... [SKIP]
16:36:27  
16:36:27  Finished running 11 table models in 0 hours 0 minutes and 0.49 seconds (0.49s).
16:36:27  
16:36:27  Completed with 5 errors, 0 partial successes, and 0 warnings:
16:36:27  
16:36:27  [ERROR]: in model stg_customers (models/staging/stg_customers.sql)
16:36:27    Database Error in model stg_customers (models/staging/stg_customers.sql)
  relation "public.olist_orders_dataset" does not exist
  LINE 27: from public.olist_orders_dataset o
                ^
  compiled code at target/run/customer_analytics_dbt/models/staging/stg_customers.sql
16:36:27  
16:36:27    compiled code at target/compiled/customer_analytics_dbt/models/staging/stg_customers.sql
16:36:27  
16:36:27  [ERROR]: in model stg_order_items (models/staging/stg_order_items.sql)
16:36:27    Database Error in model stg_order_items (models/staging/stg_order_items.sql)
  relation "public.olist_order_items_dataset" does not exist
  LINE 28: from public.olist_order_items_dataset
                ^
  compiled code at target/run/customer_analytics_dbt/models/staging/stg_order_items.sql
16:36:27  
16:36:27    compiled code at target/compiled/customer_analytics_dbt/models/staging/stg_order_items.sql
16:36:27  
16:36:27  [ERROR]: in model stg_orders (models/staging/stg_orders.sql)
16:36:27    Database Error in model stg_orders (models/staging/stg_orders.sql)
  relation "public.olist_orders_dataset" does not exist
  LINE 27: from public.olist_orders_dataset o
                ^
  compiled code at target/run/customer_analytics_dbt/models/staging/stg_orders.sql
16:36:27  
16:36:27    compiled code at target/compiled/customer_analytics_dbt/models/staging/stg_orders.sql
16:36:27  
16:36:27  [ERROR]: in model stg_products (models/staging/stg_products.sql)
16:36:27    Database Error in model stg_products (models/staging/stg_products.sql)
  relation "public.olist_products_dataset" does not exist
  LINE 32: from public.olist_products_dataset
                ^
  compiled code at target/run/customer_analytics_dbt/models/staging/stg_products.sql
16:36:27  
16:36:27    compiled code at target/compiled/customer_analytics_dbt/models/staging/stg_products.sql
16:36:27  
16:36:27  [ERROR]: in model stg_reviews (models/staging/stg_reviews.sql)
16:36:27    Database Error in model stg_reviews (models/staging/stg_reviews.sql)
  relation "public.olist_order_reviews_dataset" does not exist
  LINE 22: from "customer_analytics"."public"."olist_order_reviews_data...
                ^
  compiled code at target/run/customer_analytics_dbt/models/staging/stg_reviews.sql
16:36:27  
16:36:27    compiled code at target/compiled/customer_analytics_dbt/models/staging/stg_reviews.sql
16:36:27  
16:36:27  Done. PASS=0 WARN=0 ERROR=5 SKIP=6 NO-OP=0 REUSED=0 TOTAL=11

عالی، مرحله اتصال حل شد. الان dbt به PostgreSQL وصل می‌شود. خطای جدید مربوط به داده خام (raw data) است.

خطای اصلی:

relation "public.olist_orders_dataset" does not exist
یعنی dbt دنبال این جدول‌ها در PostgreSQL می‌گردد:

public.olist_orders_dataset
public.olist_order_items_dataset
public.olist_products_dataset
public.olist_order_reviews_dataset
ولی این جدول‌ها هنوز داخل دیتابیس ساخته نشده‌اند.

معماری پروژه تو این است:

CSV files
   |
   v
data_loader container
   |
   v
PostgreSQL (raw tables)
   |
   v
dbt transformations
   |
   v
analytics models
الان مرحله اول (data_loader) اجرا نشده یا CSVها در جای درست نیستند.

1. اول وضعیت کانتینرها را چک کن
از PowerShell خارج از کانتینر:

docker compose ps
ببین آیا data_loader داری یا نه.

در docker-compose.yml فعلی که فرستادی فقط این‌ها هستند:

postgres
airflow
api
ولی README پروژه گفته:

data_loader
باید وجود داشته باشد.

2. بررسی کن CSVها وجود دارند
در ویندوز:

C:\Users\PC\Downloads\Project\data\raw
باید این فایل‌ها باشند:

olist_orders_dataset.csv
olist_order_items_dataset.csv
olist_products_dataset.csv
olist_order_reviews_dataset.csv
اگر نیستند، باید دیتاست Olist را دانلود و extract کنی.

3. بررسی PostgreSQL
وارد postgres شو:

docker exec -it customer_postgres psql -U postgres -d customer_analytics
بعد:

\dt
الان احتمالاً چیزی شبیه این می‌بینی:

Did not find any relations.
یعنی جدول خام وجود ندارد.

4. راه سریع برای تست: اجرای loader
در ساختار پروژه باید چیزی شبیه این داشته باشی:

data_loader/
│
├── Dockerfile
├── requirements.txt
└── load_data.py
ولی در compose تو نیست.

باید یک سرویس اضافه شود:

  data_loader:
    build:
      context: ./data_loader

    container_name: customer_data_loader

    depends_on:
      - postgres

    volumes:
      - ./data:/data

    environment:
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics
بعد:

docker compose up --build
5. بعد از load شدن داده‌ها
دوباره:

docker exec -it customer_airflow bash
داخل:

cd /opt/customer_analytics_dbt
اجرا:

dbt run
این بار باید ببینی:

1 of 11 START sql table model public.stg_customers
OK
2 of 11 START sql table model public.stg_order_items
OK
...
Completed successfully
یک سؤال مهم:
لطفاً خروجی این دستور را بفرست:

tree /F /A
از مسیر:

C:\Users\PC\Downloads\Project
چون می‌خواهم ببینم آیا data_loader واقعاً داخل پروژه هست یا README با کد فعلی هماهنگ نیست. الان ۹۰٪ مشکل همین است.


data loader ro chikar konam ejra she nafahmidam

مشکل اینجاست که در پروژه‌ات data_loader باید فایل‌های CSV را بردارد و داخل PostgreSQL بریزد، ولی الان این سرویس اصلاً اجرا نشده. به همین دلیل dbt جدول‌های خام را پیدا نمی‌کند.

قدم‌به‌قدم انجام بده:

1) اول ببین data_loader وجود دارد یا نه
در PowerShell برو به ریشه پروژه:

cd C:\Users\PC\Downloads\Project
بعد:

dir
باید چیزی شبیه این ببینی:

data
data_loader
api
ml
customer_analytics_dbt
docker-compose.yml
اگر پوشه data_loader وجود ندارد، بگو چون باید جدا بسازیم.

2) CSV ها را چک کن
برو اینجا:

C:\Users\PC\Downloads\Project\data\raw
باید این فایل‌ها باشند:

olist_orders_dataset.csv
olist_order_items_dataset.csv
olist_products_dataset.csv
olist_order_reviews_dataset.csv
اگر نیستند، data_loader چیزی برای load کردن ندارد.

3) data_loader را به docker-compose اضافه کن
فایل:

docker-compose.yml
باز کن.

زیر services: این را اضافه کن:

  data_loader:
    build:
      context: ./data_loader

    container_name: customer_data_loader

    depends_on:
      - postgres

    volumes:
      - ./data:/data

    environment:
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics
یعنی آخر فایل چیزی شبیه این شود:

services:

  postgres:
    ...

  airflow:
    ...

  api:
    ...

  data_loader:
    build:
      context: ./data_loader
    container_name: customer_data_loader
    depends_on:
      - postgres
    volumes:
      - ./data:/data
    environment:
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics
4) data_loader را اجرا کن
بعد:

docker compose up --build data_loader
نه -d، چون می‌خواهیم ببینیم چه اتفاقی می‌افتد.

باید چیزی شبیه این ببینی:

Loading olist_orders_dataset.csv
Loading olist_products_dataset.csv
Loading completed
5) بررسی کن جدول‌ها ساخته شده‌اند
بعد:

docker exec -it customer_postgres psql -U postgres -d customer_analytics
داخل PostgreSQL:

\dt
باید ببینی:

olist_orders_dataset
olist_order_items_dataset
olist_products_dataset
olist_order_reviews_dataset
6) دوباره dbt اجرا کن
docker exec -it customer_airflow bash
بعد:

cd /opt/customer_analytics_dbt
dbt run
برای اینکه دقیق راهنمایی کنم، الان فقط این دو خروجی را بفرست:

dir
از مسیر:

C:\Users\PC\Downloads\Project
dir data_loader
چون باید ببینیم اصلاً load_data.py و Dockerfile وجود دارند یا نه.


data loader to foldere scripts/load_raw_data.py hast 

خوب، پس پروژه‌ات با README کمی فرق دارد. تو پوشه‌ی data_loader جدا نداری و به جای آن یک اسکریپت داری:

scripts/
└── load_raw_data.py
یعنی احتمالاً باید این اسکریپت را دستی اجرا کنیم تا CSVها را وارد PostgreSQL کند.

اول ساختار را چک کنیم.

از ریشه پروژه اجرا کن:

cd C:\Users\PC\Downloads\Project
dir scripts
باید چیزی شبیه این ببینی:

scripts
    load_raw_data.py
مرحله ۱: ببین اسکریپت چه پکیج‌هایی لازم دارد
باز کن:

scripts/load_raw_data.py
یا در PowerShell:

type scripts\load_raw_data.py
دنبال چیزهایی مثل این بگرد:

import pandas
import psycopg2
یا:

from sqlalchemy import create_engine
مرحله ۲: احتمالاً باید از داخل Airflow container اجرا شود
چون PostgreSQL و محیط پروژه داخل Docker هستند.

اول وارد Airflow شو:

docker exec -it customer_airflow bash
بعد:

cd /opt/airflow
ببین scripts mount شده یا نه:

ls
اگر پوشه scripts را نمی‌بینی، باید در docker-compose.yml اضافه شود:

volumes:
  - ./scripts:/opt/airflow/scripts
مرحله ۳: اجرای loader
اگر داخل کانتینر دیدی:

/opt/airflow/scripts/load_raw_data.py
اجرا کن:

python scripts/load_raw_data.py
مرحله ۴: اگر خطای اتصال PostgreSQL داد
داخل Docker نباید این باشد:

host="localhost"
باید:

host="postgres"
باشد.

مثلاً:

engine = create_engine(
    "postgresql://postgres:postgres@postgres:5432/customer_analytics"
)
مرحله ۵: بعد از موفقیت
چک کن:

docker exec -it customer_postgres psql -U postgres -d customer_analytics
داخل:

\dt
باید جدول‌های:

olist_orders_dataset
olist_order_items_dataset
olist_products_dataset
olist_order_reviews_dataset
را ببینی.

بعد دوباره:

docker exec -it customer_airflow bash

cd /opt/customer_analytics_dbt

dbt run
الان لطفاً محتوای فایل زیر را بفرست:

scripts/load_raw_data.py
یا حداقل ۵۰ خط اولش.

چون باید ببینیم loader برای اجرا روی ویندوز نوشته شده یا Docker، و دقیقاً چه دستور اجرای صحیحی دارد.


(venv) PS C:\Users\PC\Downloads\Project> docker compose up -d                 
validating C:\Users\PC\Downloads\Project\docker-compose.yml:  additional properties 'data_loader' not allowed
   
What's next:
    Debug this Compose error with Gordon → docker ai "help me fix this compose error"

این خطا دوباره همان مشکل ساختار YAML است:

additional properties 'data_loader' not allowed
یعنی data_loader را مثل قبل بیرون از services: گذاشتی.

احتمالاً الان فایل تو چیزی شبیه این شده:

services:

  postgres:
    ...

  airflow:
    ...

  api:
    ...


data_loader:
  build:
    context: ./scripts
در حالی که باید داخل services: باشد.

ساختار درست باید این شکلی باشد:
services:

  postgres:
    image: postgres:16
    container_name: customer_postgres

    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics

    ports:
      - "5432:5432"

    volumes:
      - postgres_data:/var/lib/postgresql/data


  airflow:
    build: .

    container_name: customer_airflow

    depends_on:
      - postgres

    ports:
      - "8080:8080"


  api:
    build:
      context: ./api

    container_name: churn_api

    ports:
      - "8000:8000"


  data_loader:
    build:
      context: ./scripts

    container_name: customer_data_loader

    depends_on:
      - postgres

    volumes:
      - ./data:/data

    environment:
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics


volumes:
  postgres_data:
اما یک نکته مهم‌تر:

تو گفتی loader اینجاست:

scripts/load_raw_data.py
پس احتمالاً Dockerfile داخل scripts نداری.

این قسمت:

data_loader:
  build:
    context: ./scripts
فقط وقتی کار می‌کند که این فایل وجود داشته باشد:

scripts/
│
├── Dockerfile
└── load_raw_data.py
اگر Dockerfile نداری، این روش درست نیست.

راه ساده‌تر برای پروژه فعلی تو:

اصلاً data_loader را به compose اضافه نکن. مستقیم اسکریپت را اجرا کن.

اول ببین فایل چه dependency دارد:

در PowerShell:

type scripts\load_raw_data.py
و خروجی را بفرست.

من بر اساس همان بهت می‌گویم دقیقاً این را اجرا کنی:

روی ویندوز داخل venv
یا

داخل Airflow container
یا

با یک command موقت Docker

الان مشکل اصلی این نیست که Docker خراب است؛ فقط باید بفهمیم load_raw_data.py برای چه محیطی نوشته شده.


(venv) PS C:\Users\PC\Downloads\Project> docker compose up -d
#1 [internal] load local bake definitions
#1 reading from stdin 1.40kB done
#1 DONE 0.0s

#2 [internal] load build definition from Dockerfile
#2 transferring dockerfile: 2B done
#2 DONE 0.0s
[+] up 0/1
 - Image project-data_loader Building                                                                                                                                                                0.4s
failed to solve: failed to read dockerfile: open Dockerfile: no such file or directory



View build details: docker-desktop://dashboard/build/default/default/4tjrb6c0hz5zcjfqucipwk7da


الان خطا کاملاً مشخص است:

failed to read dockerfile: open Dockerfile: no such file or directory
یعنی Docker برای سرویس data_loader این را اجرا کرده:

build:
  context: ./scripts
و رفته داخل:

Project/scripts/
دنبال فایل:

Dockerfile
گشته، ولی پیدا نکرده.

ساختار فعلی تو احتمالاً این است:

Project/
│
├── scripts/
│   └── load_raw_data.py
│
├── data/
├── api/
├── customer_analytics_dbt/
├── docker-compose.yml
ولی Docker انتظار دارد:

scripts/
├── Dockerfile
└── load_raw_data.py
راه ساده‌تر (پیشنهادی): data_loader را از compose حذف کن
چون تو یک اسکریپت ساده داری، لازم نیست برایش container بسازی.

از docker-compose.yml این بخش را پاک کن:

data_loader:
  build:
    context: ./scripts
  container_name: customer_data_loader
  depends_on:
    - postgres
  volumes:
    - ./data:/data
بعد:

docker compose up -d
حالا load_raw_data.py را دستی اجرا کن
اول ببین اسکریپت چه می‌خواهد:

type scripts\load_raw_data.py
ولی احتمال زیاد باید از همین محیط venv اجرا شود:

python scripts\load_raw_data.py
اگر خطای اتصال PostgreSQL گرفتی
مثلاً:

could not connect to server
چون PostgreSQL داخل Docker است، ممکن است اسکریپت روی ویندوز نتواند وصل شود.

در آن صورت باید connection string داخل فایل را تغییر دهیم.

مثلاً اگر داری:

host="localhost"
باید برای اجرای ویندوز:

host="localhost"
بماند، چون پورت را expose کردی:

ports:
  - "5432:5432"
اما اگر داخل کانتینر اجرا شود باید:

host="postgres"
باشد.

فعلاً این دو کار را انجام بده:

بخش data_loader را از compose حذف کن.

این دستور را بزن:

python scripts\load_raw_data.py
اگر خطا داد، کل خروجی را بفرست.

همچنین اگر خواستی، خروجی این دستور را هم بفرست:

type scripts\load_raw_data.py
تا دقیق بگویم چه تنظیمی لازم دارد.


nemikham dasti ejra konam khob 

باشه، اگر نمی‌خواهی دستی اجرا کنی، باید load_raw_data.py را هم مثل یک Docker service واقعی اجرا کنیم. الان فقط مشکل این است که برایش Dockerfile نداری.

باید داخل پوشه scripts یک Dockerfile بسازیم.

ساختار باید این شود:

Project/
│
├── scripts/
│   ├── Dockerfile
│   └── load_raw_data.py
│
├── data/
│   └── raw/
│       ├── olist_orders_dataset.csv
│       ├── olist_order_items_dataset.csv
│       ├── olist_products_dataset.csv
│       └── olist_order_reviews_dataset.csv
│
└── docker-compose.yml
1) داخل scripts فایل Dockerfile بساز
مسیر:

Project/scripts/Dockerfile
محتوا:

FROM python:3.12-slim

WORKDIR /app

COPY load_raw_data.py .

RUN pip install pandas sqlalchemy psycopg2-binary

CMD ["python", "load_raw_data.py"]
2) docker-compose.yml بخش data_loader را این‌طور بگذار
داخل services::

  data_loader:
    build:
      context: ./scripts

    container_name: customer_data_loader

    depends_on:
      - postgres

    volumes:
      - ./data:/data

    environment:
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics
3) دوباره build کن
اول کانتینرهای قبلی:

docker compose down
بعد:

docker compose up --build -d
4) لاگ loader را ببین
چون loader یک کار یک‌باره است (CSV → PostgreSQL)، ممکن است سریع تمام شود.

بزن:

docker logs customer_data_loader
باید چیزی شبیه:

Loading olist_orders_dataset.csv
Loading olist_products_dataset.csv
Data loading completed
ببینی.

یک نکته مهم
قبل از اجرا باید مطمئن شویم load_raw_data.py مسیر CSV را درست می‌خواند.

اگر داخل فایل نوشته باشد:

pd.read_csv("data/raw/olist_orders_dataset.csv")
داخل Docker اشتباه می‌شود.

چون volume ما این است:

./data:/data
پس داخل container مسیر باید:

/data/raw/olist_orders_dataset.csv
باشد.

برای اینکه مجبور نشویم حدس بزنیم، لطفاً فقط این قسمت از فایل را بفرست:

scripts/load_raw_data.py
قسمت‌هایی که:

read_csv

connection به PostgreSQL

engine/create_engine

هستند.

بعد Dockerfile را دقیق با کد خودت هماهنگ می‌کنیم.


New_Item Dockerfile
New_Item : The term 'New_Item' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was included, verify that the path 
is correct and try again.
At line:1 char:1
+ New_Item Dockerfile
+ ~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (New_Item:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException

این خطا به این دلیل است که:

New_Item Dockerfile
دستور صحیح PowerShell نیست. در PowerShell اسم دستور با فاصله نوشته نمی‌شود.

برای ساخت فایل Dockerfile این کار را انجام بده:

1) برو داخل پوشه scripts
cd C:\Users\PC\Downloads\Project\scripts
2) فایل Dockerfile بساز
New-Item Dockerfile
یا کوتاه‌تر:

ni Dockerfile
باید خروجی شبیه این بدهد:

Directory: C:\Users\PC\Downloads\Project\scripts

Mode                 LastWriteTime
----                 -------------
-a----               Dockerfile
3) فایل را باز کن
با Notepad:

notepad Dockerfile
این محتوا را داخلش بگذار:

FROM python:3.12-slim

WORKDIR /app

COPY load_raw_data.py .

RUN pip install pandas sqlalchemy psycopg2-binary

CMD ["python", "load_raw_data.py"]
Save کن و ببند.

4) برگرد به ریشه پروژه
cd C:\Users\PC\Downloads\Project
بعد:

docker compose up --build -d
اگر بعد از build خطایی از خود load_raw_data.py گرفتی (مثلاً مسیر CSV یا اتصال دیتابیس)، آن مرحله بعدی است. الان فقط باید Docker بتواند image مربوط به data_loader را بسازد.


                                                                                                                                       0.0s
 ✘ service... Error response from daemon: Conflict. The container name "/customer_data_loader" is already in use by container "bdf8a6a33a815f06b856ac5948c59794b0c022aa838a0da9bf2df23858d91d8e". You have to remove (or rename) that container to be able to reuse that name.  0.0s

الان Dockerfile مشکلش حل شده. خطای جدید فقط به خاطر کانتینر قبلی customer_data_loader است که هنوز وجود دارد.

خطا:

Conflict. The container name "/customer_data_loader" is already in use
یعنی قبلاً یک کانتینر با این نام ساخته شده و Docker نمی‌تواند دوباره همان اسم را استفاده کند.

راه‌حل:
اول کانتینر قبلی را حذف کن:

docker rm -f customer_data_loader
بعد دوباره اجرا کن:

docker compose up --build -d
اگر می‌خواهی همه چیز را تمیز ریست کنی:

docker compose down
بعد:

docker rm -f customer_data_loader customer_postgres customer_airflow churn_api
(اگر بعضی‌ها وجود نداشتند، مهم نیست.)

بعد:

docker compose up --build -d
بعد از بالا آمدن، لاگ data loader را ببین:

docker logs customer_data_loader
اگر موفق باشد باید ببینی که CSVها در PostgreSQL load شده‌اند.

بعد بررسی کن:

docker exec -it customer_postgres psql -U postgres -d customer_analytics
داخل PostgreSQL:

\dt
باید جدول‌های:

olist_orders_dataset
olist_order_items_dataset
olist_products_dataset
olist_order_reviews_dataset
وجود داشته باشند.

بعد می‌توانی دوباره:

docker exec -it customer_airflow bash
و:

cd /opt/customer_analytics_dbt
dbt run
را اجرا کنی.


(venv) PS C:\Users\PC\Downloads\Project> dbt run                     
dbt : The term 'dbt' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was included, verify that the path is correct 
and try again.
At line:1 char:1
+ dbt run
+ ~~~
    + CategoryInfo          : ObjectNotFound: (dbt:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException

این خطا طبیعی است. تو دوباره داری dbt run را در PowerShell ویندوز اجرا می‌کنی:

(venv) PS C:\Users\PC\Downloads\Project> dbt run
ولی dbt در پروژه تو داخل کانتینر Airflow نصب شده، نه داخل venv ویندوز.

همان کاری که قبلاً انجام دادی را انجام بده:

docker exec -it customer_airflow bash
بعد داخل کانتینر:

cd /opt/customer_analytics_dbt
dbt run
قبل از dbt بهتر است مطمئن شویم data loader واقعاً کار کرده:

از PowerShell:

docker logs customer_data_loader
اگر موفق باشد باید چیزی شبیه این ببینی:

Loading olist_orders_dataset.csv
Loading olist_order_items_dataset.csv
Loading olist_products_dataset.csv
Loading completed
بعد جدول‌ها را چک کن:

docker exec -it customer_postgres psql -U postgres -d customer_analytics
داخل PostgreSQL:

\dt
باید جدول‌های raw را ببینی:

olist_orders_dataset
olist_order_items_dataset
olist_products_dataset
olist_order_reviews_dataset
اگر این‌ها وجود داشتند، dbt run داخل Airflow باید بدون خطای قبلی اجرا شود.

اگر docker logs customer_data_loader خطا داد، همان خروجی را بفرست.


 
(venv) PS C:\Users\PC\Downloads\Project> docker exec -it customer_airflow bash
airflow@366cf9021939:/opt/airflow$ cd /opt/customer_analytics_dbt
dbt run
bash: cd: /opt/customer_analytics_dbt: No such file or directory
Usage: dbt run [OPTIONS]
Try 'dbt run --help' for help.

Error: Invalid value for '--profiles-dir': Path '/home/airflow/.dbt' does not exist.

الان دو مشکل جدا داریم:

مشکل ۱:
cd: /opt/customer_analytics_dbt: No such file or directory
یعنی این بار کانتینر customer_airflow جدیدی که ساخته شده، پوشه dbt را داخل خودش ندارد.

قبلاً این مسیر وجود داشت چون در docker-compose.yml این volume را داشتی:

- ./customer_analytics_dbt:/opt/customer_analytics_dbt
احتمالاً در تغییرات اخیر compose این بخش حذف شده است.

مشکل ۲:
Invalid value for '--profiles-dir': Path '/home/airflow/.dbt' does not exist
یعنی dbt دنبال تنظیمات profiles.yml می‌گردد ولی پوشه تنظیمات dbt وجود ندارد.

مرحله ۱: docker-compose.yml را اصلاح کن
در سرویس airflow باید این volumeها وجود داشته باشند:

airflow:
  build: .

  container_name: customer_airflow

  volumes:
    - ./airflow/dags:/opt/airflow/dags
    - ./src:/opt/airflow/src
    - ./customer_analytics_dbt:/opt/customer_analytics_dbt
    - ./data:/opt/airflow/data
    - ./profiles:/home/airflow/.dbt
خط مهم:

- ./customer_analytics_dbt:/opt/customer_analytics_dbt
برای پروژه dbt است.

و:

- ./profiles:/home/airflow/.dbt
برای profiles.yml است.

مرحله ۲: ببین پوشه profiles داری یا نه
در PowerShell:

cd C:\Users\PC\Downloads\Project
dir
باید چیزی مثل این داشته باشی:

customer_analytics_dbt
profiles
docker-compose.yml
اگر profiles نداری، بساز:

mkdir profiles
داخلش بساز:

profiles/
└── profiles.yml
مرحله ۳: کانتینرها را دوباره بساز
بعد از تغییر compose:

docker compose down
بعد:

docker compose up --build -d
مرحله ۴: دوباره وارد Airflow شو
docker exec -it customer_airflow bash
تست:

ls /opt/customer_analytics_dbt
باید فایل‌های dbt را ببینی:

dbt_project.yml
models
macros
بعد:

cd /opt/customer_analytics_dbt
dbt run
یک چیز لازم دارم تا دقیق تنظیمش کنیم: لطفاً خروجی این دستور را بفرست:

dir C:\Users\PC\Downloads\Project
می‌خواهم ببینم آیا پوشه profiles و customer_analytics_dbt واقعاً در ریشه پروژه هستند یا نه.


docker compose ro kollan kharab kardi 
avalesh chi bud hamuno bede behem 

حق داری؛ با تغییرات متعدد، فایل docker-compose.yml از حالت اولیه‌ای که پروژه با آن ساخته شده بود خارج شد. برگردیم به یک نسخه ساده و نزدیک به همان چیزی که اول داشتی.

اولین نسخه‌ای که فرستادی این بود (با اصلاح فقط مشکل api که بیرون services بود):

services:

  postgres:
    image: postgres:16

    container_name: customer_postgres

    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics

    ports:
      - "5432:5432"

    volumes:
      - postgres_data:/var/lib/postgresql/data


  airflow:
    build: .

    container_name: customer_airflow

    depends_on:
      - postgres

    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor

      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://postgres:postgres@postgres:5432/customer_analytics

      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics

    ports:
      - "8080:8080"

    volumes:
      - ./airflow/dags:/opt/airflow/dags
      - ./src:/opt/airflow/src
      - ./customer_analytics_dbt:/opt/customer_analytics_dbt
      - ./data:/opt/airflow/data

    command:
      airflow standalone


  api:
    build:
      context: ./api

    container_name: churn_api

    ports:
      - "8000:8000"

    volumes:
      - ./ml:/app/ml


volumes:
  postgres_data:
این همان ساختار اصلی تو بود:

PostgreSQL

Airflow

API

dbt mount شده داخل Airflow

فعلاً data_loader را اضافه نکن. چون README با ساختار واقعی پروژه‌ات یکی نیست و باعث شد compose را بی‌دلیل پیچیده کنیم.

بعد از گذاشتن این فایل:

پاک‌سازی کانتینرهای قبلی:

docker compose down
اگر conflict داشتی:

docker rm -f customer_postgres customer_airflow churn_api customer_data_loader
بالا آوردن:

docker compose up -d
بعد تست:

docker compose ps
بعد از این، فقط باید روی scripts/load_raw_data.py کار کنیم، نه تغییر compose.

یک نکته: من نباید بدون دیدن ساختار واقعی پروژه، data_loader را به compose اضافه می‌کردم. مسیر درست این است که اول compose اصلی را پایدار کنیم، بعد loader را متناسب با فایل واقعی پروژه اضافه کنیم.


ama man mikham data load ham tush bashe 

باشه، پس data_loader هم باید داخل docker-compose.yml باشد. ولی باید درست اضافه شود؛ نه مثل قبل که فقط build: ./scripts گذاشتیم و Docker دنبال Dockerfile گشت.

با توجه به اینکه loader تو اینجاست:

scripts/
└── load_raw_data.py
بهترین حالت این است که برایش یک Dockerfile مخصوص بسازیم و به compose اضافه کنیم.

نسخه کامل docker-compose.yml:

services:

  postgres:
    image: postgres:16

    container_name: customer_postgres

    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics

    ports:
      - "5432:5432"

    volumes:
      - postgres_data:/var/lib/postgresql/data


  data_loader:
    build:
      context: ./scripts

    container_name: customer_data_loader

    depends_on:
      - postgres

    volumes:
      - ./data:/data

    environment:
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics


  airflow:
    build: .

    container_name: customer_airflow

    depends_on:
      - postgres
      - data_loader

    environment:

      AIRFLOW__CORE__EXECUTOR: LocalExecutor

      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://postgres:postgres@postgres:5432/customer_analytics

      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics

    ports:
      - "8080:8080"

    volumes:
      - ./airflow/dags:/opt/airflow/dags
      - ./src:/opt/airflow/src
      - ./customer_analytics_dbt:/opt/customer_analytics_dbt
      - ./data:/opt/airflow/data

    command:
      airflow standalone


  api:
    build:
      context: ./api

    container_name: churn_api

    ports:
      - "8000:8000"

    volumes:
      - ./ml:/app/ml


volumes:

  postgres_data:
حالا باید این فایل را هم بسازی:

مسیر:

Project/scripts/Dockerfile
محتوا:

FROM python:3.12-slim

WORKDIR /app

COPY load_raw_data.py .

RUN pip install pandas sqlalchemy psycopg2-binary

CMD ["python", "load_raw_data.py"]
ساختار نهایی:

Project
│
├── docker-compose.yml
│
├── scripts
│   ├── Dockerfile
│   └── load_raw_data.py
│
├── data
│   └── raw
│       ├── olist_orders_dataset.csv
│       ├── olist_order_items_dataset.csv
│       ├── olist_products_dataset.csv
│       └── olist_order_reviews_dataset.csv
│
├── customer_analytics_dbt
├── api
└── ml
بعد اجرا:

docker compose down
اگر کانتینرهای قدیمی conflict دادند:

docker rm -f customer_postgres customer_airflow churn_api customer_data_loader
بعد:

docker compose up --build -d
و لاگ loader:

docker logs customer_data_loader
فقط یک چیز هنوز مهم است: من باید ببینم load_raw_data.py چطور نوشته شده، چون ممکن است مسیر CSV داخلش data/raw باشد و داخل Docker باید /data/raw شود.

این دستور را بزن و خروجی بده:

type scripts\load_raw_data.py
تا Dockerfile و volume را دقیق با کد خودت هماهنگ کنیم.


(venv) PS C:\Users\PC\Downloads\Project> docker logs customer_data_loader
Missing file: ../data/olist_orders_dataset.csv
Missing file: ../data/olist_order_items_dataset.csv
Missing file: ../data/olist_products_dataset.csv
Missing file: ../data/olist_order_reviews_dataset.csv
Missing file: ../data/olist_customers_dataset.csv
Missing file: ../data/olist_sellers_dataset.csv
Missing file: ../data/olist_geolocation_dataset.csv
Missing file: ../data/olist_order_payments_dataset.csv
Missing file: ../data/product_category_name_translation.csv
Finished loading data

خوب، الان data_loader اجرا شده ولی فایل‌ها را پیدا نکرده. مشکل دیگر Docker نیست؛ مشکل مسیر فایل‌ها است.

لاگ:

Missing file: ../data/olist_orders_dataset.csv
یعنی داخل کانتینر، اسکریپت دنبال این مسیر می‌گردد:

../data/olist_orders_dataset.csv
ولی ما volume را این‌طور وصل کردیم:

volumes:
  - ./data:/data
پس داخل کانتینر فایل‌ها اینجا هستند:

/data/raw/olist_orders_dataset.csv
نه:

../data/olist_orders_dataset.csv
راه درست: volume را مطابق اسکریپت تغییر بده
در docker-compose.yml بخش data_loader را عوض کن:

از:

volumes:
  - ./data:/data
به:

volumes:
  - ./data:/app/data
چون Dockerfile ما دارد:

WORKDIR /app
پس مسیر:

/app
و:

../data
می‌شود:

/data
اما اگر فایل‌های تو در:

Project/data/raw/
هستند، هنوز یک اختلاف داریم.

یک سؤال مهم: فایل‌ها دقیقاً کجا هستند؟
در PowerShell این را بزن:

dir data
و:

dir data\raw
ببین خروجی چیست.

چون اسکریپت انتظار دارد:

data/
├── olist_orders_dataset.csv
├── olist_order_items_dataset.csv
ولی README تو گفته:

data/
└── raw/
    ├── olist_orders_dataset.csv
اگر فایل‌ها در data/raw هستند (احتمال زیاد)
ساده‌ترین راه این است که در compose بگذاریم:

data_loader:
  volumes:
    - ./data/raw:/data
بعد داخل container:

/data/olist_orders_dataset.csv
داریم.

اما اسکریپت دنبال:

../data/olist_orders_dataset.csv
است، پس باید volume را این‌طور بگذاریم:

data_loader:
  volumes:
    - ./data:/app/data
بعد از تغییر:

docker compose down
و:

docker compose up --build -d
بعد:

docker logs customer_data_loader
فعلاً فقط خروجی این دو دستور را بفرست:

dir data
و

dir data\raw
تا دقیق بگویم کدام volume باید باشد.


csv ha tuye data/raw hastan 

خوب، پس مشکل مشخص شد. CSVها اینجا هستند:

Project/
└── data/
    └── raw/
        ├── olist_orders_dataset.csv
        ├── olist_order_items_dataset.csv
        ├── olist_products_dataset.csv
        └── ...
ولی load_raw_data.py دنبال این مسیر می‌گردد:

../data/olist_orders_dataset.csv
یعنی انتظار دارد فایل‌ها مستقیم داخل data باشند، نه داخل data/raw.

دو راه داری:

راه ۱ (پیشنهادی): فقط volume را تغییر بده
در docker-compose.yml بخش data_loader را این‌طور کن:

  data_loader:
    build:
      context: ./scripts

    container_name: customer_data_loader

    depends_on:
      - postgres

    volumes:
      - ./data/raw:/app/data

    environment:
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics
چون Dockerfile دارد:

WORKDIR /app
داخل container:

/app
├── load_raw_data.py
└── data
    ├── olist_orders_dataset.csv
    └── ...
و مسیر:

../data/file.csv
از داخل /app تبدیل می‌شود به:

/data/file.csv
اما اینجا یک مشکل کوچک داریم: اگر واقعاً اسکریپت از /app اجرا شود، ../data می‌رود به ریشه container، نه /app/data.

پس راه مطمئن‌تر:

راه ۲ (بهتر): اسکریپت را با ساختار README هماهنگ کن
در scripts/load_raw_data.py این قسمت را پیدا کن:

احتمالاً چیزی شبیه:

"../data/olist_orders_dataset.csv"
همه را تغییر بده به:

"../data/raw/olist_orders_dataset.csv"
مثلاً:

files = {
    "olist_orders_dataset": "../data/raw/olist_orders_dataset.csv",
    "olist_order_items_dataset": "../data/raw/olist_order_items_dataset.csv",
    "olist_products_dataset": "../data/raw/olist_products_dataset.csv",
}
بعد Dockerfile لازم نیست تغییر کند.

بعد دوباره:

docker compose down
و:

docker compose up --build -d
بعد:

docker logs customer_data_loader
این بار باید به جای:

Missing file
چیزی مثل:

Loading olist_orders_dataset.csv
Loading olist_order_items_dataset.csv
Finished loading data
ببینی.

من راه ۲ را پیشنهاد می‌کنم، چون README پروژه هم گفته:

data/raw/
و dbt هم با همین ساختار ساخته شده.

اگر خواستی، ۲۰ خط اول scripts/load_raw_data.py را بفرست تا دقیق بگویم کدام خط را تغییر بدهی.


import pandas as pd
from sqlalchemy import create_engine
import os


# PostgreSQL connection
DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@localhost:5432/customer_analytics"
)

engine = create_engine(DATABASE_URL)


DATA_PATH = "../data/raw"


tables = {
    "olist_orders_dataset.csv": "olist_orders_dataset",
    "olist_order_items_dataset.csv": "olist_order_items_dataset",
    "olist_products_dataset.csv": "olist_products_dataset",
    "olist_order_reviews_dataset.csv": "olist_order_reviews_dataset",
    "olist_customers_dataset.csv": "olist_customers_dataset",
    "olist_sellers_dataset.csv": "olist_sellers_dataset",
    "olist_geolocation_dataset.csv": "olist_geolocation_dataset",
    "olist_order_payments_dataset.csv": "olist_order_payments_dataset",
    "product_category_name_translation.csv": "product_category_name_translation"

}


for file_name, table_name in tables.items():

    file_path = os.path.join(DATA_PATH, file_name)

    if not os.path.exists(file_path):
        print(f"Missing file: {file_path}")
        continue

    print(f"Loading {file_name}...")

    df = pd.read_csv(file_path)

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
        schema="public"
    )

    print(f"Loaded {table_name}: {len(df)} rows")


print("Finished loading data")

خوب، الان مشکل دقیق مشخص شد. فایل load_raw_data.py برای اجرا روی سیستم خودت نوشته شده، نه داخل Docker.

دو مشکل داریم:

مشکل ۱: مسیر فایل‌ها
الان داری:

DATA_PATH = "../data/raw"
داخل Docker، چون WORKDIR ما /app است، این تبدیل می‌شود به:

/app/../data/raw
یعنی:

/data/raw
اما ما volume را درست وصل نکردیم.

مشکل ۲: اتصال PostgreSQL
الان داری:

DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@localhost:5432/customer_analytics"
)
داخل Docker، localhost یعنی خود کانتینر data_loader، نه کانتینر PostgreSQL.

باید بشود:

postgres
چون اسم سرویس Docker تو است.

فایل را این‌طور تغییر بده:
این قسمت:

DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@localhost:5432/customer_analytics"
)
تبدیل شود به:

DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@postgres:5432/customer_analytics"
)
و این:

DATA_PATH = "../data/raw"
بماند.

بعد docker-compose برای data_loader باید این باشد:
  data_loader:
    build:
      context: ./scripts

    container_name: customer_data_loader

    depends_on:
      - postgres

    volumes:
      - ./data:/data

    environment:
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics
اما چون اسکریپت از:

../data/raw
می‌خواند، داخل Docker باید مسیر زیر وجود داشته باشد:

/data/raw
پس این volume درست است:

- ./data:/data
حالا:

1. کانتینر قبلی loader را پاک کن:
docker rm -f customer_data_loader
2. دوباره build کن:
docker compose up --build -d
3. لاگ را ببین:
docker logs customer_data_loader
باید ببینی:

Loading olist_orders_dataset.csv...
Loaded olist_orders_dataset: xxxx rows

Loading olist_order_items_dataset.csv...
Loaded olist_order_items_dataset: xxxx rows

Finished loading data
بعد از موفقیت:

چک کن PostgreSQL جدول‌ها را دارد:

docker exec -it customer_postgres psql -U postgres -d customer_analytics
داخل:

\dt
بعد dbt:

docker exec -it customer_airflow bash
داخل:

cd /opt/customer_analytics_dbt
dbt run
این مسیر با معماری اصلی پروژه‌ات هماهنگ می‌شود.


alan  load_raw_data.py chejuri taghir bedam k doros she

فقط دو قسمت از load_raw_data.py را تغییر بده. بقیه کد دست نزن.

الان این قسمت داری:

DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@localhost:5432/customer_analytics"
)
تغییر بده به:

DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@postgres:5432/customer_analytics"
)
چون داخل Docker اسم سرویس PostgreSQL این است:

postgres:
نه localhost.

قسمت دوم:

الان داری:

DATA_PATH = "../data/raw"
این را تغییر نده. همین درست است، چون در Docker با volume این مسیر را می‌سازیم.

پس فایل تو فقط این تغییر را دارد:

import pandas as pd
from sqlalchemy import create_engine
import os


# PostgreSQL connection
DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@postgres:5432/customer_analytics"
)

engine = create_engine(DATABASE_URL)


DATA_PATH = "../data/raw"


tables = {
    "olist_orders_dataset.csv": "olist_orders_dataset",
    "olist_order_items_dataset.csv": "olist_order_items_dataset",
    "olist_products_dataset.csv": "olist_products_dataset",
    "olist_order_reviews_dataset.csv": "olist_order_reviews_dataset",
    "olist_customers_dataset.csv": "olist_customers_dataset",
    "olist_sellers_dataset.csv": "olist_sellers_dataset",
    "olist_geolocation_dataset.csv": "olist_geolocation_dataset",
    "olist_order_payments_dataset.csv": "olist_order_payments_dataset",
    "product_category_name_translation.csv": "product_category_name_translation"
}


for file_name, table_name in tables.items():

    file_path = os.path.join(DATA_PATH, file_name)

    if not os.path.exists(file_path):
        print(f"Missing file: {file_path}")
        continue

    print(f"Loading {file_name}...")

    df = pd.read_csv(file_path)

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
        schema="public"
    )

    print(f"Loaded {table_name}: {len(df)} rows")


print("Finished loading data")
بعد save کن.

حالا:

docker rm -f customer_data_loader
بعد:

docker compose up --build -d
بعد:

docker logs customer_data_loader
باید خروجی شبیه این شود:

Loading olist_orders_dataset.csv...
Loaded olist_orders_dataset: xxxx rows
Loading olist_order_items_dataset.csv...
Loaded olist_order_items_dataset: xxxx rows
...
Finished loading data
اگر باز Missing file دیدی، مشکل فقط volume در docker-compose.yml است، نه Python.


(venv) PS C:\Users\PC\Downloads\Project> docker logs customer_data_loader
Missing file: ../data/raw/olist_orders_dataset.csv
Missing file: ../data/raw/olist_order_items_dataset.csv
Missing file: ../data/raw/olist_products_dataset.csv
Missing file: ../data/raw/olist_order_reviews_dataset.csv
Missing file: ../data/raw/olist_customers_dataset.csv
Missing file: ../data/raw/olist_sellers_dataset.csv
Missing file: ../data/raw/olist_geolocation_dataset.csv
Missing file: ../data/raw/olist_order_payments_dataset.csv
Missing file: ../data/raw/product_category_name_translation.csv
Finished loading data

الان مشکل فقط مسیر volume داخل Docker است. خود Python درست شده، ولی داخل container فایل‌ها در مسیری که اسکریپت انتظار دارد نیستند.

اسکریپت می‌گوید:

DATA_PATH = "../data/raw"
و Dockerfile ما:

WORKDIR /app
پس داخل container دنبال این می‌گردد:

/data/raw/olist_orders_dataset.csv
اما این مسیر وجود ندارد.

1) اول ببین الان داخل container چه چیزی mount شده
این را بزن:

docker exec -it customer_data_loader bash
بعد داخل container:

ls -la
و:

ls -la /data
و:

ls -la /data/raw
احتمالاً /data/raw وجود ندارد.

2) docker-compose را اصلاح کن
در بخش data_loader باید دقیقاً این باشد:

  data_loader:
    build:
      context: ./scripts

    container_name: customer_data_loader

    depends_on:
      - postgres

    volumes:
      - ./data:/data

    environment:
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics
یعنی:

در ویندوز:

Project/data/raw/*.csv
باید داخل container بشود:

/data/raw/*.csv
3) بعد recreate کن (مهم)
فقط restart کافی نیست:

docker compose down
بعد:

docker compose up --build -d
4) دوباره تست:
docker exec -it customer_data_loader bash
داخل:

ls /data/raw
باید ببینی:

olist_orders_dataset.csv
olist_order_items_dataset.csv
olist_products_dataset.csv
...
بعد خارج شو:

exit
و:

docker logs customer_data_loader
اگر هنوز فایل‌ها را ندید، خروجی این دستور را بفرست:

docker inspect customer_data_loader
قسمت Mounts را لازم دارم تا ببینیم Docker واقعاً چه مسیری را وصل کرده.


Finished loading data
(venv) PS C:\Users\PC\Downloads\Project> docker exec -it customer_data_loader bash

What's next:
    Try Docker Debug for seamless, persistent debugging tools in any container or image → docker debug customer_data_loader
    Learn more at https://docs.docker.com/go/debug-cli/
Error response from daemon: container 57d83b83ce0011d9c32284713069e59546dc83047e66fe91ce624e1f94f52545 is not running

این پیام یعنی data_loader کارش را انجام داده و بعد متوقف شده. این اتفاق برای loaderهایی که فقط یک بار CSV را import می‌کنند طبیعی است.

یعنی:

Finished loading data
احتمالاً یعنی اسکریپت اجرا شده و تمام شده، بعد container exit کرده. به همین دلیل وقتی می‌زنی:

docker exec -it customer_data_loader bash
می‌گوید:

container is not running
چون دیگر چیزی برای اجرا داخل آن فعال نیست.

الان مهم‌ترین چیز این است که ببینیم واقعاً داده‌ها وارد PostgreSQL شده‌اند یا نه.

این را اجرا کن:

docker exec -it customer_postgres psql -U postgres -d customer_analytics
داخل PostgreSQL:

\dt
باید جدول‌هایی مثل این‌ها را ببینی:

olist_orders_dataset
olist_order_items_dataset
olist_products_dataset
olist_order_reviews_dataset
olist_customers_dataset
...
اگر دیدی، یعنی data loader موفق بوده.

بعد برو سراغ dbt:

docker exec -it customer_airflow bash
داخل:

cd /opt/customer_analytics_dbt
dbt run
اگر در \dt هیچ جدولی نبود، این را بزن:

docker logs customer_data_loader
و خروجی کاملش را بفرست.

یک نکته: برای data_loader بهتر است restart نگذاری، چون این سرویس مثل worker دائمی نیست؛ یک job یک‌باره است:

CSV → PostgreSQL → exit
که دقیقاً رفتار مورد انتظار است.


(venv) PS C:\Users\PC\Downloads\Project> docker logs customer_data_loader
Missing file: ../data/raw/olist_orders_dataset.csv
Missing file: ../data/raw/olist_order_items_dataset.csv
Missing file: ../data/raw/olist_products_dataset.csv
Missing file: ../data/raw/olist_order_reviews_dataset.csv
Missing file: ../data/raw/olist_customers_dataset.csv
Missing file: ../data/raw/olist_sellers_dataset.csv
Missing file: ../data/raw/olist_geolocation_dataset.csv
Missing file: ../data/raw/olist_order_payments_dataset.csv
Missing file: ../data/raw/product_category_name_translation.csv
Finished loading data
(venv) PS C:\Users\PC\Downloads\Project> 

خوب، پس هنوز data loader موفق نشده. پیغام:

Missing file: ../data/raw/olist_orders_dataset.csv
یعنی اسکریپت اجرا شده، ولی داخل container فایل‌های CSV را پیدا نمی‌کند. Finished loading data فقط یعنی حلقه تمام شده، نه اینکه داده‌ها load شده‌اند.

مشکل از docker-compose.yml یا مسیر mount است.

1) اول docker-compose.yml را چک کن
بخش data_loader باید دقیقاً این باشد:

  data_loader:
    build:
      context: ./scripts

    container_name: customer_data_loader

    depends_on:
      - postgres

    volumes:
      - ./data:/data

    environment:
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics
2) یک تغییر کوچک در Python بده (مطمئن‌ترین راه)
در load_raw_data.py این خط:

DATA_PATH = "../data/raw"
را عوض کن به:

DATA_PATH = "/data/raw"
چون ما در Docker داریم:

./data:/data
یعنی:

ویندوز:

Project/data/raw/*.csv
داخل Docker:

/data/raw/*.csv
3) دوباره image و container را بساز
حتماً rebuild کن:

docker compose down
بعد:

docker compose up --build -d
4) لاگ را دوباره ببین
docker logs customer_data_loader
باید چیزی شبیه این ببینی:

Loading olist_orders_dataset.csv...
Loaded olist_orders_dataset: 99441 rows

Loading olist_order_items_dataset.csv...
Loaded olist_order_items_dataset: xxxx rows

Finished loading data
بعد از این، dbt را اجرا می‌کنیم.

الان فقط همین یک تغییر لازم است:

DATA_PATH = "/data/raw"
این مشکل مسیر را کامل حل می‌کند.


(venv) PS C:\Users\PC\Downloads\Project> docker logs customer_data_loader
Error response from daemon: No such container: customer_data_loader

این خطا یعنی کانتینر customer_data_loader دیگر وجود ندارد؛ یا با docker compose down حذف شده یا اصلاً ساخته نشده است.

بیایید اول وضعیت را بررسی کنیم.

1. همه کانتینرها را ببین
docker ps -a
خروجی را بفرست.

2. اگر کانتینری با نام دیگری برای loader وجود دارد، همان را بررسی می‌کنیم.
اگر هیچ customer_data_loader وجود نداشت، دوباره اجرا کن:

docker compose up --build
این بار -d نزن.

این کار باعث می‌شود لاگ‌ها را مستقیم در ترمینال ببینی و دقیق مشخص شود:

آیا data_loader ساخته می‌شود؟

آیا فایل‌ها را پیدا می‌کند؟

آیا به PostgreSQL وصل می‌شود؟

یا در همان ابتدا خطا می‌دهد.

3. یک سؤال مهم
لطفاً این دو بخش را هم بفرست:

بخش data_loader از فایل docker-compose.yml

فایل scripts/Dockerfile

چون تا اینجا چند بار آن‌ها را تغییر داده‌ایم و احتمال دارد الان تنظیمات با load_raw_data.py هماهنگ نباشند.

با این سه مورد (docker ps -a، بخش data_loader از compose، و Dockerfile)، می‌توانیم دقیق مشکل را پیدا کنیم.


(venv) PS C:\Users\PC\Downloads\Project> docker ps -a
CONTAINER ID   IMAGE          COMMAND                  CREATED      STATUS                  PORTS     NAMES
472f59f150b8   churn-api      "uvicorn app.main:ap…"   6 days ago   Exited (0) 6 days ago             xenodochial_babbage
5ff643beb221   2602c79507e4   "uvicorn app.main:ap…"   6 days ago   Exited (1) 6 days ago             infallible_maxwell

عالی، این خروجی خیلی کمک کرد.

الان هیچ‌کدام از کانتینرهای پروژه‌ات وجود ندارند. نه:

customer_postgres

customer_airflow

customer_data_loader

فقط دو کانتینر قدیمی و بی‌ربط مانده‌اند:

472f59f150b8   churn-api
5ff643beb221   ...
یعنی الان اصلاً چیزی برای docker logs customer_data_loader وجود ندارد.

قدم بعدی
قبل از هر چیز، لطفاً این دو فایل را بفرست:

کل فایل docker-compose.yml فعلی

فایل scripts/Dockerfile

چون در طول گفتگو چند بار تغییر کرده‌اند و الان باید ببینیم وضعیت نهایی‌شان چیست.

بعد از دیدن این دو فایل، یک نسخه صحیح بهت می‌دهم و پروژه را از صفر بالا می‌آوریم:

docker compose up --build
و همان لحظه خطا را می‌بینیم و رفع می‌کنیم.

فعلاً docker compose up را اجرا نکن. اول docker-compose.yml و scripts/Dockerfile را بفرست تا مطمئن شویم تنظیمات درست هستند.


services:

  postgres:
    image: postgres:16

    container_name: customer_postgres

    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics

    ports:
      - "5432:5432"

    volumes:
      - postgres_data:/var/lib/postgresql/data


  data_loader:
    build:
      context: ./scripts

    container_name: customer_data_loader

    depends_on:
      - postgres

    volumes:
      - ./data:/data

    environment:
      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics


  airflow:
    build: .

    container_name: customer_airflow

    depends_on:
      - postgres
      - data_loader

    environment:

      AIRFLOW__CORE__EXECUTOR: LocalExecutor

      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://postgres:postgres@postgres:5432/customer_analytics

      POSTGRES_HOST: postgres
      POSTGRES_PORT: 5432
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: customer_analytics

    ports:
      - "8080:8080"

    volumes:
      - ./airflow/dags:/opt/airflow/dags
      - ./src:/opt/airflow/src
      - ./customer_analytics_dbt:/opt/customer_analytics_dbt
      - ./data:/opt/airflow/data

    command:
      airflow standalone


  api:
    build:
      context: ./api

    container_name: churn_api

    ports:
      - "8000:8000"

    volumes:
      - ./ml:/app/ml


volumes:

  postgres_data:

FROM python:3.12-slim

WORKDIR /app

COPY load_raw_data.py .

RUN pip install pandas sqlalchemy psycopg2-binary

CMD ["python", "load_raw_data.py"]

ممنون. الان مشکل را پیدا کردم.

مشکل از این است که Dockerfile و load_raw_data.py با هم هماهنگ نیستند.

در Dockerfile داری:

WORKDIR /app

COPY load_raw_data.py .
یعنی فایل در این مسیر اجرا می‌شود:

/app/load_raw_data.py
اما در load_raw_data.py اگر DATA_PATH را ../data/raw گذاشته باشی، مسیر به این تبدیل می‌شود:

/app/../data/raw
که می‌شود:

/data/raw
پس باید volume دقیقاً /data را mount کند که تو همین کار را کردی. این قسمت درست است.

اما یک مشکل مهم‌تر وجود دارد
اگر COPY load_raw_data.py . را انجام بدهی، فقط فایل Python داخل image کپی می‌شود، نه پوشه پروژه.

بهترین راه این است که Dockerfile را این‌طور تغییر بده:

FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install pandas sqlalchemy psycopg2-binary

CMD ["python", "load_raw_data.py"]
و از همه مهم‌تر: DATA_PATH
در load_raw_data.py این خط را به این تغییر بده:

DATA_PATH = "/data/raw"
نه:

DATA_PATH = "../data/raw"
چون تو در compose این را داری:

volumes:
  - ./data:/data
پس داخل کانتینر، فایل‌ها دقیقاً اینجا هستند:

/data/raw/olist_orders_dataset.csv
بعد این دستورات را اجرا کن
docker compose down
بعد:

docker compose up --build
بدون -d.

یک نکته دیگر که ممکن است بعد از این خطا بدهد
در load_raw_data.py الان داری:

DATABASE_URL = (
    "postgresql+psycopg2://postgres:postgres@postgres:5432/customer_analytics"
)
این درست است، ولی depends_on فقط ترتیب شروع کانتینرها را تضمین می‌کند، نه اینکه PostgreSQL آماده دریافت اتصال باشد. ممکن است لازم باشد چند ثانیه صبر کنی یا برای loader مکانیزم retry اضافه کنی.

لطفاً یک چیز آخر را هم بگو
داخل پوشه پروژه، این ساختار را داری؟

Project/
│
├── docker-compose.yml
├── data/
│   └── raw/
│       ├── olist_orders_dataset.csv
│       ├── ...
│
└── scripts/
    ├── Dockerfile
    └── load_raw_data.py
یا scripts و data جای دیگری هستند؟

اگر این ساختار را تأیید کنی، مشکل را کامل حل می‌کنیم.


(venv) PS C:\Users\PC\Downloads\Project> cd customer_analytics_dbt
>> 
>> dbt run
>> 
>> 
dbt : The term 'dbt' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was included, verify that the path is correct 
and try again.
At line:3 char:1
+ dbt run
+ ~~~
    + CategoryInfo          : ObjectNotFound: (dbt:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
 

این خطا ربطی به dbt project ندارد؛ مشکل این است که dbt روی ویندوزت نصب نیست.

تو این دستور را زدی:

cd customer_analytics_dbt
dbt run
اما قبلاً دیدیم که dbt فقط داخل کانتینر Airflow نصب شده بود، نه داخل venv ویندوز.

اول بررسی کنیم کانتینرها اصلاً بالا هستند یا نه
این را اجرا کن:

docker ps
اگر customer_airflow را دیدی، واردش شو:

docker exec -it customer_airflow bash
بعد:

cd /opt/customer_analytics_dbt
dbt run
اگر docker ps خالی بود
یعنی اصلاً سرویس‌ها بالا نیستند و باید اول:

docker compose up --build -d
را اجرا کنی.

اگر می‌خواهی dbt run را مستقیماً در PowerShell اجرا کنی
باید dbt را داخل همان virtual environment نصب کنی:

pip install dbt-postgres
ولی برای پروژه تو این کار لازم نیست، چون معماری پروژه طوری طراحی شده که dbt داخل کانتینر Airflow اجرا شود.

لطفاً فقط خروجی این دستور را بفرست:
docker ps
با دیدن آن مشخص می‌شود که مشکل از بالا نیامدن کانتینرهاست یا فقط داری dbt را در جای اشتباه اجرا می‌کنی.


(venv) PS C:\Users\PC\Downloads\Project\customer_analytics_dbt> docker exec -it customer_airflow bash
airflow@453b17dd4030:/opt/airflow$ cd /opt/customer_analytics_dbt
dbt run
17:22:59  Running with dbt=1.12.0-rc2
17:22:59  Registered adapter: postgres=1.10.2
17:23:00  Found 11 models, 13 data tests, 1 source, 475 macros
17:23:00  
17:23:00  Concurrency: 1 threads (target='dev')
17:23:00  
17:23:00  1 of 11 START sql table model public.stg_customers ............................. [RUN]
17:23:00  1 of 11 OK created sql table model public.stg_customers ........................ [SELECT 99441 in 0.51s]
17:23:00  2 of 11 START sql table model public.stg_order_items ........................... [RUN]
17:23:00  2 of 11 OK created sql table model public.stg_order_items ...................... [SELECT 112650 in 0.15s]
17:23:00  3 of 11 START sql table model public.stg_orders ................................ [RUN]
17:23:01  3 of 11 OK created sql table model public.stg_orders ........................... [SELECT 99441 in 0.30s]
17:23:01  4 of 11 START sql table model public.stg_products .............................. [RUN]
17:23:01  4 of 11 OK created sql table model public.stg_products ......................... [SELECT 32951 in 0.08s]
17:23:01  5 of 11 START sql table model public.stg_reviews ............................... [RUN]
17:23:01  5 of 11 OK created sql table model public.stg_reviews .......................... [SELECT 99224 in 0.18s]
17:23:01  6 of 11 START sql table model public_analytics.fact_orders ..................... [RUN]
17:23:01  6 of 11 ERROR creating sql table model public_analytics.fact_orders ............ [ERROR in 0.05s]
17:23:01  7 of 11 START sql table model public_analytics.mart_customer_rfm ............... [RUN]
17:23:01  7 of 11 OK created sql table model public_analytics.mart_customer_rfm .......... [SELECT 75387 in 0.41s]
17:23:01  8 of 11 START sql table model public_analytics.mart_customer_segments .......... [RUN]
17:23:02  8 of 11 OK created sql table model public_analytics.mart_customer_segments ..... [SELECT 98666 in 0.92s]
17:23:02  9 of 11 START sql table model public_analytics.mart_sales_summary .............. [RUN]
17:23:03  9 of 11 OK created sql table model public_analytics.mart_sales_summary ......... [SELECT 1 in 0.55s]
17:23:03  10 of 11 START sql table model public_analytics.mart_product_performance ....... [RUN]
17:23:04  10 of 11 OK created sql table model public_analytics.mart_product_performance .. [SELECT 32951 in 0.91s]
17:23:04  11 of 11 SKIP relation public_analytics.mart_daily_sales ....................... [SKIP]
17:23:04  
17:23:04  Finished running 11 table models in 0 hours 0 minutes and 4.30 seconds (4.30s).
17:23:04  
17:23:04  Completed with 1 error, 0 partial successes, and 0 warnings:
17:23:04  
17:23:04  [ERROR]: in model fact_orders (models/marts/fact_orders.sql)
17:23:04    Database Error in model fact_orders (models/marts/fact_orders.sql)
  column c.customer_state does not exist
  LINE 22:     c.customer_state
               ^
  compiled code at target/run/customer_analytics_dbt/models/marts/fact_orders.sql
17:23:04  

عالی! 🎉 این یعنی تقریباً کل پروژه درست کار می‌کند.

✅ PostgreSQL بالا آمده.

✅ Data Loader داده‌ها را وارد کرده.

✅ dbt اجرا شده.

✅ 10 مدل از 11 مدل با موفقیت ساخته شده‌اند.

فقط یک مدل مشکل دارد:

fact_orders

column c.customer_state does not exist
این دیگر مشکل Docker یا dbt نیست؛ مشکل کد SQL مدل است.

دلیل خطا
در فایل:

customer_analytics_dbt/models/marts/fact_orders.sql
جایی شبیه این وجود دارد:

select
    ...
    c.customer_state
from ...
اما مدل یا جدول stg_customers ستونی به نام customer_state ندارد.

قدم بعدی
لطفاً این دو فایل را بفرست:

customer_analytics_dbt/models/marts/fact_orders.sql
customer_analytics_dbt/models/staging/stg_customers.sql
با دیدن این دو فایل دقیق می‌توانم بگویم:

آیا customer_state باید در stg_customers ساخته شود؟

یا در fact_orders.sql نام ستون اشتباه نوشته شده است.

احتمال زیاد
با توجه به دیتاست Olist، ستون customer_state در فایل olist_customers_dataset.csv وجود دارد. اگر در stg_customers.sql آن را انتخاب نکرده باشی، fact_orders نمی‌تواند از آن استفاده کند.

پس به احتمال زیاد فقط باید stg_customers.sql را اصلاح کنیم، اما برای اینکه دقیق بگوییم، لطفاً آن دو فایل را بفرست.


select

    o.order_id,

    o.customer_id,

    o.order_status,

    o.purchase_date,

    c.customer_state


from {{ ref('stg_orders') }} o

left join {{ ref('stg_customers') }} c

on o.customer_id = c.customer_id


select

    o.order_id,

    o.customer_id,

    c.customer_unique_id,

    o.order_status,

    o.order_purchase_timestamp::timestamp as purchase_date,

    o.order_delivered_customer_date::timestamp as delivery_date


from public.olist_orders_dataset o

left join public.olist_customers_dataset c

on o.customer_id = c.customer_id

مشکل دقیقاً مشخص شد.

در fact_orders.sql داری این را می‌خوانی:

c.customer_state
اما در stg_customers.sql اصلاً ستون customer_state را انتخاب نکرده‌ای.

الان stg_customers.sql فقط این ستون‌ها را می‌سازد:

o.order_id,
o.customer_id,
c.customer_unique_id,
o.order_status,
o.order_purchase_timestamp,
o.order_delivered_customer_date
پس طبیعتاً fact_orders آن ستون را پیدا نمی‌کند.

راه‌حل
فایل:

customer_analytics_dbt/models/staging/stg_customers.sql
را این‌طور تغییر بده:

select

    o.order_id,

    o.customer_id,

    c.customer_unique_id,

    c.customer_state,

    o.order_status,

    o.order_purchase_timestamp::timestamp as purchase_date,

    o.order_delivered_customer_date::timestamp as delivery_date


from public.olist_orders_dataset o

left join public.olist_customers_dataset c

on o.customer_id = c.customer_id
فقط این خط اضافه شد:

c.customer_state,
بعد دوباره داخل کانتینر Airflow:

cd /opt/customer_analytics_dbt
اجرا کن:

dbt run
انتظار داریم این بار:

stg_customers        OK
stg_order_items      OK
stg_orders           OK
stg_products         OK
stg_reviews          OK
fact_orders          OK
mart_customer_rfm    OK
...
همه سبز شوند.

بعد از موفق شدن dbt، مرحله بعدی پروژه‌ات می‌شود:

اجرای تست‌های dbt:

dbt test
آماده کردن Power BI dashboard

اجرای مدل ML churn.


(venv) PS C:\Users\PC\Downloads\Project> uvicorn api.app.main:app --reload
>> 
>> 
uvicorn : The term 'uvicorn' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was included, verify that the path is 
correct and try again.
At line:1 char:1
+ uvicorn api.app.main:app --reload
+ ~~~~~~~
    + CategoryInfo          : ObjectNotFound: (uvicorn:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException

این خطا مثل مشکل dbt قبلی است. یعنی uvicorn داخل venv ویندوز نصب نیست.

تو پروژه‌ات API را داخل Docker داری:

api:
  build:
    context: ./api
پس دو راه داری:

راه ۱ (پیشنهادی): API را با Docker اجرا کن
اول ببین کانتینر API بالا هست:

docker ps
اگر churn_api را دیدی، لاگ بگیر:

docker logs churn_api
اگر بالا نیست:

docker compose up --build -d api
بعد تست کن:

در مرورگر:

http://localhost:8000
یا اگر FastAPI docs داری:

http://localhost:8000/docs
راه ۲: اجرای مستقیم روی ویندوز
اگر می‌خواهی همین دستور README را اجرا کنی:

uvicorn api.app.main:app --reload
باید داخل venv نصبش کنی.

اول برو ریشه پروژه:

cd C:\Users\PC\Downloads\Project
بعد:

pip install -r api/requirements.txt
یا اگر requirements نداری:

pip install fastapi uvicorn
بعد:

uvicorn api.app.main:app --reload
با توجه به معماری پروژه‌ای که ساختی، من راه اول را پیشنهاد می‌کنم چون API و ML هم داخل Docker تعریف شده‌اند.

برای اطمینان، این را بزن و خروجی بده:

docker ps
ببینیم churn_api الان در حال اجرا هست یا نه.


(venv) PS C:\Users\PC\Downloads\Project> docker ps
CONTAINER ID   IMAGE             COMMAND                  CREATED          STATUS          PORTS                                         NAMES
453b17dd4030   project-airflow   "/usr/bin/dumb-init …"   18 minutes ago   Up 18 minutes   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp   customer_airflow
26a242c3d691   postgres:16       "docker-entrypoint.s…"   18 minutes ago   Up 18 minutes   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp   customer_postgres
8ec7ada99afb   project-api       "uvicorn app.main:ap…"   18 minutes ago   Up 18 minutes   0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp   churn_api

عالی، الان همه سرویس‌های اصلی پروژه بالا هستند:

✅ customer_postgres   → PostgreSQL
✅ customer_airflow    → Airflow + dbt
✅ churn_api           → FastAPI
مشکل uvicorn دیگر مهم نیست، چون API داخل Docker در حال اجراست.

الان تست API را انجام بده:

1) در مرورگر باز کن:
http://localhost:8000
یا برای مستندات FastAPI:

http://localhost:8000/docs
باید صفحه Swagger UI باز شود.

2) اگر خواستی لاگ API را ببینی:
docker logs churn_api
باید چیزی شبیه این ببینی:

Uvicorn running on http://0.0.0.0:8000
3) تست کامل پروژه تا اینجا:
ترتیب درست اجرای پروژه تو الان این است:

1. docker compose up -d
        ↓
2. data_loader
        ↓
3. dbt run داخل customer_airflow
        ↓
4. API روی localhost:8000
        ↓
5. Power BI dashboard
        ↓
6. ML churn model
فقط یک مورد را چک کن: چون قبلاً dbt run یک خطای fact_orders داشت، بعد از اصلاح stg_customers دوباره اجرا کن:

docker exec -it customer_airflow bash
داخل:

cd /opt/customer_analytics_dbt
dbt run
باید همه مدل‌ها OK شوند.

بعد از آن API آماده است که از جداول مدل‌شده استفاده کند.


khob in kar mikone 
chejuri tu readme benevisamesh k kasi k mikhad run kone ham bedune tu docker hast 

خوبه. الان چون پروژه‌ات Docker-based شده، README فعلی کمی گمراه‌کننده است؛ چون نوشته:

python -m venv venv
pip install -r requirements.txt
uvicorn api.app.main:app --reload
این برای اجرای مستقیم روی سیستم است، ولی معماری واقعی تو الان این است:

Docker Compose
 ├── PostgreSQL
 ├── Data Loader
 ├── Airflow + dbt
 └── FastAPI
بهتر است بخش How To Run را این‌طور تغییر بده:

How To Run
Prerequisites
Make sure you have installed:

Docker Desktop

Docker Compose

No local Python environment is required because all services run inside Docker containers.

1. Clone Repository
git clone REPOSITORY_URL
cd customer-analytics-platform
2. Dataset Setup
Raw datasets are not included in this repository because of their size.

Download the Brazilian E-Commerce Public Dataset by Olist from Kaggle:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Extract the CSV files into:

data/raw/
Expected structure:

data/
└── raw/
    ├── olist_orders_dataset.csv
    ├── olist_order_items_dataset.csv
    ├── olist_products_dataset.csv
    ├── olist_order_reviews_dataset.csv
    ├── olist_customers_dataset.csv
    ├── olist_sellers_dataset.csv
    ├── olist_geolocation_dataset.csv
    ├── olist_order_payments_dataset.csv
    └── product_category_name_translation.csv
3. Start Docker Services
Build and start all services:

docker compose up --build -d
This starts:

Service	Description
PostgreSQL	Data warehouse database
Data Loader	Loads raw CSV files into PostgreSQL
Airflow	Workflow orchestration and dbt execution
FastAPI	Churn prediction API
4. Load Raw Data
The data loader runs automatically when Docker starts.

Check loading status:

docker logs customer_data_loader
Successful output:

Loading olist_orders_dataset.csv...
Loaded olist_orders_dataset: xxxx rows

Loading olist_products_dataset.csv...
Loaded olist_products_dataset: xxxx rows

Finished loading data
5. Run dbt Transformations
Open the Airflow container:

docker exec -it customer_airflow bash
Go to dbt project:

cd /opt/customer_analytics_dbt
Run transformations:

dbt run
Run data quality tests:

dbt test
6. Access Applications
Airflow
Open:

http://localhost:8080
FastAPI
API:

http://localhost:8000
Swagger documentation:

http://localhost:8000/docs
7. Stop Services
Stop all containers:

docker compose down
Project Execution Flow
CSV Files
    |
    v
Data Loader Container
    |
    v
PostgreSQL
    |
    v
dbt Transformations
    |
    v
Analytics Models
    |
    v
Machine Learning Model
    |
    v
FastAPI Prediction API
All components run inside Docker containers to provide a reproducible environment.

این نسخه برای GitHub خیلی بهتر است، چون هر کسی clone کند فقط Docker لازم دارد و دیگر درگیر نصب Python، dbt، uvicorn و dependencyها نمی‌شود.


hala mikham hame taghirati k dadam tu githubam save beshe 

برای ذخیره کردن همه تغییراتی که دادی روی GitHub، این مراحل را از ریشه پروژه انجام بده.

اول مطمئن شو در مسیر اصلی پروژه هستی:

cd C:\Users\PC\Downloads\Project
1) ببین چه فایل‌هایی تغییر کرده‌اند
git status
باید فایل‌هایی مثل این‌ها را ببینی:

docker-compose.yml

scripts/load_raw_data.py

scripts/Dockerfile

customer_analytics_dbt/models/...

README.md

2) همه تغییرات را اضافه کن
git add .
3) یک commit بساز
مثلاً:

git commit -m "Fix Docker pipeline, data loader, dbt models and update README"
4) تغییرات را به GitHub بفرست
اول ببین branch اسمش چیست:

git branch
اگر دیدی:

* main
بزن:

git push origin main
اگر دیدی:

* master
بزن:

git push origin master
5) چک کن
برو GitHub repository را refresh کن. باید تغییرات را ببینی.

یک نکته مهم قبل از git add .:

چون پروژه‌ات دیتاست Olist دارد، مطمئن شو CSVها را push نکنی. داخل .gitignore این‌ها باید باشند:

data/raw/
*.csv
venv/
__pycache__/
target/
.dbt/
چون دیتاست بزرگ است و نباید داخل GitHub برود.

برای اطمینان اول بزن:

git status
اگر CSVها را نشان داد، قبل از commit باید .gitignore را درست کنیم.



Changes not staged for commit:
  (use "git add/rm <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        deleted:    .flake8
        modified:   customer_analytics_dbt/models/staging/stg_customers.sql
        modified:   docker-compose.yml
        deleted:    scripts/load_raw_data.py

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        ../../.cisco/
        ../../.config/
        ../../.copilot/
        ../../.dbt/
        ../../.docker/
        ../../.env
        ../../.gitconfig
        ../../.ipython/
        ../../.lesshst
        ../../.python_history
        ../../.texlive2023/
        ../../.vscode-shared/
        ../../.vscode/
        ../../AppData/
        ../../Contacts/
        ../../Customer-Analytics-Platform/
        ../(No subject).zip
        ../(Senior) Data Analyst (english).docx.pdf
        ../0a7e0106.zip
        ../1 - Administrative Introduction.pdf
        ../1 - Gradient Descent.pdf
        ../1.pdf
        ../125908881.pdf
        ../138f38ff0b7896ad9b829485b0fc970d.pdf
        ../1bf217a86da43dd357d1347ca84847f2 (1).pdf
        ../1bf217a86da43dd357d1347ca84847f2.pdf
        ../2 - Introduction to Data Science.pdf
        ../2 - Perceptrons.pdf
        ../20240208_10382231_WorkingStudentDataAn_Yazdanian_S_CV.pdf
        ../20250428-1504543297-umsatz.CSV
        ../20251023_104121_ARBEITSBESCHEINIGUNG.pdf
        ../20251027_133754_Bewilligungsbescheid.pdf
        ../20251124_220950_SCHREIBEN.pdf
        ../20260110_013252_SCHREIBEN (1).pdf
        ../20260110_013252_SCHREIBEN.pdf
        ../20260119_072828_Aufhebungsbescheid_und_Entgeltbescheinigung.pdf
        ../20260209_055204_LEISTUNGSNACHWEIS.pdf
        ../20260701-1076529115-umsatz.CSV
        ../20260715_200128_SCHREIBEN.pdf
        ../3 - Multilayer Perceptrons.pdf
        ../365465823df79765201fb4bec9783066.pdf
        ../4 - Deep Neural Networks.pdf
        ../411c63e6dbe03dde0e41ead7914f09b9 (1).pdf
        ../411c63e6dbe03dde0e41ead7914f09b9 (2).pdf
        ../411c63e6dbe03dde0e41ead7914f09b9.pdf
        ../465b69d7fd8c8701fd088817e375bcfb.pdf
        ../5 - Convolutional Neural Networks.pdf
        ../5-17981-65451449 (1).pdf
        ../5-17981-65451449.pdf
        ../5-17981-65651093.pdf
        ../7 - Ensemble Learning.pdf
        ../8 - Bias-Variance Trade-Off.pdf
        ../8aa071dadcdbc398501bb68866cb81b2 (1).pdf
        ../8aa071dadcdbc398501bb68866cb81b2.pdf
        ../AI_and_Applications.html
        ../AI_and_Applications_ (1).html
        ../AI_and_Applications_ (2).html
        ../AI_and_Applications_.html
        ../AI_and_Applications_.ipynb
        ../Acrobat_Set-Up.exe
        ../Antrag - AE (1).pdf
        ../Antrag - AE.pdf
        ../Antrag_Zweitschrift (1).pdf
        ../Antrag_Zweitschrift (2).pdf
        ../Antrag_Zweitschrift (3).pdf
        ../Antrag_Zweitschrift (4).pdf
        ../Antrag_Zweitschrift.pdf
        ../April 2024 M509_AB (1).pdf
        ../April 2024 M509_AB.pdf
        ../Assessment Submission Form_all modules (1).pdf
        ../Ausserordentliche_Kuendigung_Zweitschrift (1).pdf
        ../Ausserordentliche_Kuendigung_Zweitschrift.pdf
        ../AusweisApp-2.3.2.msi
        "../Basisdienst Digitaler Antrag_Verpflichtungserkl\303\244rung abgeben_2024-04-25.html"
        ../BlueStacks10Installer_10.42.168.1001_native_2d725b3f83167c4ca606bf23ee5be90e_MzsxNSwwOzUsMTsxNSw0OzE1LDU7MTU=_2KLZhdmI2LLYtCBydWJpa2E=.exe
        "../Bonit\303\244tsCheck_g\303\274ltig_bis_27.12.2024 (1).pdf"
        "../Bonit\303\244tsCheck_g\303\274ltig_bis_27.12.2024.pdf"
        ../CV.pdf
        ../CV_Shokoufeh_Yazdanian (3).pdf
        ../Challenge.ipynb
        ../Challenge_annotated.ipynb
        ../ChromeSetup (1).exe
        ../ChromeSetup.exe
        ../Contact_Center_Forecasting_Candidate_Exercise Template.xlsx
        ../Contract_Yazdanian.pdf
        ../Copy_of_(orginal)_project_1,ipynb (1).ipynb
        ../Copy_of_(orginal)_project_1,ipynb.ipynb
        ../Copy_of_support_vector_machines.ipynb
        ../Cover Letter Shokoufeh Yazdanian.pdf
        ../Cover Letter..pdf
        ../Cover Letter.pdf
        ../Customer-Analytics-Platform-main.zip
        ../Customer-Analytics-Platform.zip
        ../De-Stu-68SHOKOUFEH-M09D13-1P-Pr.txt
        ../Dexter.S01E01.480p.Farsi.Subbed.mkv
        ../Dexter.S01E02.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S01E02.480p.Farsi.Subbed.mkv
        ../Dexter.S01E03.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S01E03.480p.Farsi.Subbed.mkv
        ../Dexter.S01E04.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S01E05.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S01E06.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S01E07.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S01E08.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S01E09.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S01E10.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S01E11.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S01E12.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S02E01.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S02E02.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S02E03.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S02E04.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S02E05.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S02E06.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S02E07.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S02E08.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S02E09.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S02E10.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S02E11.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S02E12.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S03E01.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S03E02.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S03E03.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S03E04.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S03E05.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S03E06.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S03E07.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S03E08.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S03E09.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S03E10.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S03E11.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S03E12.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S04E01.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../Dexter.S04E02.480p.BluRay.SoftSub.Pahe.DonyayeSerial.mkv
        ../DiamondPrice (1).html
        ../DiamondPrice (2).html
        ../DiamondPrice (3).html
        ../DiamondPrice (4).html
        ../DiamondPrice.html
        ../Digital Marketing assignment.pdf
        ../Digital Marketing.pdf
        ../Docker Desktop Installer.exe
        ../Document 1.pdf
        ../EN_Office_2021_Professional_Plus_64Bit_v.exe
        ../EN_Office_2021_Professional_Plus_64Bit_v/
        ../EN_Windows_11_Home_Pro_23H2_v2_x64.iso
        ../Extension of Enrolment deadline letter_GH1026726_Shokoufeh Yazdanian Khormandichali.pdf
        ../Extra German 1 Video [www.kardOOnline.com].rar
        ../Extra German 2 Video [www.kardOOnline.com].rar
        ../Footloose.2011.720p.BluRay.mkv
        ../Forderungsaufstellung_60813371A.pdf
        ../GH1026726 Admission Pack October 2023qr (1).pdf
        ../GH1026726 Admission Pack October 2023qr.pdf
        ../GH1026726 GISMA Admissions Pack, July 2023qr.pdf
        ../GH1026726_GISMA_Admissions_Pack,_January_2024_qr.pdf
        ../GH1026726_Payment_Demand__Payment_Plan,_January_2024.pdf
        ../GH1026726_Payment_Demand__Payment_Plan,_January_2024.zip
        ../GISMA UAS VCR guide_September 2023.pdf
        ../GISMA UAS_Extenuating Circumstances Form - Copy.docx
        ../GermanCV.pdf
        ../Gisma Payment Modes.pdf
        ../Gisma VCR Guide_2024.pdf
        ../Git-2.55.0.2-64-bit.exe
        "../Gmail - Fwd_ lastminute_.de Buchung f\303\274r Hotel Ascot-Bristol, Potsdam.pdf"
        ../Green And White Illustrative Marketing Plan Presentation.pdf
        ../Health insurance.pdf
        ../Health.pdf
        ../Hurdle 1.py
        ../IMG_20220515_200745_11zon.jpg
        ../IMG_20231003_151531.jpg
        ../IMG_20231003_151531.png
        ../IMG_20231003_151600.jpg
        ../IMG_20231114_150321.jpg
        ../IMG_20231114_150324.jpg
        ../IMG_20231207_105220.jpg
        ../IMG_5320 (1).pdf
        ../IMG_5320.pdf
        ../IMG_5322.jpg
        ../IMG_5323 (1).jpg
        ../IMG_5323 (2).jpg
        ../IMG_5323.jpg
        ../IMG_6917.pdf
        ../Illichmann_Abdulai_AAEA 2013.pdf
        ../Internet.Download.Manager.6.41.Build.15.Retail.zip
        ../KMPlayer_4.2.3.21.exe
        ../Kandidatenfragebogen_Auskunft_zu_Vorbeschaeftigungen_EN (1).pdf
        ../Kandidatenfragebogen_Auskunft_zu_Vorbeschaeftigungen_EN.docx
        ../Kandidatenfragebogen_Auskunft_zu_Vorbeschaeftigungen_EN.pdf
        ../Konto_1504543297-Auszug_2024_0004.PDF
        ../Konto_1504543297-Auszug_2024_0005.PDF
        ../Konto_1504543297-Auszug_2024_0006.PDF
        ../Konto_1504543297-Auszug_2024_0007.PDF
        ../Konto_1504543297-Auszug_2024_0008.PDF
        ../Konto_1504543297-Auszug_2024_0009.PDF
        ../Konto_1504543297-Auszug_2024_0010.PDF
        ../Kopie von Case Study - Workforece Management.xlsx
        ../Kursliste.pdf
        ../Lebenslauf von shokoufeh yazdanian.pdf
        ../Leg-276SHOKOUFEH-M07D25-1P-Pr.txt
        ../LibreOffice.v24.2.4.x64_p30download.com.msi
        ../M504 Assessment Brief (2) (1).pdf
        ../M504 Assessment Brief (2).pdf
        ../M505 Assessment Brief (4).pdf
        ../M506_Assessment-brief-2024.docx
        ../M507 Assessment Brief (1).pdf
        ../M507 Assessment Brief (2).pdf
        ../M507 Assessment Brief.pdf
        ../M507_Methods_of_Prediction_assignment (1).ipynb
        ../M507_Methods_of_Prediction_assignment.html
        ../M507_Methods_of_Prediction_assignment.ipynb
        ../M508 Assessment Brief (1).pdf
        ../M508 Assessment Brief (2).pdf
        ../M508 Assessment Brief (3).pdf
        ../M508 Assessment Brief.pdf
        ../M508_Final_Assessment (1).html
        ../M508_Final_Assessment (1).ipynb
        ../M508_Final_Assessment (2).ipynb
        ../M508_Final_Assessment.html
        ../M508_Final_Assessment.ipynb
        ../M508_Final_Assignment.html
        ../M508_Final_Assignment.ipynb
        ../Machine_Learning_Course_Assignment (1).ipynb
        ../Machine_Learning_Course_Assignment (2).ipynb
        ../Machine_Learning_Course_Assignment Shokoufeh Yazdanian.html
        ../Machine_Learning_Course_Assignment Shokoufeh Yazdanian.ipynb
        ../Machine_Learning_Course_Assignment.ipynb
        ../Machine_Learning_Course_Assignment_Shokoufeh_Yazdanian (1).html
        ../Machine_Learning_Course_Assignment_Shokoufeh_Yazdanian (2).html
        ../Machine_Learning_Course_Assignment_Shokoufeh_Yazdanian.html
        ../Mitgliedschaftvereinbarung Bestseller (1).pdf
        ../Mitgliedschaftvereinbarung Bestseller (2).pdf
        ../Mitgliedschaftvereinbarung Bestseller.pdf
        ../Munich_CV_Shokoufeh_Yazdanian.docx
        ../New-Rich-Text-Document-1.rtf
        ../OneLaunch - Manuals Search_nvywc.exe
        ../One_Flew_Over_The_Cuckoos_Nest_1975_Hardsub.mp4
        ../PBIDesktopSetup_x64.exe
        ../PDFAnnotatorSetup.exe
        ../Passport (1).jpg
        ../Passport.jpg
        ../Payment issue.eml
        ../Payment modes at GISMA Potsdam (2).pdf
        ../Peaky.Blinders.S01E01.720p.BluRay.HardSub.Zardfilm.Net.mp4
        ../Pejman_10_(Doostiha.NET).mp4
        ../Phone Number Price Prediction (1).html
        ../Phone Number Price Prediction (2).html
        ../Phone Number Price Prediction.html
        ../Power BI Exercise Files.zip
        data/raw/
        data_loader/
        ../Receipt.pdf
        ../Referral Bonus form (1).pdf
        ../Referral Bonus form.pdf
        ../Referral bonus.eml
        ../Referral-Bonus form (1).pdf
        ../Referral-Bonus form.pdf
        ../Research Methods.pdf
        ../SIGNED_CONTRACT_693a9d4c89a050f9d045730f_20260110.pdf
        ../Sales and Leads report (1).html
        ../Sales and Leads report.html
        ../Scan_2024-10-15_10-36-57-622.pdf
        ../Screenshot 2024-01-31 142246.jpg
        "../Selbsterkl\303\244rung Verl\303\244ngerung AT_Declaration renewal residence permit (1).pdf"
        "../Selbsterkl\303\244rung Verl\303\244ngerung AT_Declaration renewal residence permit (2).pdf"
        "../Selbsterkl\303\244rung Verl\303\244ngerung AT_Declaration renewal residence permit.pdf"
        ../Shokoufeh Yazdanian (1).pdf
        ../Shokoufeh Yazdanian Khormandichali (1) (1).pdf
        ../Shokoufeh Yazdanian Khormandichali (1).pdf
        ../Shokoufeh Yazdanian Khormandichali (2).pdf
        ../Shokoufeh Yazdanian Khormandichali.pdf
        ../Shokoufeh Yazdanian.pdf
        ../Shokoufeh yazdanian CV.pdf
        ../Shokoufeh-Yazdanian-1699733010157-Psychometric.pdf
        ../Shokoufeh_Yazdanian_CV (1).pdf
        ../Shokoufeh_Yazdanian_CV.pdf
        ../Shokoufeh_Yazdanian_Optimized_CV.pdf
        ../Shokoufeh_Yazdanian_s_CV (1).docx
        ../Shokoufeh_Yazdanian_s_CV.pdf
        ../Shokoufeh_yazdanian's_CV (1).pdf
        ../Shokoufeh_yazdanian's_CV.pdf
        ../Shooufeh Yazdanian's CV.pdf
        ../Stellungnahme_Verspaetet_ASU_Zweitschrift.pdf
        ../Study at Gisma_ Your Pathway to Success.ics
        ../Telegram Desktop/
        ../Thank you for your enquiry - MSc Data Science, AI, and Digital Business.eml
        ../The Matrix Reloaded.srt
        ../The.Big.Bang.Theory.Deutschweb.S01E01.avi
        ../The.Office.S02E03.480p.WEB-DL.SoftSub.DonyayeSerial.mkv
        ../The.Office.S02E04.480p.WEB-DL.SoftSub.DonyayeSerial.mkv
        ../The.Office.S02E05.480p.WEB-DL.SoftSub.DonyayeSerial.mkv
        ../The.Office.S02E06.480p.WEB-DL.SoftSub.DonyayeSerial.mkv
        ../The.Office.S02E07.480p.WEB-DL.SoftSub.DonyayeSerial.mkv
        ../The.Office.S02E09.480p.WEB-DL.SoftSub.DonyayeSerial.mkv
        ../The.Office.S02E12.480p.WEB-DL.SoftSub.DonyayeSerial.mkv
        ../The_Matrix_Reloaded_HD720.mp4
        ../True.Detective.S01E01.720p.BluRay.x265.SoftSub.DonyayeSerial.mkv
        ../True.Detective.S01E02.720p.BluRay.x265.SoftSub.DonyayeSerial.mkv
        ../True.Detective.S01E03.720p.BluRay.x265.SoftSub.DonyayeSerial.mkv
        ../Tweets.csv.zip
        ../Unbekannt (1).pdf
        ../Unbekannt.pdf
        ../Unconfirmed 465576.crdownload
        ../VISA.pdf
        ../VLC.Media.Player.3.0.18.x64.zip
        ../VSCodeUserSetup-x64-1.127.0.exe
        ../Visumantrag_YAZDANIAN KHORMANDICHALI_20230917-1720.json
        ../Visumantrag_YAZDANIAN KHORMANDICHALI_20230917-1734.json
        ../Visumantrag_YAZDANIAN KHORMANDICHALI_20230917-1818.json
        ../WhatsApp Image 2024-10-11 at 18.12.17.jpeg
        ../WhatsApp Installer (1).exe
        ../WhatsApp Installer.exe
        ../Yazdanian Khormandichali Shokoufeh_Dienstvertrag ab 15.01.2026.pdf
        ../Yazdanian,Shokoufe Rg.Nr. B000001798 (2).pdf
        ../Yazdanian,Shokoufe Rg.Nr. B000001886 (1).pdf
        ../Zahra_Hassan (1).ipynb
        ../Zahra_Hassan.html
        ../Zahra_Hassan.ipynb
        ../Zoom_cm_fo42lnktZ9vvrZo4_m-iggJJqlydZS5-JU1C5xEXHTdPKJm2xAzkKR@CzUTKLXEMTREIEbf_kdc0ca8663f40ed4b_.exe
        "../_Versicherungsbest\303\244tigung (1).PDF"
        "../_Versicherungsbest\303\244tigung (2).PDF"
        "../_Versicherungsbest\303\244tigung.PDF"
        ../anmeldung.pdf
        ../antrag-aufenthaltstitel-deutsch-engl-frz-ital (1) (1).pdf
        ../antrag-aufenthaltstitel-deutsch-engl-frz-ital (1).docx
        ../antrag-aufenthaltstitel-deutsch-engl-frz-ital (1).pdf
        ../anyconnect-win-4.9.00086-core_MiniRoid.com.msi
        ../archive (1).zip
        ../archive (10).zip
        ../archive (11).zip
        ../archive (12).zip
        ../archive (13).zip
        ../archive (14).zip
        ../archive (15).zip
        ../archive (16).zip
        ../archive (2).zip
        ../archive (3).zip
        ../archive (4).zip
        ../archive (5).zip
        ../archive (6).zip
        ../archive (7).zip
        ../archive (8).zip
        ../archive (9).zip
        ../archive.zip
        ../ax (1).jpg
        ../ax.jpg
        ../bundle.zip
        ../c8dbc4fa014aaa0ab7fc07040ea44f20.jpg
        ../code_v2025-10-27.zip
        ../compressjpeg (1).zip
        ../compressjpeg.zip
        ../compressjpeg/
        ../contract.pdf
        ../cv_yaz.docx
        ../cv_yaz.pdf
        ../db3d2e848390206b0bcb9851a281fc31 (1).pdf
        ../db3d2e848390206b0bcb9851a281fc31 (2).pdf
        ../db3d2e848390206b0bcb9851a281fc31.pdf
        ../degree.pdf
        ../desktop.ini
        ../downloadgram.org_AQNoNzuCvQ5SIj36f_qnxI__2YyDUkSDO5kaQ7K2Q0VaoUdMMO0fUA4bs-t0NZAnZ3VUpTkvCOIH1AIswjv1PmNduKZwZIPP_mMW3Q0.mp4
        ../downloadgram.org_AQPllfxlCClhOKJMyXP9DE1YWmd5lir7hPRv7R24HyX8KyU56_xrWqu3MH2QwPBEWCRHKp9cpEfwe2vtjZ0WBSNL.mp4
        ../evidence (1).pdf
        ../evidence.pdf
        ../fa28ccae0d13b47b4aaa263b920ec56c.pdf
        ../harry_potter.txt
        ../install-tl-windows.exe
        ../jre-8u491-windows-i586-iftw.exe
        ../labo-4030-antrag-ve-08-19.pdf
        ../labo-4384-zusatzerklaerung-zur-ve-09-19 (1).pdf
        ../labo-4384-zusatzerklaerung-zur-ve-09-19.pdf
        ../login.htm
        ../mdb-f403192-pr__fungsbericht_ve.docx
        ../mini reseach paper (1).docx
        ../mini reseach paper (1).pdf
        ../mini reseach paper (2).docx
        ../mini reseach paper.docx
        ../mini reseach paper.pdf
        ../new_CV (1).pdf
        ../new_CV.pdf
        ../olist_customers_dataset.csv
        ../olist_geolocation_dataset.csv
        ../olist_order_items_dataset.csv
        ../olist_order_payments_dataset.csv
        ../olist_order_reviews_dataset.csv
        ../olist_orders_dataset.csv
        ../olist_products_dataset.csv
        ../olist_sellers_dataset.csv
        ../passport.pdf
        ../photo_2023-02-28_14-55-13.jpg
        ../photo_2024-04-25_14-23-27 (1).jpg
        ../photo_2024-04-25_14-23-30 (1).jpg
        ../photo_2025-07-24_12-45-51.jpg
        ../photo_2025-12-19_14-00-47.jpg
        ../png2jpg.zip
        ../postgresql-18.4-2-windows-x64.exe
        ../product_category_name_translation.csv
        ../profile pic.jpg
        ../receipt_AI_and_Applications_.html.pdf
        ../receipt_M507_Methods_of_Prediction_assignment.html.pdf
        ../refund.docx
        ../refund.pdf
        ../report.pdf
        ../scanner_20231101_125343.jpg
        ../scholar.enw
        ../sejel-min (1).jpg
        ../sejel-min.jpg
        ../sejel_11zon.jpg
        ../sejel_11zon_11zon (1).jpg
        ../sejel_11zon_11zon.jpg
        ../sp06in01.pdf
        ../standard_cv.docx
        ../start.bat
        ../tchareerak2,+Journal+editor,+14.pdf
        ../thumbnail_image.png
        ../ticket_sales_analysis.ipynb
        ../tsetup-x64.4.9.8 (1).exe
        ../tsetup-x64.4.9.8.exe
        ../user_JfU7rqA6UJVqtcldCVZ2mVxICPS6cHyBNWtNfN9r.ics
        ../vertopal.com_Machine_Learning_Course_Assignment.zip
        ../videx.pdf
        ../visa.jpg
        ../y2mate.is - Hey one in a Million love cat Cute kitten hugs puppy shorts pets cats puppy dog-lIUUtcjKc-s-1080pp-1701974498.mp4
        ../y2mate.is - So Cute Cat Funny Video-AJa1lT1KyxQ-480pp-1701974203.mp4
        ../../Favorites/
        ../../IntelGraphicsProfiles/
        ../../Links/
        ../../Microsoft/
        ../../NTUSER.DAT
        ../../NTUSER.DAT{a47803dc-4466-11f0-b808-b957bd9686f3}.TM.blf
        ../../NTUSER.DAT{a47803dc-4466-11f0-b808-b957bd9686f3}.TMContainer00000000000000000001.regtrans-ms
        ../../NTUSER.DAT{a47803dc-4466-11f0-b808-b957bd9686f3}.TMContainer00000000000000000002.regtrans-ms
        ../../OneDrive/
        ../../Saved Games/
        ../../Searches/
        ../../edb_asp_bluefin_pg18.exe
        ../../edb_mtk.exe
        ../../edb_pem_agent.exe
        ../../edb_pem_server.exe
        ../../edb_pgagent_pg18.exe
        ../../edb_pgbouncer.exe
        ../../edb_psqlodbc.exe
        ../../edb_xdb_7.exe
        ../../ntuser.dat.LOG1
        ../../ntuser.dat.LOG2
        ../../ntuser.ini
        ../../pemhttpd.exe
        ../../postgis_3_6_pg18.exe
        ../../postgresql_18.exe
        ../../requirements.txt
        ../../untitled-1.log
        ../../untitled-1.tex

no changes added to commit (use "git add" and/or "git commit -a")

مشکل اینجاست که داخل پوشه درست Git repository نیستی یا داری از یک مسیر بالاتر git status می‌گیری.

از خروجی مشخص است:

Untracked files:
../../.cisco/
../../.config/
../../AppData/
...
یعنی Git فکر می‌کند کل C:\Users\PC را داری track می‌کنی، نه فقط پروژه.

احتمالاً قبلاً اشتباهی در C:\Users\PC دستور:

git init
زدی.

1) اول ببین الان Git کدام repo را پیدا کرده
در همین PowerShell بزن:

git rev-parse --show-toplevel
احتمالاً چیزی شبیه این می‌دهد:

C:/Users/PC
که اشتباه است.

باید چیزی مثل این باشد:

C:/Users/PC/Downloads/Project
2) برو داخل پروژه و چک کن
cd C:\Users\PC\Downloads\Project
بعد:

git rev-parse --show-toplevel
اگر باز هم C:/Users/PC داد
باید Git اشتباه را پاک کنیم.

برو:

cd C:\Users\PC
و این پوشه مخفی را پاک کن:

Remove-Item -Recurse -Force .git
⚠️ فقط وقتی مطمئن شدی که این .git مربوط به Home folder است، نه پروژه.

3) حالا داخل پروژه Git را درست کن
cd C:\Users\PC\Downloads\Project
بعد:

git init
4) Remote GitHub را دوباره وصل کن
اول:

git remote -v
اگر چیزی نبود:

git remote add origin YOUR_GITHUB_REPO_URL
5) .gitignore بساز
داخل Project یک فایل .gitignore داشته باش:

data/raw/
*.csv
venv/
__pycache__/
.dbt/
target/
.env
6) حالا commit کن
git add .
چک:

git status
باید فقط فایل‌های پروژه را ببینی، مثل:

modified: docker-compose.yml
modified: README.md
modified: customer_analytics_dbt/models/staging/stg_customers.sql
new file: data_loader/...
بعد:

git commit -m "Update Docker pipeline, dbt models and documentation"
و:

git push origin main
اول فقط خروجی این دستور را بفرست:

git rev-parse --show-toplevel
تا مطمئن شویم repo اشتباه نیست.


# Python
__pycache__/
*.pyc

# Virtual environment
venv/
.env

# Jupyter
.ipynb_checkpoints/

data/raw/*
!data/raw/.gitkeep

data/processed/*
!data/processed/.gitkeep

# OS
.DS_Store

# dbt generated files
customer_analytics_dbt/target/
customer_analytics_dbt/logs/
customer_analytics_dbt/dbt_packages/

# dbt local profile
customer_analytics_dbt/profiles.yml

# Logs
logs/
airflow/logs/

# MLflow
mlruns/
mlflow.db

# Large model files
*.pkl
*.skops

# Python cache
__pycache__/
.pytest_cache/

مشکل اصلی اینجاست که الان داخل Project نیستی یا Git root اشتباه تنظیم شده. از خروجی git status مشخصه Git دارد فایل‌های کل C:\Users\PC را می‌بیند (../../AppData, ../../.vscode و ...). یعنی احتمالاً قبلاً git init را جای اشتباه زده‌ای.

اول این را چک کن:

git rev-parse --show-toplevel
باید چیزی شبیه این بدهد:

C:/Users/PC/Downloads/Project
اگر چیز دیگری داد (مثلاً C:/Users/PC) یعنی Git اشتباه ساخته شده.

1) حذف Git اشتباه
برو به جایی که اشتباه init شده:

cd C:\Users\PC
بعد:

Remove-Item -Recurse -Force .git
(این فقط تاریخچه Git را حذف می‌کند، فایل‌هایت پاک نمی‌شوند.)

2) دوباره Git را برای پروژه بساز
برگرد:

cd C:\Users\PC\Downloads\Project
بعد:

git init
3) .gitignore را درست کن
فایلی که فرستادی خوبه، فقط این خط را تغییر بده:

الان:

data/raw/*
!data/raw/.gitkeep
درسته، یعنی CSVها commit نمی‌شوند.

برای اینکه پوشه بماند:

ساختار:

data
 └── raw
     └── .gitkeep
بساز:

New-Item data/raw/.gitkeep -ItemType File
4) فایل‌های پروژه را اضافه کن
حالا:

git add .
چک کن:

git status
باید فقط چیزهای پروژه را ببینی:

مثلاً:

docker-compose.yml
Dockerfile
api/
scripts/
customer_analytics_dbt/
README.md
نباید ببینی:

AppData
.vscode
Documents
PDF
5) Commit
git commit -m "Add dockerized customer analytics platform"
6) وصل کردن به GitHub
اگر repository را در GitHub ساخته‌ای:

git remote add origin YOUR_GITHUB_URL
مثلاً:

git remote add origin https://github.com/username/customer-analytics-platform.git
بعد:

git branch -M main
git push -u origin main
یک نکته مهم:
data/raw را عمداً push نکن. CSVهای Olist بزرگ هستند و بهتر است کسی که clone می‌کند طبق README دانلود کند و بعد:

docker compose up -d
اجرا کند.

برای README هم بهتر است این flow را بنویسی:

1. Clone repository

2. Put dataset files inside:
data/raw/

3. Run:
docker compose up -d

4. Load raw data:
docker compose run data_loader

5. Run dbt:
docker exec -it customer_airflow bash
cd /opt/customer_analytics_dbt
dbt run

6. Access:
Airflow:
http://localhost:8080

API:
http://localhost:8000
الان اول فقط git rev-parse --show-toplevel را بزن ببین root درست است یا نه.


 git rev-parse --show-toplevel
C:/Users/PC/Downloads/Project

عالیه. الان Git درست روی پروژه تنظیم شده و مشکل قبلی (دیدن کل C:\Users\PC) حل شده. ✅

حالا این مراحل را انجام بده:

1) اول وضعیت را دوباره ببین
git status
دیگه نباید چیزهایی مثل:

../../AppData
../../.vscode
../../Documents
ببینی.

2) فایل‌های پروژه را اضافه کن
git add .
بعد:

git status
ببین چه چیزهایی قرار است commit شوند.

احتمالاً باید چیزهایی شبیه این ببینی:

modified: docker-compose.yml
modified: customer_analytics_dbt/models/staging/stg_customers.sql
new file: README.md
new file: scripts/load_raw_data.py
...
3) اگر load_raw_data.py به اشتباه حذف شده
قبلاً داشتی:

deleted: scripts/load_raw_data.py
ولی الان چون دوباره ساختی ممکن است برگردد.

چک کن:

dir scripts
باید ببینی:

load_raw_data.py
Dockerfile
اگر نیست، از Git برگردان:

git restore scripts/load_raw_data.py
4) Commit بزن
git commit -m "Add dockerized customer analytics pipeline"
5) وصل به GitHub
اول ببین remote داری یا نه:

git remote -v
اگر چیزی نشان نداد:

git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
بعد:

git branch -M main
git push -u origin main
یک نکته: چون .gitignore داری:

data/raw/*
!data/raw/.gitkeep
CSVها push نمی‌شوند. این خوب است.

قبل از commit اگر خواستی مطمئن شوی هیچ فایل حساس یا بزرگ نمی‌رود:

git status --short
خروجی را بفرست اگر چیزی عجیب دیدی.


>> C:/Users/PC/Downloads/Project
C:/Users/PC/Downloads/Project
C:/Users/PC/Downloads/Project : The term 'C:/Users/PC/Downloads/Project' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a 
path was included, verify that the path is correct and try again.
At line:2 char:1
+ C:/Users/PC/Downloads/Project
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : ObjectNotFound: (C:/Users/PC/Downloads/Project:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException
 

این خطا مشکلی نیست. فقط اشتباه این اتفاق افتاده:

وقتی این دستور را زدی:

git rev-parse --show-toplevel
خروجی‌اش این بود:

C:/Users/PC/Downloads/Project
این دستور نبود، فقط آدرس پوشه‌ای بود که Git نشان داد. تو دوباره همان آدرس را در PowerShell اجرا کردی، برای همین گفت:

The term 'C:/Users/PC/Downloads/Project' is not recognized
الان Git درست است. ادامه بده:

git status
بعد:

git add .
بعد دوباره:

git status
خروجی دوم را بفرست تا ببینیم چه چیزهایی آماده commit شده.


(venv) PS C:\Users\PC\Downloads\Project> git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .env.txt
        .github/
        .gitignore
        Dockerfile
        README.md
        airflow/
        analysis/
        api/
        connect_postgres.py
        create_expectations.py
        create_suite.py
        customer_analytics_dbt/
        dashboard/
        data/
        data_loader/
        docker-compose.yml
        docs/
        great expectations/
        init_gx.py
        ml/
        notebooks/
        pytest.ini
        requirements.txt
        sql/
        src/
        tests/
        "tructure\357\200\242"
        validate_data.py

nothing added to commit but untracked files present (use "git add" to track)

عالیه، الان وضعیت درست است. ✅
Git فقط فایل‌های خود پروژه را می‌بیند و دیگر فایل‌های شخصی (AppData, PDFها و...) داخلش نیستند.

یک نکته: این فایل عجیب را می‌بینم:

"tructure\357\200\242"
احتمالاً یک فایل اشتباهی با اسم خراب ساخته شده. قبل از git add بهتر است حذفش کنیم.

در PowerShell بزن:

Remove-Item -LiteralPath "tructure\357\200\242"
اگر گفت فایل پیدا نشد، مهم نیست.

بعد:

git add .
حالا چک کن:

git status
باید فایل‌ها به صورت:

new file:
    README.md
    docker-compose.yml
    api/...
    airflow/...
نمایش داده شوند.

بعد commit:

git commit -m "Initial commit - Dockerized customer analytics platform"
بعد برای GitHub:

اول چک کن remote داری یا نه:

git remote -v
اگر خالی بود:

git remote add origin https://github.com/USERNAME/REPOSITORY.git
بعد:

git branch -M main
git push -u origin main
یک نکته قبل از git add .:
چون پروژه‌ات ML + Docker + Airflow + dbt است، بهتر است مطمئن شویم این‌ها commit نمی‌شوند:

data/raw/*.csv ✅

venv/ ✅

customer_analytics_dbt/target/ ✅

logs/ ✅

.env واقعی ✅

ولی این فایل را دیدم:

.env.txt
این را چک کن که داخلش پسورد یا secret نباشد. اگر دارد، بهتر است قبل از commit حذفش کنیم یا داخل .gitignore بگذاریم.

اول git add . نزن تا .env.txt را چک کنی. بزن:

type .env.txt
و ببین داخلش چی هست.


POSTGRES_HOST=localhost
POSTGRES_PORT=5433
POSTGRES_DB=customer_analytics
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

این فایل .env.txt فقط تنظیمات PostgreSQL دارد و پسورد واقعی حساس ندارد (چون اینجا پسورد لو رفته نیست و مقدار postgres برای پروژه Docker معمولی است)، ولی بهتر است فایل‌های محیطی را معمولاً داخل Git نگذاریم.

بهتر است:

1) اسمش را از .env.txt به .env.example تغییر بده
در PowerShell:

Rename-Item .env.txt .env.example
بعد داخل .env.example نگهش دار:

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=customer_analytics
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
(توجه: در Docker تو پورت داخلی PostgreSQL 5432 است، نه 5433.)

2) .env واقعی را ignore کن
در .gitignore این خط را اضافه کن:

.env
بعد اگر کسی پروژه را clone کرد:

.env.example  →  .env
کپی می‌کند.

3) حالا Git را آماده کن
بزن:

git add .
بعد:

git status
اگر دیدی:

.env.example
آمد ولی:

.env
نیامد، درست است.

بعد:

git commit -m "Initial commit - Dockerized customer analytics platform"
و بعد push به GitHub.


Data Source

Python ETL

PostgreSQL

Great Expectations

dbt Warehouse

Power BI Dashboard

ML Pipeline

FastAPI

workflow projam chi hala ? vase diagram readme

برای README بهتره workflow پروژه‌ات را این‌طوری نشان بدهی. با توجه به چیزی که ساختی، ترتیب درست pipeline این است:

                ┌─────────────────────┐
                │     Data Source      │
                │  Olist CSV Dataset   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │    Python ETL       │
                │  load_raw_data.py   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │     PostgreSQL      │
                │    Raw Tables       │
                └──────────┬──────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
┌─────────────────────┐       ┌─────────────────────┐
│ Great Expectations  │       │        dbt          │
│ Data Validation     │       │ Transformations     │
└─────────────────────┘       └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │  Analytics Warehouse │
                              │ Staging + Marts      │
                              └──────────┬──────────┘
                                         │
                    ┌────────────────────┴──────────────────┐
                    ▼                                       ▼
          ┌───────────────────┐                 ┌───────────────────┐
          │  Power BI Dashboard│                 │   ML Pipeline     │
          │ Business Analytics│                 │ Customer Churn    │
          └───────────────────┘                 └─────────┬─────────┘
                                                          │
                                                          ▼
                                               ┌───────────────────┐
                                               │      FastAPI      │
                                               │ ML Prediction API │
                                               └───────────────────┘
برای README می‌توانی این بخش را اضافه کنی:

## Data Pipeline Architecture

The project implements an end-to-end customer analytics platform:

1. **Data Source**
   - Olist e-commerce dataset (CSV files)

2. **Python ETL**
   - Loads raw CSV files
   - Creates PostgreSQL raw tables

3. **PostgreSQL Database**
   - Stores raw data
   - Acts as the central data layer

4. **Great Expectations**
   - Performs data quality checks
   - Validates schema and data integrity

5. **dbt Warehouse Layer**
   - Creates staging models
   - Builds analytical marts:
     - Customer RFM analysis
     - Customer segmentation
     - Sales analytics
     - Product performance

6. **Analytics & ML**
   - Power BI dashboard for business insights
   - ML pipeline for churn prediction

7. **FastAPI**
   - Serves trained ML models through REST API
برای GitHub README حتی بهتر است Mermaid diagram استفاده کنی چون خودش render می‌شود:

flowchart TD

A[Data Source<br/>Olist CSV] --> B[Python ETL<br/>load_raw_data.py]

B --> C[PostgreSQL<br/>Raw Tables]

C --> D[Great Expectations<br/>Data Validation]

C --> E[dbt Warehouse<br/>Staging + Marts]

E --> F[Power BI Dashboard]

E --> G[ML Pipeline<br/>Churn Prediction]

G --> H[FastAPI<br/>Prediction API]
این نسخه برای README حرفه‌ای‌تر است چون GitHub خودش diagram را نمایش می‌دهد.


marmaid ro daghigh bezar copy konam

این را دقیقاً کپی کن داخل README.md:

## Project Workflow Architecture

```mermaid
flowchart TD

    A[Data Source<br/>Olist E-commerce CSV Files] --> B[Python ETL<br/>load_raw_data.py]

    B --> C[PostgreSQL<br/>Raw Data Layer]

    C --> D[Great Expectations<br/>Data Quality Validation]

    C --> E[dbt Warehouse<br/>Staging Models + Analytics Marts]

    E --> F[Power BI Dashboard<br/>Business Analytics]

    E --> G[ML Pipeline<br/>Customer Churn Prediction]

    G --> H[FastAPI<br/>ML Prediction API]
```
نتیجه در GitHub این شکلی نمایش داده می‌شود:

Data Source
     |
     v
Python ETL
     |
     v
PostgreSQL
   /    \
  v      v
Great    dbt Warehouse
Expect.      |
             |
      ----------------
      |              |
      v              v
 Power BI       ML Pipeline
                    |
                    v
                FastAPI
این diagram دقیقاً با architecture فعلی پروژه‌ات match است:

scripts/load_raw_data.py → Python ETL

customer_postgres → PostgreSQL

Great Expectations → validation

customer_analytics_dbt → warehouse layer

Power BI → dashboard

ml/ → churn model

api/ → FastAPI container

برای یک پروژه Data Engineering + ML این ساختار README کاملاً استاندارد است.


# Customer Analytics Platform

End-to-End Data Analytics & Machine Learning Platform

This project demonstrates an end-to-end analytics platform
built with modern data engineering, analytics and machine learning tools.

The goal is to analyze customer behavior, generate business insights,
and predict customer churn.
## Business Problem

E-commerce companies need to understand:

- Which customers generate the most value?
- Which products drive revenue?
- Which customers are at risk of churn?
- How can data support business decisions?

This project builds a complete analytics pipeline
to answer these questions.


## Architecture
mermaid
flowchart TD

    A[Data Source<br/>Olist E-commerce CSV Files] --> B[Python ETL<br/>load_raw_data.py]

    B --> C[PostgreSQL<br/>Raw Data Layer]

    C --> D[Great Expectations<br/>Data Quality Validation]

    C --> E[dbt Warehouse<br/>Staging Models + Analytics Marts]

    E --> F[Power BI Dashboard<br/>Business Analytics]

    E --> G[ML Pipeline<br/>Customer Churn Prediction]

    G --> H[FastAPI<br/>ML Prediction API]


## Tech Stack

### Data Engineering

- Python
- PostgreSQL
- Docker
- dbt
- Great Expectations


### Analytics

- SQL
- Pandas
- Power BI


### Machine Learning

- Scikit-learn
- XGBoost
- MLflow


### Deployment

- FastAPI
- Docker
- GitHub Actions

## Project Structure


customer-analytics-platform/

text
.
├── data
│   └── raw
│       └── dataset files
│
├── data_loader
│   ├── Dockerfile
│   ├── requirements.txt
│   └── load_data.py
│
├── src
│   └── data ingestion
│
├── customer_analytics_dbt
│   └── transformation models
│
├── ml
│   ├── feature engineering
│   ├── training
│   └── models
│
├── api
│   └── FastAPI service
│
├── dashboard
│   └── Power BI dashboard
│
└── docker-compose.yml

## Data Pipeline


1. Data ingestion

Raw datasets are loaded into PostgreSQL using a dedicated Docker data loader service.

The loader reads CSV files from:

data/raw/

Expected files:

data/raw/
text
├── olist_orders_dataset.csv
├── olist_order_items_dataset.csv
├── olist_products_dataset.csv
└── olist_order_reviews_dataset.csv

The data_loader container automatically imports these files into PostgreSQL.

2. Data validation

Great Expectations validates data quality.


3. Data transformation

dbt creates analytical models.


4. Analytics

Business KPIs are generated.


5. Machine Learning

Customer churn prediction model is trained.

## Dashboard Preview


### Executive Overview

![Dashboard](dashboard/screenshots/dashboard.png)

### Products 

![Products](dashboard/screenshots/products.png)

## Machine Learning Model


### Problem

Customer churn prediction.


### Features

- Recency
- Frequency
- Monetary Value
- Average Order Value


### Models Tested

- Logistic Regression
- Random Forest
- XGBoost


### Evaluation Metrics

- Accuracy
- Precision
- Recall
- ROC-AUC

Best Model:

Random Forest

ROC-AUC:
0.67


## How To Run


### Prerequisites

Make sure you have installed:

* Docker Desktop
* Docker Compose

No local Python environment is required because all services run inside Docker containers.

---

## 1. Clone Repository

bash
git clone github.com/shokoufehyazdanian/Customer-Analytics-Platform


---

## 2. Dataset Setup

Raw datasets are not included in this repository because of their size.

Download the Brazilian E-Commerce Public Dataset by Olist from Kaggle:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Extract the CSV files into:

data/raw/


Expected structure:

data/
└── raw/
    ├── olist_orders_dataset.csv
    ├── olist_order_items_dataset.csv
    ├── olist_products_dataset.csv
    ├── olist_order_reviews_dataset.csv
    ├── olist_customers_dataset.csv
    ├── olist_sellers_dataset.csv
    ├── olist_geolocation_dataset.csv
    ├── olist_order_payments_dataset.csv
    └── product_category_name_translation.csv


---

## 3. Start Docker Services

Build and start all services:

bash
docker compose up --build -d


This starts:

| Service     | Description                              |
| ----------- | ---------------------------------------- |
| PostgreSQL  | Data warehouse database                  |
| Data Loader | Loads raw CSV files into PostgreSQL      |
| Airflow     | Workflow orchestration and dbt execution |
| FastAPI     | Churn prediction API                     |

---

## 4. Load Raw Data

The data loader runs automatically when Docker starts.

Check loading status:

bash
docker logs customer_data_loader


Successful output:

Loading olist_orders_dataset.csv...
Loaded olist_orders_dataset: xxxx rows

Loading olist_products_dataset.csv...
Loaded olist_products_dataset: xxxx rows

Finished loading data


---

## 5. Run dbt Transformations

Open the Airflow container:

bash
docker exec -it customer_airflow bash


Go to dbt project:

bash
cd /opt/customer_analytics_dbt


Run transformations:

bash
dbt run


Run data quality tests:

bash
dbt test


---

## 6. Access Applications

### Airflow

Open:

http://localhost:8080


### FastAPI

API:

http://localhost:8000


Swagger documentation:

http://localhost:8000/docs


---

## 7. Stop Services

Stop all containers:

bash
docker compose down


---

## Project Execution Flow

CSV Files
    |
    v
Data Loader Container
    |
    v
PostgreSQL
    |
    v
dbt Transformations
    |
    v
Analytics Models
    |
    v
Machine Learning Model
    |
    v
FastAPI Prediction API


All components run inside Docker containers to provide a reproducible environment.


## Future Improvements


- Cloud deployment (AWS/Azure)
- Data warehouse migration
- Real-time streaming pipeline
- Advanced ML monitoring
- Automated retraining



in readme khube?

آره، README الان خیلی خوب شده و برای یک Data Engineering / Analytics Portfolio Project کاملاً قابل ارائه است. فقط چند تا اصلاح کوچک پیشنهاد می‌کنم که حرفه‌ای‌تر بشه و کسی که از GitHub clone می‌کند گیر نکند.

1. Architecture Diagram را کمی دقیق‌تر کن
الان خوبه، ولی چون واقعاً پروژه‌ات این flow را دارد:

CSV → Data Loader Container → PostgreSQL → GX/dbt → Dashboard/ML → FastAPI

این نسخه دقیق‌تر است:

flowchart LR

    A[Olist CSV Dataset<br/>data/raw] --> B[Docker Data Loader<br/>Python + Pandas]

    B --> C[(PostgreSQL<br/>Raw Layer)]

    C --> D[Great Expectations<br/>Data Validation]

    C --> E[dbt Transformation Layer]

    E --> E1[Staging Models]
    E --> E2[Analytics Marts]

    E2 --> F[Power BI Dashboard]

    E2 --> G[Feature Engineering]

    G --> H[ML Pipeline<br/>Scikit-learn/XGBoost]

    H --> I[MLflow<br/>Experiment Tracking]

    H --> J[FastAPI<br/>Churn Prediction API]

    K[Airflow Scheduler] --> E
    K --> H
این بهتر نشان می‌دهد که Airflow کجاست.

2. یک قسمت اضافه کن: Services
بعد از Architecture یک بخش بگذار:

## Docker Services

| Service | Purpose |
|---|---|
| postgres | PostgreSQL database storing raw and transformed data |
| data_loader | Python ETL container loading CSV files |
| airflow | Workflow orchestration and dbt execution |
| churn_api | FastAPI service for churn prediction |
این برای recruiter خیلی کمک می‌کند.

3. قسمت Run کردن یک مشکل کوچک دارد
اینجا:

git clone github.com/shokoufehyazdanian/Customer-Analytics-Platform
باید باشد:

git clone https://github.com/shokoufehyazdanian/Customer-Analytics-Platform.git
4. اضافه کن که dbt داخل Airflow container است
چون خودت این مشکل را داشتی که روی ویندوز:

dbt is not recognized
یک نفر دیگر هم همین مشکل را خواهد داشت.

این قسمت را بعد از dbt اضافه کن:

Note:
dbt is installed inside the Airflow Docker container.
Run dbt commands from inside the container:

docker exec -it customer_airflow bash

cd /opt/customer_analytics_dbt

dbt run
5. Data Loader بخش را کمی اصلاح کن
الان نوشته:

data_loader container automatically imports these files

ولی بهتر است بگویی:

The data_loader Docker service executes load_raw_data.py
and loads CSV files into PostgreSQL automatically during startup.
6. Environment variables
چون داری Docker استفاده می‌کنی، بهتر است .env.example داشته باشی.

مثلاً:

.env.example
با:

POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=customer_analytics
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
نه این:

localhost
5433
چون داخل Docker باید اسم service باشد:

postgres
7. اضافه کن که Docker لازم نیست Python نصب باشد
این قسمت را داری و خوب است:

No local Python environment is required

حتماً نگهش دار.

8. یک بخش Demo اضافه کن
آخر README قبل از Future Improvements:

## Demo

### API Example

Endpoint:

POST /predict


Example request:

```json
{
  "recency": 30,
  "frequency": 5,
  "monetary": 450
}
Response:

{
  "churn_prediction": 0,
  "probability": 0.12
}

این برای ML project خیلی ارزش دارد.

---

### 9. ساختار پروژه کمی اشتباه نوشته شده

این:
├── src
│ └── data ingestion


بهتر:
├── src
│ ├── feature_engineering
│ ├── preprocessing
│ └── utils


چون ingestion الان داخل data_loader است.

---

### 10. Git قبل از push

الان مشکل اصلی تو این است که Git root درست است ولی داری از `Downloads/Project` کل فایل‌ها را می‌بینی.

قبل از commit:

```powershell
git add .
نزن چون ممکن است فایل‌های Downloads بروند.

اول:

git status --ignored
چک کن.

باید فقط پروژه را ببینی:

README.md
docker-compose.yml
customer_analytics_dbt/
api/
ml/
data_loader/
...
بعد:

git add README.md docker-compose.yml api ml data_loader customer_analytics_dbt airflow dashboard src
بعد:

git commit -m "Complete customer analytics platform with Docker pipeline"
و:

git push origin master
در مجموع README فعلی حدود 85-90٪ آماده GitHub Portfolio است. با این چند تغییر، مخصوصاً Docker flow و dbt داخل container، خیلی حرفه‌ای‌تر می‌شود.


Today 9:20 PM
# Customer Analytics Platform

End-to-End Data Analytics & Machine Learning Platform

This project demonstrates an end-to-end analytics platform
built with modern data engineering, analytics and machine learning tools.

The goal is to analyze customer behavior, generate business insights,
and predict customer churn.
## Business Problem

E-commerce companies need to understand:

- Which customers generate the most value?
- Which products drive revenue?
- Which customers are at risk of churn?
- How can data support business decisions?

This project builds a complete analytics pipeline
to answer these questions.


## Architecture
mermaid
flowchart LR

    A[Olist CSV Dataset<br/>data/raw] --> B[Docker Data Loader<br/>Python + Pandas]

    B --> C[(PostgreSQL<br/>Raw Layer)]

    C --> D[Great Expectations<br/>Data Validation]

    C --> E[dbt Transformation Layer]

    E --> E1[Staging Models]
    E --> E2[Analytics Marts]

    E2 --> F[Power BI Dashboard]

    E2 --> G[Feature Engineering]

    G --> H[ML Pipeline<br/>Scikit-learn/XGBoost]

    H --> I[MLflow<br/>Experiment Tracking]

    H --> J[FastAPI<br/>Churn Prediction API]

    K[Airflow Scheduler] --> E
    K --> H


## Docker Services

| Service | Purpose |
|---|---|
| postgres | PostgreSQL database storing raw and transformed data |
| data_loader | Python ETL container loading CSV files |
| airflow | Workflow orchestration and dbt execution |
| churn_api | FastAPI service for churn prediction |

## Tech Stack

### Data Engineering

- Python
- PostgreSQL
- Docker
- dbt
- Great Expectations


### Analytics

- SQL
- Pandas
- Power BI


### Machine Learning

- Scikit-learn
- XGBoost
- MLflow


### Deployment

- FastAPI
- Docker
- GitHub Actions

## Project Structure


customer-analytics-platform/

text
.
├── data
│   └── raw
│       └── dataset files
│
├── data_loader
│   ├── Dockerfile
│   ├── requirements.txt
│   └── load_data.py
│
├── src
│   └── data ingestion
│
├── customer_analytics_dbt
│   └── transformation models
│
├── ml
│   ├── feature engineering
│   ├── training
│   └── models
│
├── api
│   └── FastAPI service
│
├── dashboard
│   └── Power BI dashboard
│
└── docker-compose.yml

## Data Pipeline


1. Data ingestion

Raw datasets are loaded into PostgreSQL using a dedicated Docker data loader service.

The loader reads CSV files from:

data/raw/

Expected files:

data/raw/
text
├── olist_orders_dataset.csv
├── olist_order_items_dataset.csv
├── olist_products_dataset.csv
└── olist_order_reviews_dataset.csv

The data_loader container automatically imports these files into PostgreSQL.

2. Data validation

Great Expectations validates data quality.


3. Data transformation

dbt creates analytical models.


4. Analytics

Business KPIs are generated.


5. Machine Learning

Customer churn prediction model is trained.

## Dashboard Preview


### Executive Overview

![Dashboard](dashboard/screenshots/dashboard.png)

### Products 

![Products](dashboard/screenshots/products.png)

## Machine Learning Model


### Problem

Customer churn prediction.


### Features

- Recency
- Frequency
- Monetary Value
- Average Order Value


### Models Tested

- Logistic Regression
- Random Forest
- XGBoost


### Evaluation Metrics

- Accuracy
- Precision
- Recall
- ROC-AUC

Best Model:

Random Forest

ROC-AUC:
0.67


## How To Run


### Prerequisites

Make sure you have installed:

* Docker Desktop
* Docker Compose

No local Python environment is required because all services run inside Docker containers.

---

## 1. Clone Repository

bash
git clone github.com/shokoufehyazdanian/Customer-Analytics-Platform.git


---

## 2. Dataset Setup

Raw datasets are not included in this repository because of their size.

Download the Brazilian E-Commerce Public Dataset by Olist from Kaggle:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Extract the CSV files into:

data/raw/


Expected structure:

data/
└── raw/
    ├── olist_orders_dataset.csv
    ├── olist_order_items_dataset.csv
    ├── olist_products_dataset.csv
    ├── olist_order_reviews_dataset.csv
    ├── olist_customers_dataset.csv
    ├── olist_sellers_dataset.csv
    ├── olist_geolocation_dataset.csv
    ├── olist_order_payments_dataset.csv
    └── product_category_name_translation.csv


---

## 3. Start Docker Services

Build and start all services:

bash
docker compose up --build -d


This starts:

| Service     | Description                              |
| ----------- | ---------------------------------------- |
| PostgreSQL  | Data warehouse database                  |
| Data Loader | Loads raw CSV files into PostgreSQL      |
| Airflow     | Workflow orchestration and dbt execution |
| FastAPI     | Churn prediction API                     |

---

## 4. Load Raw Data

The data_loader Docker service executes load_raw_data.py
and loads CSV files into PostgreSQL automatically during startup.

Check loading status:

bash
docker logs customer_data_loader


Successful output:

Loading olist_orders_dataset.csv...
Loaded olist_orders_dataset: xxxx rows

Loading olist_products_dataset.csv...
Loaded olist_products_dataset: xxxx rows

Finished loading data


---

## 5. Run dbt Transformations

Note: dbt is installed inside the Airflow Docker container.

Open the Airflow container:
bash
docker exec -it customer_airflow bash


Go to dbt project:

bash
cd /opt/customer_analytics_dbt


Run transformations:

bash
dbt run


Run data quality tests:

bash
dbt test


---

## 6. Access Applications

### Airflow

Open:

http://localhost:8080


### FastAPI

API:

http://localhost:8000


Swagger documentation:

http://localhost:8000/docs


---
## Demo

### API Example

Endpoint:

POST /predict


Example request:

json
{
  "recency": 30,
  "frequency": 5,
  "monetary": 450
}

Response: 
json
{
  "churn_prediction": 0,
  "probability": 0.87
}


## 7. Stop Services

Stop all containers:

bash
docker compose down


---

## Project Execution Flow

CSV Files
    |
    v
Data Loader Container
    |
    v
PostgreSQL
    |
    v
dbt Transformations
    |
    v
Analytics Models
    |
    v
Machine Learning Model
    |
    v
FastAPI Prediction API


All components run inside Docker containers to provide a reproducible environment.


## Future Improvements


- Cloud deployment (AWS/Azure)
- Data warehouse migration
- Real-time streaming pipeline
- Advanced ML monitoring
- Automated retraining

alan khube>?

آره، الان README خیلی بهتر شده و تقریباً آماده GitHub است. برای یک Portfolio پروژه Data Analyst / Data Engineer / ML Engineer سطحش خوبه. فقط چند تا اصلاح کوچک باقی مانده که قبل از push انجام بده:

1. لینک clone هنوز اشتباه است
الان:

git clone github.com/shokoufehyazdanian/Customer-Analytics-Platform.git
باید:

git clone https://github.com/shokoufehyazdanian/Customer-Analytics-Platform.git
2. Project Structure را اصلاح کن
این قسمت:

├── src
│   └── data ingestion
دقیق نیست چون ingestion در data_loader است.

بهتر:

├── src
│   ├── feature_engineering
│   ├── preprocessing
│   └── utils
و:

├── data_loader
│   ├── Dockerfile
│   ├── requirements.txt
│   └── load_raw_data.py
چون اسم فایل واقعی تو load_raw_data.py است.

3. Architecture یک خط کم دارد
الان Airflow فقط به dbt و ML وصل شده:

K[Airflow Scheduler] --> E
K --> H
ولی در واقع بهتر است Airflow کل pipeline را orchestrate کند:

K[Airflow Scheduler] --> B
K --> D
K --> E
K --> H
یعنی:

Airflow → Data Loader → Validation → dbt → ML

چون الان diagram کمی نشان می‌دهد که Data Loader مستقل است.

4. Data Pipeline قسمت اول فقط 4 فایل نشان می‌دهد
ولی پروژه 9 فایل load می‌کند.

این:

├── olist_orders_dataset.csv
├── olist_order_items_dataset.csv
├── olist_products_dataset.csv
└── olist_order_reviews_dataset.csv
بهتر است:

├── olist_orders_dataset.csv
├── olist_order_items_dataset.csv
├── olist_products_dataset.csv
├── olist_order_reviews_dataset.csv
├── olist_customers_dataset.csv
├── olist_sellers_dataset.csv
├── olist_geolocation_dataset.csv
├── olist_order_payments_dataset.csv
└── product_category_name_translation.csv
یا بنویس:

(all Olist CSV files)
5. MLflow را فقط اگر واقعاً استفاده کردی نگه دار
در README نوشتی:

MLflow
و در architecture:

MLflow Experiment Tracking
اگر واقعاً:

mlruns folder داری

experiment ثبت کردی

model version داری

نگه دار.

اگر فقط نصب شده ولی استفاده نشده، حذفش کن، چون reviewer ممکن است دنبال implementation بگردد.

6. Demo خوب است، ولی API path بهتر است
الان:

POST /predict
خوبه.

ولی بهتر:

POST http://localhost:8000/predict
7. یک badge اضافه کن (اختیاری ولی قشنگ می‌کند)
بالای README بعد از title:

![Docker](https://img.shields.io/badge/Docker-enabled-blue)
![Python](https://img.shields.io/badge/Python-3.12-yellow)
![dbt](https://img.shields.io/badge/dbt-analytics-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
8. مهم‌ترین چیز: .env
چون دیدم قبلاً:

.env.txt
داری.

بهتر است:

.env.example
commit شود.

ولی:

.env
در .gitignore بماند.

امتیاز فعلی من:
بخش	وضعیت
Architecture	⭐⭐⭐⭐⭐
Docker explanation	⭐⭐⭐⭐⭐
Data pipeline	⭐⭐⭐⭐
ML explanation	⭐⭐⭐⭐
Reproducibility	⭐⭐⭐⭐⭐
GitHub readiness	⭐⭐⭐⭐½
بعد از این اصلاحات واقعاً آماده portfolio است.

قبل از commit فقط این را انجام بده:

git status
و مطمئن شو این‌ها داخل commit می‌روند:

README.md
docker-compose.yml
data_loader/
customer_analytics_dbt/
api/
ml/
airflow/
dashboard/
و این‌ها نروند:

.env
data/raw/*.csv
venv/
*.pdf
Downloads files
بعد:

git add .
git commit -m "Finalize customer analytics platform documentation and Docker pipeline"
git push origin master
الان پروژه‌ات از نظر ساختار خیلی نزدیک به یک پروژه واقعی تیم Data است.


3. Architecture یک خط کم دارد

الان Airflow فقط به dbt و ML وصل شده:

K[Airflow Scheduler] --> E
K --> H

ولی در واقع بهتر است Airflow کل pipeline را orchestrate کند:

K[Airflow Scheduler] --> B
K --> D
K --> E
K --> H
kamelesho bede copy konam 

این بخش Architecture کامل‌ترش اینه. کل Mermaid را جایگزین کن و مستقیم copy کن:

flowchart LR

    A[Olist CSV Dataset<br/>data/raw] --> B[Docker Data Loader<br/>Python + Pandas]

    B --> C[(PostgreSQL<br/>Raw Layer)]

    C --> D[Great Expectations<br/>Data Validation]

    C --> E[dbt Transformation Layer]

    E --> E1[Staging Models]
    E --> E2[Analytics Marts]

    E2 --> F[Power BI Dashboard]

    E2 --> G[Feature Engineering]

    G --> H[ML Pipeline<br/>Scikit-learn/XGBoost]

    H --> I[MLflow<br/>Experiment Tracking]

    H --> J[FastAPI<br/>Churn Prediction API]

    K[Airflow Scheduler<br/>Workflow Orchestration] --> B
    K --> D
    K --> E
    K --> H


```

## Docker Services

| Service | Purpose |
|---|---|
| postgres | PostgreSQL database storing raw and transformed data |
| data_loader | Python ETL container loading CSV files |
| airflow | Workflow orchestration and dbt execution |
| churn_api | FastAPI service for churn prediction |

## Tech Stack

### Data Engineering

- Python
- PostgreSQL
- Docker
- dbt
- Great Expectations


### Analytics

- SQL
- Pandas
- Power BI


### Machine Learning

- Scikit-learn
- XGBoost
- MLflow


### Deployment

- FastAPI
- Docker
- GitHub Actions

## Project Structure


customer-analytics-platform/

```text
.
├── data
│   └── raw
│       └── dataset files
│
├── data_loader
│   ├── Dockerfile
│   ├── requirements.txt
│   └── load_data.py
│
├── src
│   └── data ingestion
│
├── customer_analytics_dbt
│   └── transformation models
│
├── ml
│   ├── feature engineering
│   ├── training
│   └── models
│
├── api
│   └── FastAPI service
│
├── dashboard
│   └── Power BI dashboard
│
└── docker-compose.yml
```
## Data Pipeline


1. Data ingestion

Raw datasets are loaded into PostgreSQL using a dedicated Docker data loader service.

The loader reads CSV files from:

data/raw/

Expected files:

data/raw/
```text
├── olist_orders_dataset.csv
├── olist_order_items_dataset.csv
├── olist_products_dataset.csv
├── olist_order_reviews_dataset.csv
├── olist_customers_dataset.csv
├── olist_sellers_dataset.csv
├── olist_geolocation_dataset.csv
├── olist_order_payments_dataset.csv
└── product_category_name_translation.csv
```
The data_loader container automatically imports these files into PostgreSQL.

2. Data validation

Great Expectations validates data quality.


3. Data transformation

dbt creates analytical models.


4. Analytics

Business KPIs are generated.


5. Machine Learning

Customer churn prediction model is trained.

## Dashboard Preview


### Executive Overview

![Dashboard](dashboard/screenshots/dashboard.png)

### Products 

![Products](dashboard/screenshots/products.png)

## Machine Learning Model


### Problem

Customer churn prediction.


### Features

- Recency
- Frequency
- Monetary Value
- Average Order Value


### Models Tested

- Logistic Regression
- Random Forest
- XGBoost


### Evaluation Metrics

- Accuracy
- Precision
- Recall
- ROC-AUC

Best Model:

Random Forest

ROC-AUC:
0.67


## How To Run


### Prerequisites

Make sure you have installed:

* Docker Desktop
* Docker Compose

No local Python environment is required because all services run inside Docker containers.

---

## 1. Clone Repository

```bash
git clone https://github.com/shokoufehyazdanian/Customer-Analytics-Platform.git
```

## 2. Dataset Setup

Raw datasets are not included in this repository because of their size.

Download the Brazilian E-Commerce Public Dataset by Olist from Kaggle:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

Extract the CSV files into:

```
data/raw/
```

Expected structure:

```
data/
└── raw/
    ├── olist_orders_dataset.csv
    ├── olist_order_items_dataset.csv
    ├── olist_products_dataset.csv
    ├── olist_order_reviews_dataset.csv
    ├── olist_customers_dataset.csv
    ├── olist_sellers_dataset.csv
    ├── olist_geolocation_dataset.csv
    ├── olist_order_payments_dataset.csv
    └── product_category_name_translation.csv
```

---

## 3. Start Docker Services

Build and start all services:

```bash
docker compose up --build -d
```

This starts:

| Service     | Description                              |
| ----------- | ---------------------------------------- |
| PostgreSQL  | Data warehouse database                  |
| Data Loader | Loads raw CSV files into PostgreSQL      |
| Airflow     | Workflow orchestration and dbt execution |
| FastAPI     | Churn prediction API                     |

---

## 4. Load Raw Data

The data_loader Docker service executes load_raw_data.py
and loads CSV files into PostgreSQL automatically during startup.

Check loading status:

```bash
docker logs customer_data_loader
```

Successful output:

```
Loading olist_orders_dataset.csv...
Loaded olist_orders_dataset: xxxx rows

Loading olist_products_dataset.csv...
Loaded olist_products_dataset: xxxx rows

Finished loading data
```

---

## 5. Run dbt Transformations

Note: dbt is installed inside the Airflow Docker container.

Open the Airflow container:
```bash
docker exec -it customer_airflow bash
```

Go to dbt project:

```bash
cd /opt/customer_analytics_dbt
```

Run transformations:

```bash
dbt run
```

Run data quality tests:

```bash
dbt test
```

---

## 6. Access Applications

### Airflow

Open:

```
http://localhost:8080
```

### FastAPI

API:

```
http://localhost:8000
```

Swagger documentation:

```
http://localhost:8000/docs
```

---
## Demo

### API Example

Endpoint:

POST http://localhost:8000/predict

Example request:

```json
{
  "recency": 30,
  "frequency": 5,
  "monetary": 450
}
```
Response: 
```json
{
  "churn_prediction": 0,
  "probability": 0.87
}
```

## 7. Stop Services

Stop all containers:

```bash
docker compose down
```

---

## Project Execution Flow

```
CSV Files
    |
    v
Data Loader Container
    |
    v
PostgreSQL
    |
    v
dbt Transformations
    |
    v
Analytics Models
    |
    v
Machine Learning Model
    |
    v
FastAPI Prediction API
```

All components run inside Docker containers to provide a reproducible environment.


## Future Improvements


- Cloud deployment (AWS/Azure)
- Data warehouse migration
- Real-time streaming pipeline
- Advanced ML monitoring
- Automated retraining
