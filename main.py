from typing import Union

from fastapi import FastAPI, Request

from func.funcs import find_consecutive_slots

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/availability")
async def traer_horarios(request: Request):
    datos = await request.json()
    if "available_times" not in datos or "busy_start_times" not in datos or "busy_end_times" not in datos:
        return {"error": "Faltan campos requeridos"}
    horario = datos["available_times"]
    inicio_del_turno = datos["busy_start_times"]
    fin_del_turno = datos["busy_end_times"]

    return find_consecutive_slots(horario, inicio_del_turno, fin_del_turno)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

#dowload fastapi: pip install "fastapi[standard]"
#start the server: fastapi dev main.py