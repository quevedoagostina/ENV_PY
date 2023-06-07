import requests
from flask import Flask, render_template, request

app = Flask(__name__, static_folder='static')
 
BASE_URL = 'https://apis.datos.gob.ar/georef/api/'

@app.route('/', methods =['POST', 'GET'])
def index():
    if request.method == 'POST':
        print(request.form['nombre'])
    else:
        print("HICE UNA PETICIÓN GET")
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    password = request.form['password']
    tipo_usuario = request.form['tipo_usuario']
    return (f"<h1>Apriete el botón submit y recibí el {usuario}"
        f"Y la contraseña {password}"
        f"El tipo de usuario es {tipo_usuario} </h1>"
    )
    

@app.route('/provincias')
def obtener_todas_provincias():
    response = requests.get(f"{BASE_URL}provincias")
    data = response.json()
    cantidad = data.get('cantidad')
    provincias = data.get('provincias')
    return render_template(
        'provincias.html',
        cant_prov=cantidad,
        provs=provincias,
        )

@app.route('/provincias/<id>/municipios')
def municipios_por_provincia(id):
    # Obtener los municipios de la provincia desde la API
    response = requests.get(
        f"https://apis.datos.gob.ar/georef/api/localidades?provincia={id}"
    )
    data = response.json()
    cantidad = data.get('cantidad')
    municipios = data.get('localidades')

    # Obtener el nombre de la provincia correspondiente
    response = requests.get(f"{BASE_URL}provincias/{id}")
    data = response.json()
    
    # Renderizar la plantilla municipios.html con los datos de la provincia y los municipios
    return render_template(
        'municipios.html',
        cant_municipios=cantidad,
        municipios=municipios
    )

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/sobrenosotros')
def sobrenosotros():
    return render_template('sobrenosotros.html')

