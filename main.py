import random
from datetime import datetime, tzinfo
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()



class IntrebareModel(BaseModel):
    id:int 
    enunt:str
    variante_de_raspuns:str
    raspuns_Corect:str

class Rezultat(BaseModel):
    nume:str
    prenume:str
    puctaj:int
    data_predari:datetime

db_intrebari = [IntrebareModel(id=3,enunt="Intrebarea 1",variante_de_raspuns="A,b,c,d",raspuns_Corect="A"),
                IntrebareModel(id=2,enunt="Intrebarea 2",variante_de_raspuns="A,b,c,d",raspuns_Corect="B"),
                IntrebareModel(id=23,enunt="Intrebarea 3",variante_de_raspuns="A,b,c,d",raspuns_Corect="B"),
                IntrebareModel(id=1,enunt="Intrebarea 4",variante_de_raspuns="A,b,c,d",raspuns_Corect="D")]
db_test = []
db_rezultate = []


@app.get("/intrebari")
def arata_intrebarile():
    return db_intrebari

@app.post("/intrebari")
def introducere_intrebare(intrebare:IntrebareModel):
    db_intrebari.append(intrebare)
    return{"mesaj:":"Intrebarea a fost adaugata"}

@app.delete("/intrebari/{id}")
def arata_intrebarile(id:int):
    for intrebare in db_intrebari:
        if(intrebare.id == id):
            db_intrebari.remove(intrebare)
            return {"mesaj:":"Intrebarea a fost stearsa"}
    raise HTTPException(status_code=404,detail=f"Intrebarea cu id {id} nu a fost gasita")


@app.post("/test")
async def genereaza_test(nrIntrebari:int):
    for i in range(nrIntrebari):
        index = random.randint(0,len(db_intrebari)-1)
        db_test.append(db_intrebari[index])
    return{"mesaj:":"Testul a fost generat cu succes"}

@app.get("/test")
def distribuie_test():
    return db_test

@app.post("/rezultate")
def incarcarca_rezultat(rezultat_student:Rezultat):
    rezultat_student.data_predari = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return db_rezultate.append(rezultat_student)

@app.get("/rezultate")
def arata_rezultatele_sudentiilor():
    return db_rezultate

@app.delete("/rezultate")
def arata_rezultatele_sudentiilor():
    db_rezultate.clear()
    return {"mesaj:":"Rezultatele au fost sterse cu succes"}
