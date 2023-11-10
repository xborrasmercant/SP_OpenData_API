from fastapi import FastAPI
import requests
import uvicorn

app = FastAPI()

@app.get("/fetch-data")
async def fetch_data():
    dataUrl = "https://services5.arcgis.com/UxADft6QPcvFyDU1/arcgis/rest/services/WebMapOOGG/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"
    response = requests.get(dataUrl)

    if response.status_code == 200:

        print()
        print("=========================================================")
        print("Oficinas de gestión Tarjeta Transporte Público de Madrid")
        print("=========================================================")
        print()


        data = response.json()
    
        officeArray = data.get('features', [])

        # Print the list of features
        for office in officeArray:
            officeAttributes = office.get('attributes', {})
            officeName = officeAttributes.get('Name', 'Unknown Station')
            officeInfo = officeAttributes.get('PopupInfo', 'No Popup Info Available')

            print("Oficina: " + officeName)
            print("Información: " + officeInfo)

            print()            
    
        print("=========================================================")
        print()
        return {"message": "Data fetched and printed to console"}
    else:
        return {"message": "Failed to fetch data from the API"}

if __name__ == "__main__":
    print("-> Inicio integrado de servicio web")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload="True")

    
else:
    print("-> Iniciado desde el servidor web")
    print("   Módulo python iniciado:", __name__)