import requests

text = "I Love you so much you are amazing"
url = "http://0.0.0.0:8000/predict"
data = {"text": text}

x = requests.post(url, json=data)

print(x.text)
