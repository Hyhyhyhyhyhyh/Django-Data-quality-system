from django.test import TestCase
import requests

url = "http://localhost:8000/api/demand_list"
response = requests.get(url=url,params={'company':'信托'})


url = "http://localhost:8000/api/demand_list"
response = requests.get(url=url,params={'company':'信托'})