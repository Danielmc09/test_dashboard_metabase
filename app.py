from flask import Flask, render_template
import jwt
import time
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

app = Flask(__name__)

# Obtener variables del entorno
METABASE_SITE_URL = os.getenv("METABASE_SITE_URL")
METABASE_SECRET_KEY = os.getenv("METABASE_SECRET_KEY")
DASHBOARD_ID_15 = int(os.getenv("DASHBOARD_ID_15"))
DASHBOARD_ID_16 = int(os.getenv("DASHBOARD_ID_16"))

def generate_iframe_url(dashboard_id, project_manager_name="", project_name=""):
    # Crear el diccionario de params
    params = {}
    
    # Agregar parámetros si no están vacíos
    if project_manager_name:
        params["nombre_del_project_manager"] = project_manager_name
    if project_name:
        params["nombre_del_proyecto"] = project_name
    
    # Crear el payload
    payload = {
        "resource": {"dashboard": dashboard_id},
        "params": params,
        #"exp": round(time.time()) + (60 * 10)  # 10 minute expiration
    }
    
    # Generar el token
    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")
    iframe_url = f"{METABASE_SITE_URL}/embed/dashboard/{token}#bordered=true&titled=true"
    return iframe_url

@app.route('/')
def dashboard():
    # Ejemplo de valores para los parámetros
    project_manager_name = "Yolanda Gomez"
    project_name = ""
    
    # Generar URLs de los iframes con parámetros opcionales
    iframe_url_1 = generate_iframe_url(DASHBOARD_ID_15, project_manager_name, project_name)
    iframe_url_2 = generate_iframe_url(DASHBOARD_ID_16, project_manager_name)
    
    return render_template('dashboard.html', iframe_url_1=iframe_url_1, iframe_url_2=iframe_url_2)


if __name__ == '__main__':
    app.run(debug=True, port=5001)



