import requests

if __name__ == '__main__':
    headers = {
        "Content-Type": 'application/json',
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MDg5NTI3NSwianRpIjoiZWNhNWZlOWUtYzM3Yi00NDI2LTgwYjktMDNiZjFkMzNlMWQ1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjgzNDZhMjQ2LWUzYjQtNDU0ZC1hMDRhLTI5NzJiZTQyMDcyMiIsIm5iZiI6MTY4MDg5NTI3NX0.xAMGOg3ymsuqvIIbBCtHtczZ4GzRf7Mc7Bal9TjQdQ8"
    }
    json_data = {"group_name": "testing 5","group_currency":"USD","participants":["curl@gmail.com"]}
    json_data_1 = {"group_name": "testing 6","group_currency":"USD","participants":["curl@gmail.com"]}
    res = requests.post("http://127.0.0.1:5004/group/register",headers=headers,json=json_data)
    res2 = requests.post("http://127.0.0.1:5004/group/register",headers=headers,json=json_data_1)

    # json_data_2 = {"group_id": "9e448351-bd60-11ed-82b0-2556c802de4f","email":"curl@gmail.com", "amount": 123.43423}