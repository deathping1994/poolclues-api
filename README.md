# poolclues-api
Python Apis for PoolClues
Test server for front end setup at http://api.poolclues.anip.xyz:8080/
so use it as url in front end.
NOTE: This ip address is blocked in college so use proxy to access it in college

To test if you are apble to connect to server send http get request to http://api.poolclues.anip.xyz:8080/ or try to open it in browser

response should be
               {
               "success": "It works"
               }

#Api description:
# User
## Register
### endpoint: `/register`
so url will be `http://api.poolclues.anip.xyz:8080/register`

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
               "phone":"8375847862",     //optional
               "user_img":"imgae url"  //optional
               }

### Response:  
              {
                 "success": "User successfully registered"
             }
        or
             {
             "error": "Oops something went wrong. Contact the adminsitrator"
             }

## Fblogin
### endpoint: `/fblogin`
so url will be `http://api.poolclues.anip.xyz:8080/fblogin`

### Samle payload:
               {
               "fbtoken":"send fb token here",
                "first_name": "Gaurav",
               "middle_name":"Ramakant",
               "last_name": "Shukla",
               "email_id":"deathping1994@gmail.com",
               "password":"",  //don't send any password
               "house_no":"559 ka/48 kha",
               "street":"Singar Nagar",
               "city":"Lucknow",
               "state":"Uttar Pradesh",
               "country":"India",
               "phone":"8375847862",     //optional
               "user_img":"imgae url"  //optional
               }

### Response:  
              {
                 "success": "User successfully logged in",
                 "authtoken": "$2b$12$WI1yg7EgIo0MbGblJd7sA.zhaPBSpMuKenvnoWEiiUANR1ywBOEaC"
             }
        or
             {
             "error": "Oops something went wrong. Contact the adminsitrator"
             }
 

 
## Verify Email
### endpoint: `/:email:/verify`
so url will be `http://localhost:8080/gshukla66@gmail.com/verify`

### Samle payload:
              {
             "authtoken": "$2b$12$WI1yg7EgIo0MbGblJd7sA.zhaPBSpMuKenvnoWEiiUANR1ywBOEaC",
             "verification_code":"7OL124"
              }
              
### Response:  
             {
                "success": ""Email Successfully verified"
            }
        or
            {
            "error": "Some error message"
            }
## Forgot Password (Generate password change request)
### endpoint: `/forgotpassword/:user:`
so url will be `http://localhost:8080/forgotpassword/gshukla66@gmail.com`

### Response:  
                {
                   "success": "Password change request has been recorded check your email for further instructions."
               }
            or
               {
               "error": "Some error message"
               }

## Login
### endpoint: /authenticate
example: http://api.poolclues.anip.xyz:8080/logout/gshukla66@gmail.com

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
        
## Logout
### endpoint: /logout/:email_id:
example: http://api.poolclues.anip.xyz:8080/logout/gshukla66@gmail.com

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
NOTE: As of now this endpoint return successfully logged off even when you are not logged in ,
this is a bug but wont be fixed keeping in mind that this system would be replaced with three legged auth system using redis,and JWT

## Add Phone Number
### endpoint: /:email_id:/addphone/:phonenumber:
example: http://api.poolclues.anip.xyz:8080/gshukla66@gmail.com/addphone/8375847862

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

# Products
## Product Search
### endpoint: `/products/search`
### Both get and Post Allowed
so url will be `http://localhost:8080/products/search?query="search keyword"`
or http://localhost:8080/products/search?query=beautiful%20watch&from=100

default size is 10
and default from is 0

where from denotes the result number eg: is total matches is 100 and from is 30 
then products from 30 onwards are returned
### Samle payload:
              {
             "authtoken": "$2b$12$WI1yg7EgIo0MbGblJd7sA.zhaPBSpMuKenvnoWEiiUANR1ywBOEaC"
              }
              
### Response:  
            {
              "hits": [
                {
                  "_id": "97805",
                  "_index": "products",
                  "_score": 0.8274903,
                  "_source": {
                    "Brand": "Suunto",
                    "COD": "Yes",
                    "Category Id": "1559",
                    "Category Path": "Jewelry & Watches///Watches///Unisex",
                    "Customer_type": "R",
                    "Deal": "No",
                    "Discount (percentage)": "15%",
                    "EMI": "Yes",
                    "FreeBee Inside": "No",
                    "Gender": "U",
                    "Leaf Category": "Unisex",
                    "Leaf CategoryId": "1559",
                    "MRP": "22950.00",
                    "Meta category": "Jewelry  Watches",
                    "Price": "19508.00",
                    "Product ID": "97805",
                    "Product Label1": "NotAvailable",
                    "Product Label2": "NotAvailable",
                    "Product Label3": "NotAvailable",
                    "Product Label4": "NotAvailable\n",
                    "Product Name": "Suunto Quest Orange Watch SS018154000",
                    "Product URL": "http://www.shopclues.com/suunto-quest-orange-watch-ss018154000.html",
                    "Shipping Cost": "0.00",
                    "Stock": "Yes",
                    "Warranty": "NotAvailable",
                    "image_path": "http://cdn.shopclues.net/images/detailed/85/SUUNTO_QUEST_ORANGE.jpg"
                  },
                  "_type": "product"
                }
              ],
              "max_score": 1.3740486,
              "total": 202
            }
### endpoint: /:user:/change/password
TO change password once the forgot password request has been generated
example: http://api.poolclues.anip.xyz:8080/gshukla66@gmail.com/change/password

### Payload:
          {
            "request_code":"password change request code sent in email".
            "new_password":"new password"
          }
### Response:
       {
           "success": "Password changed successfully"
       }
       or
       {
       "error":"Some error message"
       }

## Change Password without forgot password

### endpoint: /:user:/change/password/2
example: http://api.poolclues.anip.xyz:8080/gshukla66@gmail.com/change/password/2

### Payload:
          {
            "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq",
            "new_password": "new password here"
          }
### Response:
       {
           "success": "Password updated successfully"
       }
       or
       {
       "error":"Some error message"
       }


# POOL

### endpoint: /:email_id:/pool/list/:type:

type can be invited, all, created
contributed : List all pools the user has contributed to
created : List all events user has created
all : Include both created and contributed
 example: http://api.poolclues.anip.xyz:8080/gshukla66@gmail.com/pool/list/invited

### Response:

               {
            "pool_list": [
             {
                 "date_created": "2015-10-08",
                 "pool_description": "Too lazy for that",
                 "pool_id": 106,
                 "pool_name": "Gaurav's b'day",
                 "public": true,
                 "target_amount": 5000,
                 "target_date": "2015-12-11"
             },
             {
                 "date_created": "2015-10-08",
                 "pool_description": "Too lazy for that",
                 "pool_id": 106,
                 "pool_name": "Gaurav's b'day",
                 "public": true,
                 "target_amount": 5000,
                 "target_date": "2015-12-11"
             }
            ]
            }   
               or
            {
            "error":"Some error message"
            }
           
            
### endpoint: /pool/:pool_id:

### Usage:
To give details of a single pool
example: http://api.poolclues.anip.xyz:8080/pool/115

### Response:
       {
            "contributors": [
                {
                    "amount": 2500,
                    "amount_paid": null,
                    "email_id": "deathping19@gmail.com",
                    "status": "UNPAID"
                },
                {
                    "amount": 2500,
                    "amount_paid": null,
                    "email_id": "deathping192@gmail.com",
                    "status": "UNPAID"
                }
            ],
            "is_creator":true,
            "pool_description": "Too lazy for that",
            "pool_id": 116,
            "pool_name": "Gaurav's b'day",
            "target_amount": 5000,
            "target_date": "2015-12-11"
        }
       or
       {
       "error":"Some error message"
       }
## Create New Pool       
### endpoint: /pool/create
example: http://api.poolclues.anip.xyz:8080/pool/create

### Payload:
          {"email_id":"94@gmail.com",
            "pool_name": "Gaurav's b'day",
            "pool_img": "url for pool image"  //optional
            "target_date": "11122015",
            "target_amount":"5000",
            "description":"Too lazy for that",
            "contributors": [{"email_id":"deathping1994@gmail.com","amount":"2000"},// minimum two contributors required
                            {"email_id":"94@gmail.com","amount":"2000"}         // creator must also be a contributor 
                ],
            "products":["id1","id2"],  //Array of pid of products selected as gift (optional in case of cash voucher do not pass this field)
    
            "msg": "new custom message",
            "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq",
            "searchable": true
    
          }
### Response:
       {
        "failedlist": [],
        "inviteSent": true,
        "pool_id": 116,
        "success": "Pool created successfully."
       }
       or
       {
       "error":"Some error message"
       }

## Add new Contributors
### endpoint: /pool/:pool_id:/contributor/add
example: http://api.poolclues.anip.xyz:8080/event/104/invite
### Payload:
          {
            "contributors": [{"email_id":"deathping1994@gmail.com","amount":2000}  // amount here is not optional.
                ],
            "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq"
          }
### Response:
       {
           "success": "Invites sent successfully"
       }
       or
       {
       "error":"Some error message"
       }

## Delete Pool
### endpoint: /:email_id:/pool/:pool_id:/delete
example: http://api.poolclues.anip.xyz:8080/gshukla66@gmail.com/pool/104/delete
### Payload:
          {
            "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq"
          }
### Response:
       {
           "success": "Pool Deleted successfully"
       }


## Modify Pool
### endpoint: /:email_id:/pool/:pool_id:/update
example: http://api.poolclues.anip.xyz:8080/gshukla66@gmail.com/pool/104/update
###Note: Constraints This api can't be used to upload images, and target amount can't be reduced
Only send fields that need to be updated
### Payload:
          { "pool_name": "Gaurav's b'day",
            "target_date": "11122015",
            "target_amount":"5000",
            "description":"Too lazy for that",
            "searchable": true
           "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq"
          }
### Response:
           {
           "success":"Pool updated Successfully"
           }
## Find Share
### endpoint: /:email_id:/:pool_id:/find/share
example: http://api.poolclues.anip.xyz:8080/gshukla66@gmail.com/103/find/share

### Payload:
          {
            "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq"
          }
### Response:
       {
           "success": "Payment request submitted check status in the payment history"
       }
       or
       {
       "error":"Some error message"
       }

## Pay your share in pool
### endpoint: /:email_id:/pay/:pool_id:
example: http://api.poolclues.anip.xyz:8080/gshukla66@gmail.com/pay/103

### Payload:
          {
            "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq"
          }
### Response:
       {
           "success": "Payment request submitted check status in the payment history"
       }
       or
       {
       "error":"Some error message"
       }
# Registry
Registry is like wish list of user. User creates a registry and selects products which he wants to receive as gifts. 
Invite is send to all email id from whom user wishes to get a gift.
User is not bound to make any payment and only this products get delivered for which the payment is complete

## Create Registry

### end point : /registry/create
example: http://api.poolclues.anip.xyz:8080/registry/create

### Payload:
          {
            "email_id":"deathping1994@gmail.com",
            "registry_name": "Gaurav's b'day",
            "target_date": "11122015",
            "description":"Too lazy for that",
            "invites": [{"email_id":"poolclues@gmail.com","amount":3000
            }],
            "products":["id1","id2"], 
            "msg": "new custom message",
            "authtoken": "$2b$12$zXJud8qrfsPbMjdyLULT7O13LsrJ.LfO5RwwxrpCvy3cuSyrqXPqS",
            "public": true   //optional By default Assumed too be true

            }
### Response:
           {
               "failedlist": [],
                "inviteSent": true,
                "registry_id": 105,
                "success": "Registry created successfully."
            }
           or
           {
           "error":"Some error message"
           }

## Show Details of all registry
### endpoint: :email_id:/registry/list
example: http://api.poolclues.anip.xyz:8080/deathping1994@gmail.com/registry/list
### Payload:
          {
            "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq"
          }

### Response:
        {
        "registry_list": [
            {
                "date_created": "2015-11-28",
                "pool_description": "Too lazy for that",
                "pool_id": 102,
                "pool_name": "Gaurav's b'day",
                "searchable": true,
                "target_date": "2015-12-11"
            }
        ]
        }
        or
        {
        "error":"Some Error Message"
        }
## Show Details of single registry
### endpoint: /registry/:registry_id:
example: http://api.poolclues.anip.xyz:8080/registry/104
### Payload:
          {
            "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq"
          }
### Response:
       {
            "giftbucket": [
                {
                    "pid": "id1",
                    "status": null
                },
                {
                    "pid": "id2",
                    "status": null
                }
            ],
            "invitees": [
                "poolclues@gmail.com"
            ],
            "is_creator": true,
            "registry_description": "Too lazy for that",
            "registry_id": 101,
            "registry_name": "Gaurav's b'day",
            "target_date": "2015-12-11"
       }

## Delete Registry
### endpoint: /:email_id:/registry/:registry_id:/delete
example: http://api.poolclues.anip.xyz:8080/gshukla66@gmail.com/registry/104/delete
### Payload:
          {
            "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq"
          }
### Response:
       {
           "success": "Registry Deleted successfully"
       }


## Modify Registry
### endpoint: /:email_id:/registry/:registry_id:/update
example: http://api.poolclues.anip.xyz:8080/gshukla66@gmail.com/registry/104/update
###Note: Constraints This api can't be used to upload images, and target amount can't be reduced
Only send fields that need to be updated
### Payload:
          { "registry_name": "Gaurav's b'day",
            "target_date": "11122015",
            "target_amount":"5000",
            "description":"Too lazy for that",
            "searchable": true
           "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq"
          }
### Response:
           {
           "success":"Pool updated Successfully"
           }

## Invite in Registry
### endpoint: /registry/:registry_id:/invite
example: http://api.poolclues.anip.xyz:8080/registry/104/invite
### Payload:
          {
            "invites": [{"email_id":"deathping1994@gmail.com","amount":2000}
                ],
            "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq"
          }
### Response:
       {
           "success": "Invites sent successfully"
       }
       or
       {
       "error":"Some error message"
       }

# Wallet

## Show wallet amount
### endpoint: `/:email_id:/wallet`
### Payload:
            {
            "authtoken": "your auth token"
            }
### Response:
            {"amount": amount in wallet
             }
             or 
             {"error": "Some error msg"
             }

## Transaction History

Shows list of all transaction by a particular user. Where pool_id ='' in response then the money was added to wallet.
if pool_id=event id or registry id 

### endpoint: /:emailid:/wallet/history
example: http://api.poolclues.anip.xyz:8080/gshukla66@gmail.com/wallet/history

### Payload:
          {
            "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq"
          }
### Response:
       {
            "transactions": [
                {
                    "amount": 0,
                    "date": "2015-11-04",
                    "pool_id": "",
                    "transaction_id": "$2b$12$C1Ba/kQF3jhBNNdKpzUy6uCPGRTRym0/SCgA.48Cr463G0nxOHMSm"
                },
                {
                    "amount": 400,
                    "date": "2015-11-04",
                    "pool_id": "",
                    "transaction_id": "$2b$12$Q9yqx80LPuDBX3KCL9x0Y.Bn8T/gNplTzD2YnNvcEVYUm.Zlq8aqa"
                }
            ]
        }
       or
       {
       "error":"Some error message"
       }


## Dummy Payment (Add money to wallet)

Each user is given a wallet when he signs up all the payments are processed via this wallet. Initially the balance is zero
to add money to wallet user needs to be logged in and then submit a request to add money to wallet via this url.

### endpoint: /:emailid:/wallet/add
example: http://api.poolclues.anip.xyz:8080/gshukla66@gmail.com/wallet/add

### Payload:
          {
            "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq",
            "amount": 5000
          }
### Response:
       {
           "success": "Payment request submitted check status in the payment history"
       }
       or
       {
       "error":"Some error message"
       }

##List all POSTS on POOL AND REGISTRY timeline
### endpoint: /:event_id:/post/list
example: http://api.poolclues.anip.xyz:8080/104/post/list

### Payload:
          {
            "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq"
          }
### Response:
       {
            "posts": [
                {
                    "author": "deathping1994@gmail.com",
                    "comments": [],
                    "content": "hi how are you ganesh ?",
                    "post_id": 10
                },
                {
                    "author": "deathping1994@gmail.com",
                    "comments": [
                        {
                            "author": "deathping1994@gmail.com",
                            "comment_id": 20,
                            "content": "hi how are you ganesh ?"
                        }
                    ],
                    "content": "hi how are you ganesh ?",
                    "post_id": 11
                }
            ]
        }
       or
       {
       "error":"Some error message"
       }

##List single POST
### endpoint: /:event_id:/post/:post_id:
example: http://api.poolclues.anip.xyz:8080/104/post/21

### Payload:
          {
            "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq"
          }
### Response:
       {
            "author": "deathping1994@gmail.com",
            "comments": [
                {
                    "author": "deathping1994@gmail.com",
                    "comment_id": 20,
                    "content": "hi how are you ganesh ?"
                }
            ],
            "content": "hi how are you ganesh ?",
            "post_id": 11
        }
       or
       {
       "error":"Some error message"
       }




##POSTS on POOL AND REGISTRY timeline
### endpoint: /:event_id:/post
example: http://api.poolclues.anip.xyz:8080/104/post

### Payload:
          {
            "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq",
            "content": "post content goes here"
          }
### Response:
       {
           "success": "Posted Successfully"
       }
       or
       {
       "error":"Some error message"
       }


##Comments on Posts
### endpoint: /:event_id:/:post_id/comment
example: http://api.poolclues.anip.xyz:8080/104/21/comment

### Payload:
          {
            "authtoken": "$2a$12$wdss4GzgeKb/JW/HUpINjO0pZ462LF65U2dBnlHAGmF7TIndhdRgq",
            "content": "comment content goes here"
          }
### Response:
       {
           "success": "Comment Posted Successfully"
       }
       or
       {
       "error":"Some error message"
       }
