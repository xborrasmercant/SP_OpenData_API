from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

distritoDict = {}

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/showinfo")
async def showinfo(request: Request):

    distritoDict = fetchData()

    distritos = list(distritoDict.keys())
    return templates.TemplateResponse("showinfo.html", {"request": request, "distritos": distritos})

@app.get("/api/barrios/{distrito}")
async def obtener_barrios(distrito: str):

    barrioDict = list(distritoDict.get(distrito, {}).keys())
    return {"barrioDict": barrioDict}


@app.post("/submit_form")
async def handle_form_submission(district: str = Form(...), neighborhood: str = Form(...)):

    pobTotal = distritoDict[district][neighborhood][0]
    hTotal = distritoDict[district][neighborhood][1]
    mTotal = distritoDict[district][neighborhood][2]

    return {"district": district, "neighborhood": neighborhood, "pobTotal": pobTotal, "hTotal": hTotal,"mTotal": mTotal}


@app.get("/api/neighborhoodData/{distrito}/{barrio}")
async def barrio_data(distrito: str, barrio: str):


    pobTotal = distritoDict[distrito][barrio][0]
    hTotal = distritoDict[distrito][barrio][1]
    mTotal = distritoDict[distrito][barrio][2]


    return {
        "pobTotal": pobTotal,
        "hTotal": hTotal,
        "mTotal": mTotal
    }

@app.get("/fetch-data")
async def fetch_data():
    dataUrl = "https://services1.arcgis.com/hcmP7kr0Cx3AcTJk/arcgis/rest/services/Poblacion_Sec_Censales_Tipo_02/FeatureServer/4/query?where=1%3D1&outFields=CUSEC,Barrio,Distrito,Población_Total,M_Total,H_total&outSR=4326&f=json"
    response = requests.get(dataUrl)

    if response.status_code == 200:
        data = response.json()
        features = data.get('features', [])

        extractInfo(features)
        printDistritoInfo(distritoDict)

        return {"message": "Data fetched and printed to console"}
    else:
        return {"message": "Failed to fetch data from the API"}

def extractInfo(features):
        for feature in features:
            attributes = feature.get('attributes', {})
            distrito = attributes.get('Distrito', 'Unknown')
            barrio = attributes.get('Barrio', 'Unknown')
            pobTotal = attributes.get('Población_Total', 'Unknown')
            MTotal = attributes.get('M_Total', 'Unknown')
            HTotal = attributes.get('H_total', 'Unknown')

            if distrito not in distritoDict:
                barrioDict = {}
                barrioDict[barrio] = [pobTotal, MTotal, HTotal]
                distritoDict[distrito] = barrioDict
            else:
                barrioDict = distritoDict[distrito]
                if barrio not in barrioDict:
                    barrioDict[barrio] = [pobTotal, MTotal, HTotal]
                else:
                    oldValues = barrioDict[barrio]
                    newPobTotal = oldValues[0] + pobTotal
                    newMTotal = oldValues[1] + MTotal
                    newHTotal = oldValues[2] + HTotal
                    barrioDict[barrio] = [newPobTotal, newMTotal, newHTotal]

        return distritoDict

def printDistritoInfo (distritoDict):
    for distritoKey, barrioDict in distritoDict.items():
            print()
            print("Distrito:", distritoKey)
            for barrio, values in barrioDict.items():
                print("| Barrio:", barrio)
                print("| | Población Total:", values[0])
                print("| | Mujeres Totales:", values[1])
                print("| | Hombres Totales:", values[2])
                print("| |")
            print("^ ^")

def fetchData():
    dataUrl = "https://services1.arcgis.com/hcmP7kr0Cx3AcTJk/arcgis/rest/services/Poblacion_Sec_Censales_Tipo_02/FeatureServer/4/query?where=1%3D1&outFields=CUSEC,Barrio,Distrito,Población_Total,M_Total,H_total&outSR=4326&f=json"
    response = requests.get(dataUrl)

    if response.status_code == 200:
        data = response.json()
        features = data.get('features', [])

        return extractInfo(features)


if __name__ == "__main__":
    print("-> Inicio integrado de servicio web")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
else:
    print("-> Iniciado desde el servidor web")
    print("   Módulo python iniciado:", __name__)