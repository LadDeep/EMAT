#This API calculates the total amount and divides it equally
# to the number of users. Further, the variable amount and amount owed
# by individuals will be calculated and displayed.

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/settleUp', method = ['POST'])

#function to calculate expense and total users in a group
 def netAmount():

    expenses = request.json.get('expenses')
    group = request.json.get('group')

    # total expense
    totalExpense = sum(expenses.values())

    # no of users in a group

    totalUsers = len(group)

    # amount owed by individual user
    netAmounts = = {}
    for user in group:
        if user in expenses:
            netAmounts[user] = expenses[user] - (totalExpense / totalUsers)

        else:
            netAmount[user] = -(totalExpense / totalUsers) 