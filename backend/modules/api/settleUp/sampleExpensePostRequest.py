import requests

expenses = {'user1': 10, 'user2': 20, 'user3': 15, 'user4': 30}
group = ['user1', 'user2', 'user3', 'user4', 'user5']

response = requests.post('http://localhost:5000/settleUp', json={'expenses': expenses, 'group': group})
result = response.json()

netAmounts = result['netAmounts']
isZero = result['isZero']

print(netAmounts)
print(isZero)
