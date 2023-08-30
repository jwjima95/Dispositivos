import requests

url = 'http://127.0.0.1:5000/process'

files = {
    'pdf1': open('elprincipito1.pdf', 'rb'),
    'pdf2': open('elprincipito2.pdf', 'rb')
}
data = {'question': 'nombre de los personajes'}

response = requests.post(url, files=files, data=data)

if response.status_code == 200:
    result = response.json()
    print('Respuesta:', result['answer'])
else:
    print('Error:', response.text)
