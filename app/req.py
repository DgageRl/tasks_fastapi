import requests

url = "http://195.161.41.49:8080/tasks"
data = {"name": "Новая задача", "description": "Тестовая"}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
