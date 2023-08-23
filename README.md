# FetchRewardsAssessment #
## Data Engineering: ETL off a SQS Qeueue ##
## To run the code follow the below steps
Step-1. Clone this repo.
```bash
git clone https://github.com/Urvashi-Patel/FetchRewards_DE_Assessment.git
```

Step-2. Go into the cloned repo directory.
```bash
cd FetchRewards_DE_Assessment
```

Step-3. Upgrade the pip version.
```bash
python -m pip install -U pip
```

Step-4. Run the requirements.txt file.
```bash
pip install -r requirements.txt
```

Step-5. Pull the postgres docker image.
```bash
docker pull fetchdocker/data-takehome-postgres
```

Step-6. Pull the localstack docker image.
```bash
docker pull fetchdocker/data-takehome-localstack
```

Step-7. Run docker-compose command.
```bash
docker-compose up -d
```

Step-8. Run psql command.
```bash
psql -d "dbname='postgres' user='postgres' password='postgres' host='localhost'" -f table_ddl.sql
```

Step-9. Run load_sqs_to_postgres.py file.
```bash
python load_sqs_to_postgres.py
```

Step-10. Post load validation using below command in postgres.
```bash
select * from user_logins;
```

#### We can Unmasked ip and device_id using below command #####
```bash
select *, convert_from(decode(masked_ip, 'base64'), 'UTF8') as unmasked_ip,  convert_from(decode(masked_device_id, 'base64'), 'UTF8') as unmasked_ip from user_logins;
```
