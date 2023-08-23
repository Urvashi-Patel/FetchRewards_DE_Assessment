import boto3
import pandas as pd
import base64
import subprocess
import psycopg2
from sqlalchemy import create_engine

class Adapter():
    """Class for performing SQS process using ETL"""

    def __init__(self, host, database, user, password):
        """To get the postgresql credentials"""

        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def recieve_message(self):
        """Read the message from docker image using awslocal sqs url"""

        response = eval(subprocess.check_output("awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue", shell=True))
        message = [eval(i["Body"]) for i in response['Messages']]
        return message
    
    def maksing_process(self,message):
        """This method is used for masking id and device_id using base64"""

        messageDf = pd.DataFrame.from_dict(message)
        messageDf['masked_ip'] = messageDf.ip.str.encode('utf-8', 'strict').apply(base64.b64encode).str.decode('utf-8', 'strict')
        messageDf['masked_device_id'] = messageDf.device_id.str.encode('utf-8', 'strict').apply(base64.b64encode).str.decode('utf-8', 'strict')

        messageDf['create_date'] = pd.Timestamp('now')
        messageDf=messageDf[["user_id","device_type","masked_ip","masked_device_id","locale","app_version","create_date"]]
        return messageDf

    def load_to_postgresql(self,messageDf):
        """This method is used for load data to the posgtresql db"""

        try:
            pg_con = psycopg2.connect(
                    host = self.host,
                    database = self.database,
                    user = self.user,
                    password = self.password
                )
            cursor = pg_con.cursor()
            print("Connection successful!")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)


        engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/postgres')

        messageDf.to_sql('user_logins', engine, if_exists='append', index=False)

def main():
    """Define main method"""
        
    sqs_process_obj = Adapter('localhost', 'postgres', 'postgres', 'postgres')
    message = sqs_process_obj.recieve_message()
    messageDf = sqs_process_obj.maksing_process(message)
    sqs_process_obj.load_to_postgresql(messageDf)
    return


if __name__ == "__main__":
    main()