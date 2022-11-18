from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from schemas.student import Student
from config.db import con
from models.index import students
app = FastAPI()



# root@localhost:3306
@app.get("/")
def hello():
    return FileResponse('index.html')

@app.get('/api/students')
async def index():
    return {"hello": "world"}

@app.post('/api/students')
async def stroe(student:Student):
    data = con.execute(students.insert().values(
        name=student.name,
        email=student.email,
        age=student.age,
        country=student.country,
    ))
    if data.is_insert:
        return {
            "success": True,
            "msg": "Student store Successfully"
        }
    else:
        return {
            "success": False,
            "msg": "something wrong with you"
        }
 


@app.get("/data")
def data():
    return {'data': 1234}


class send_data(BaseModel):
    name : str
    phone : int

@app.post("/send")
def send(data: send_data):
    print(data)
    return {'data': 'done'}


@app.put('/api/students/{id}')
async def edit(id:int):
    data=con.execute(students.select().where(students.c.id==id)).fetchall()
    return {
            "success": True,
            "data": data
        }

@app.patch('/api/students/{id}')
async def update(id:int, student:Student):
    data=con.execute(students.update().values(
        name=student.name,
        email=student.email,
        age=student.age,
        country=student.country,
    ).where(students.c.id==id))

    if data:
        return {
            "success": True,
            "msg": "Student update Successfully"
        }
    else:
        return {
            "success": False,
            "msg": "something wrong with you"
        }

@app.delete('/api/students/{id}')
async def delete(id:int):
    data=con.execute(students.delete().where(students.c.id==id))
    if data:
        return {
            "success": True,
            "msg": "Student Delete Successfully"
        }
    else:
        return {
            "success": False,
            "msg": "something wrong with you"
        }
@app.get('/api/students/{search}')
async def search(search):
    data=con.execute(students.select().where(students.c.name.like('%'+search+'%'))).fetchall()
    return {
            "success": True,
            "data": data
        }