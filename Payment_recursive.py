import json 
import requests 
import psycopg2 #Import the psycopg2 for the postgres-binary  for request the database from the cloud heroku 
import uuid # Generate uuid encode the login session 
import paypalrestsdk
from itertools import count  
from paypalcheckoutsdk.core import PayPalHttpClient, LiveEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalhttp import HttpError 
from itertools import count
#from roboreactmaster import Create_node_sub,get_datetime # Getting the date time running the incuresive payment
import secrets
import datetime # check current date 

DATABASE_URL = "postgres://wwpxpsshftlinh:b85574f77cd76ccbaef7a0f661086c6b28724d236c730c74c2d8021934e8bbe1@ec2-18-215-96-54.compute-1.amazonaws.com:5432/d8rl9i6joj63v8"
Host = "ec2-18-215-96-54.compute-1.amazonaws.com"
Database = "d8rl9i6joj63v8"
Password = "b85574f77cd76ccbaef7a0f661086c6b28724d236c730c74c2d8021934e8bbe1"
Port = "5432"
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#Payment function 
PUBLIC_KEY = "pkey_5ov0wg43quxwx1xsm8s"
SECRET_KEY = "skey_5ov0wgvkh2zpg7qh9tl"
paypalrestsdk.configure({
  "mode": "live", # sandbox or live
  "client_id": "AevuTpnclVhyJZICMY3CY5w0i2riVW9HcjVWXIsnz3aO6NhubjGHQ-bOFIR-OW2WNZbzs_icwBIn9EPn",
  "client_secret": "ECbnY9Vp8rVxU6K6sngSdsa6juQAwEuLYIZqckuiIYTRxVh50Ij9tRyLrHM4yYY2Ib5xyMvVQZQ64lMg" })

data_current = {}
data_map = []

def updatexpire(cardholder,chrtoken,payment):
                    conn = psycopg2.connect(
                    DATABASE_URL,
                    sslmode='require',
                    )
                    c = conn.cursor()
                    c.execute('''CREATE TABLE IF NOT EXISTS customers
                    (index Text,
                    first_name Text,
                    last_name Text,
                    e_mail Text,
                    password Text,
                    address Text,
                    payment_status Text,
                    cardholder Text,
                    schedule Text,
                    recharge Text);''')
                    # Create a cursor
                    c = conn.cursor()
                    cur = conn.cursor()
                    # Change from INDEX into the card holder data to using as reference 
                    r = requests.get("http://0.0.0.0:4050")
                    current_data = r.json() # Getting the current data on the json format
                    #Submit the database data from the cloud database to get into the function of the submit registration 
                    # update current data of the expiration date after the payment
                    cur.execute("UPDATE customers set schedule = %s where cardholder = %s",(str({'Token':str(chrtoken),'Payment':str(payment),'Time':str("expired")}),str(cardholder),))
                    conn.commit()
                    print("Total updated rows:", cur.rowcount)

def fetchdatabase():
                    conn = psycopg2.connect(
                    DATABASE_URL,
                    sslmode='require',
                    )
                    c = conn.cursor()
                    c.execute('''CREATE TABLE IF NOT EXISTS customers
                    (index Text,
                    first_name Text,
                    last_name Text,
                    e_mail Text,
                    password Text,
                    address Text,
                    payment_status Text,
                    cardholder Text,
                    schedule Text,
                    recharge Text);''')
                    # Create a cursor
                    c = conn.cursor()
                    #Grab stuff from online database 
                    c.execute("SELECT*FROM customers")
                    records = c.fetchall() 
                  
                    for rowdata in records:
                           
                       if rowdata not in data_map:
                          # add data into the list if not in the list    
                          data_map.append(rowdata) 
                          data_current[rowdata[0]] = (str(rowdata[1]),str(rowdata[2]),str(rowdata[3]),str(rowdata[4]),str(rowdata[5]),str(rowdata[6]),str(rowdata[7]),str(rowdata[8]),str(rowdata[9]))
                          # Running the for loop to check the date of the user inside and collect the index and the token to change the position 
                       for date_check in list(data_current):
                                 # 
                                 cardholder = str(data_current[date_check][1])+str(data_current[date_check][2]) #Creating the card golder 
                                 if data_current[date_check][8] != "Non":
                                       data_update_expired = json.loads(data_current[date_check][8])  
                                       print(data_current.get(date_check)," Get expire date ",data_update_expired,type(data_update_expired)) # get the tuple inside the list to check the expiration date count
                                       # update the epiration date into the database 
                                       current_date = datetime.datetime.now().date()
                                       if str(data_update_expired.get('Time').get('expire_date')) == str(current_date): # Checking current date time to activate the paement data 
                                                         print("Updating expiration and update database token")
                                                         # Getting the json data of token and payment id and the 
                                                         Token_data = data_update_expired.get('Token')
                                                         Payment_data = data_update_expired.get('Payment')
                                                         Time_data = data_update_expired.get('Time') 
                                                         print("Current data of card",Token_data,Payment_data,Time_data) # Getting the current data of card 
                                                         updatexpire(cardholder,"Non","Non")

for i in count(0):                                
      fetchdatabase() # Getting the database from the cloud heroku of the payment in the paypal token data 
      print(data_current)
      print(str(i),data_map)