# EMAT   

## Technology Stack

This project is a mobile app built on React Native with its backend being served using a combination of Python, Flask & MongoDB

### Languages Used:
1. Javascript
2. Python

## Dependencies & Deployment

### Backend:
1. Make sure python is installed on your machine (Python version 3.9 or later)
2. If you are planning to use a local MongoDB instance, set the MONGODB_SETTINGS configuration accordingly in app.py
3. Go to backend/ directory after cloning this project
4. Create a Python Virtual Environment ```python -m venv ENV_NAME```
5. Activate the virtual environment
6. After the virtual environment is activated, Run ```pip install -r requirements.txt```
7. Run ```python app.py```
8. By default, the app runs on port 5004

### Frontend:

1. Install node if not exists on your machine (the LTS version)
2. Run ```npm i -g expo-cli```
3. Go to client/ directory 
4. Run ```npm i``` to install project dependencies`
5. Change the base URL inside the axios.js somewhere under the client/ directory ```http://IP_ADDRESS:PORT``` (Note: this should be the same IP address where your backend is running)
6. Run ```npm start```

## User Scenarios

1. User Specific:

| User Scenarios      | Status      |
| ------------------- | ----------- |
| Login & Sign-up               | Done       |
| Users will be able to connect with other users using  email.           | Done        |
| Users will be able to add the expense among the group & also be able to clear their borrowings.           | Done        |
| User can set their monthly budget as the limit.         | Done        |
| Users will get notifications/warning popups when their monthly spending will go close to their limit.           | In Progress        |
| User can check their statistical spending data using graphs. (Optional part of next phase)          | In Progress        |
| User can set their base currency.           | Done        |


2. Group Specific:

| User Scenarios      | Status      |
| ------------------- | ----------- |
| A temporary group can be formed that will be deleted after a particular date or when all the payments within members are cleared.               | In Progress       |
| Functionality to send the payment notification to all the members of the group by a user. (It will send a notification to clear the payment to members of the group who didn’t clear their payment).           | Done        |
| The group can show the name of the user who has spent the most amount in the group expenses and the user that has the most due remaining.           | Done        |
| The group will also have its base currency and if any user’s base currency is different from the group currency, then that user will be able to see the due amount in both currencies.         | In Progress        |

## Code Smells - Initial

There were a total of 111 smells ranging on CRITICAL, MAJOR & MINOR severity levels, out of which 93 of them were based on our code, and the remaining were located under tests/ folder for the entire backend

| Severity Level      | Count      |
| ------------------- | ---------- |
| CRITICAL | 14 |
| MAJOR | 50 |
| MINOR | 30 |

## Code Smells - Refactoring

There were a total of 33 smells ranging on CRITICAL, MAJOR & MINOR severity levels, out of which 16 of them were based on our code, and the remaining were located under tests/ folder for the entire backend

| Severity Level      | Count      |
| ------------------- | ---------- |
| CRITICAL | 10 |
| MAJOR | 6 |


## Test Coverage 

We have a total of 26 test cases and a total code coverage of around 80 - 85 %

## Contributions

| Student name      | Contributions      |
| ------------------- | ---------- |
| Ishan Sharma | Backend- Expense,Group,Code smells,Refactoring,Front-End Integration |
| Deep Lad | Front-End App Setup,Group Expenses Settle Up,API Integration,Refactoring,navigating Design Aspects |
| Shubh Patel | Front-End Pages Design And Integration-Login,Register,Forgot Password,Logout,User Profile,Charts,Activites |
| Jiaye Tang | Backend-Authentication,User Profile,Test Cases. |
| Nitesh Kumar | Backend-Pipeline,Test Cases,Expense Api |


