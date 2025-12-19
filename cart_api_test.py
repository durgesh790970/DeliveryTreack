import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE','durgesh.settings')
django.setup()

from django.test import Client

c = Client()
print('Posting add-to-cart...')
r = c.post('/api/cart/', data=json.dumps({'action':'add','name':'Automated Test Item','price':199,'qty':1}), content_type='application/json')
print('POST status:', r.status_code)
print('POST response:', r.content.decode('utf-8'))

r2 = c.get('/api/cart/')
print('GET status:', r2.status_code)
print('GET response:', r2.content.decode('utf-8'))

# Try checkout
print('Attempting checkout...')
r3 = c.post('/api/cart/checkout/')
print('CHECKOUT status:', r3.status_code)
print('CHECKOUT response:', r3.content.decode('utf-8'))

r4 = c.get('/api/cart/')
print('POST-checkout GET status:', r4.status_code)
print('POST-checkout GET response:', r4.content.decode('utf-8'))
