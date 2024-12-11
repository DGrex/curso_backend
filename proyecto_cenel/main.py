from fastapi import FastAPI
import requests

app = FastAPI()

BASE_URL = "https://api.cnelep.gob.ec/servicios-linea/v1/notificaciones/consultar"

@app.get("/consulta")
def consulta_datos(cedula: str, tipo_documento: str):
    """
    Endpoint para consumir la API y extraer parámetros específicos.
    """
    api_url = f"{BASE_URL}/{cedula}/{tipo_documento}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        # Procesar el JSON de la respuesta
        data = response.json()

        if data.get("resp") == "OK" and data.get("notificaciones"):
            notificacion = data["notificaciones"][0]  # Tomar la primera notificación
            detalle_planificacion = notificacion.get("detallePlanificacion", [])

            # Extraer los cortes específicos
            cortes_simplificados = [
                {
                    "fechaCorte": corte.get("fechaCorte"),
                    "horaDesde": corte.get("horaDesde"),
                    "horaHasta": corte.get("horaHasta"),
                    "comentario": corte.get("comentario"),
                }
                for corte in detalle_planificacion
            ]

            # Construir la respuesta filtrada
            filtered_data = {
                "cuentaContrato": notificacion.get("cuentaContrato"),
                "direccion": notificacion.get("direccion"),
                "cortes": cortes_simplificados,
            }
            return {"status": "success", "filtered_data": filtered_data}
        
        else:
            return {"status": "error", "message": "No se encontraron notificaciones válidas."}
    
    else:
        return {
            "status": "error",
            "message": f"Error al consultar la API: {response.status_code}",
            "details": response.text,
        }


