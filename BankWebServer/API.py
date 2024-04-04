import requests

url = 'http://127.0.0.1:5000'

banks = ['Alpha Bank', 'National Bank of Greece', 'Piraeus Bank', 'Eurobank', 'Viva']

# loop to create 5 banks
for bank in banks:
    response = requests.post(url + '/create', json={'name': bank, 'location': 'Greece'})

    if response.status_code == 200:
        print('Bank created successfully!')
    else:
        print('An error occurred while creating the bank!')

# read all banks
response = requests.get(url + '/read')

if response.status_code == 200:
    print(response.json())


# read a specific bank
response = requests.get(url + '/find/Viva')

if response.status_code == 200:
    print(response.json())

# update a bank
viva_id = response.json()['id']
viva_location = response.json()['location']
response = requests.put(url + '/update/' + str(viva_id), json={'name': 'Viva Wallet', 'location': viva_location})

if response.status_code == 200:
    print('Bank updated successfully!')

#delete a bank
response = requests.get(url + '/delete/' + str(viva_id))
if response.status_code == 200:
    print('Bank deleted successfully!')

