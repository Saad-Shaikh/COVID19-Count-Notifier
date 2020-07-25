# DailyCOVID19Count
A script that fetches the latest Covid counts for the requested *Indian* cities and mails it to the people in the mail list.  
Data is fetched using [COVID19-India API](https://api.covid19india.org/).

## Requirements
* [Python3](https://www.python.org/downloads/)
* Requests ```pip3 install requests```
* Schedule ```pip3 install schedule```
* [Less Secure App Access](https://myaccount.google.com/lesssecureapps) enabled for the sender's Gmail account (required only if you are not using App Passwords)

## How To Use:
* In *credentials.py*, add your(sender's) email id and password, preferably a separate [App Password](https://myaccount.google.com/apppasswords) so you don't have to enable *Less Secure App Access*.
```python
login_email = 'loginemail'
login_pass = 'loginpassword'
```
* In *details.py*, edit *states_and_cities*
```python
states_and_cities = [
        {'state': 'state1', 'cities': ['city1', 'city2']},
        {'state': 'state2', 'cities': ['city3']},
    ]
```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; and *email_list* to add recipients
```python
email_list = [
    {'email': 'recipientemail1', 'states': ['requestedstate1'], 'cities': ['requestedcity1', 'requestedcity2']},
    {'email': 'recipientemail2', 'states': ['requestedstate1', 'requestedstate2'], 'cities': ['requestedcity1', 'requestedcity3']},
]
```
* Run *python3 db_operations.py* to create the database. **Only needs to be done once**.
* Run *python3 main.py*
---
