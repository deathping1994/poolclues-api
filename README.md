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
###endpoint: `/register`
so url will be `http://188.166.249.229:8080/register`

###Samle payload: 
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
       "country":"India"
       }

###Response:  
      {
         "success": "User successfully registered"
     }
or 
     {
     "error": "Oops something went wrong. Contact the adminsitrator"
     }
     
