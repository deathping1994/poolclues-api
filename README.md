# poolclues-api
Python Apis for PoolClues
Test server for front end setup at http://188.166.249.229:8080/
so use it as url in front end.
NOTE: This ip address is blocked in college so use proxy to access it in college

To test if you are apble to connect to server send http get request to http://188.166.249.229:8080/ or try to open it in browser

response should be
       {
       "success": "It works"
       }

#Api description:
## Register User
### endpoint: `/register`
so url will be `http://188.166.249.229:8080/register`

### Samle payload:
       {
        "first_name": "Gaurav",
       "middle_name":"Ramakant",
       "last_name": "Shukla",
       "email_id":"deathping1994@gmail.com",
       "password":"bastard007",
       "house_no":"559 ka/48 kha",
       "street":"Singar Nagar",
       "city":"Lucknow",
       "state":"Uttar Pradesh",
       "country":"India",
       "phone":"8375847862"     //optional
       }

### Response:  
      {
         "success": "User successfully registered"
     }
or
     {
     "error": "Oops something went wrong. Contact the adminsitrator"
     }

### endpoint: /authenticate
example: http://188.166.249.229:8080/logout/gshukla66@gmail.com

#### payload:
       {
       "email_id":<user's email_id>,
       "password":<user's password>
       }
### Response:
       {
       "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq",
       "success": "Successfully Logged in !"
       }
       or
       {
       "error":"Some error message"
       }


### endpoint: /logout/:email_id:
example: http://188.166.249.229:8080/logout/gshukla66@gmail.com

#### payload:
       {"authtoken":<user's suth token>
       }
### Response:
       {
       "success":"Successfully logged off"
       }
       or
       {
       "error":"Some error message"
       }
NOTE: As of now this endpoint return successfully logged off even when you are not logged in , this is a bug but wont be fixed keeping in mind that this system would be replaced with three legged auth system using redis,and JWT


### endpoint: /:email_id:/addphone/:phonenumber:
example: http://188.166.249.229:8080/gshukla66@gmail.com/addphone/8375847862

#### payload:
       {"authtoken":<user's suth token>
       }
### Response:
       {
       "success":"Contact added Successfully!"
       }
       or
       {
       "error":"Some error message"
       }

 ### endpoint: /:email_id:/event/list

 example: http://188.166.249.229:8080/gshukla66@gmail.com/event/list

 ### Response:
       {
    "event_list": [
     {
         "date_created": "2015-10-08",
         "event_description": "Too lazy for that",
         "event_id": 106,
         "event_name": "Gaurav's b'day",
         "public": true,
         "target_amount": 5000,
         "target_date": "2015-12-11"
     },
     {
         "date_created": "2015-10-08",
         "event_description": "Too lazy for that",
         "event_id": 106,
         "event_name": "Gaurav's b'day",
         "public": true,
         "target_amount": 5000,
         "target_date": "2015-12-11"
     },
     {
         "date_created": "2015-10-08",
         "event_description": "Too lazy for that",
         "event_id": 106,
         "event_name": "Gaurav's b'day",
         "public": true,
         "target_amount": 5000,
         "target_date": "2015-12-11"
     }
    ]
    }          or
        {
        "error":"Some error message"
        }


### endpoint: /event/:event_id:

example: http://188.166.249.229:8080/event/115

### Response:
       {
           "event_description": "Too lazy for that",
           "event_id": 115,
           "event_name": "Gaurav's b'day",
           "target_amount": 5000,
           "target_date": "2015-12-11"
       }
       or
       {
       "error":"Some error message"
       }
### endpoint: /event/create
example: http://188.166.249.229:8080/event/115

### Payload:
      {"email_id":"94@gmail.com",
        "event_name": "Gaurav's b'day",
        "target_date": "11122015",
        "target_amount":"5000",
        "description":"Too lazy for that",
        "invites": [{"email_id":"deathping1994@gmail.com"}
 			],
        "msg": "new custom message"

      }
### Response:
       {
           "event_id": 115,
           "success": "event created successfully"
       }
       or
       {
       "error":"Some error message"
       }
