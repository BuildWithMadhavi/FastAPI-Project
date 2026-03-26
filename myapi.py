from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1:{
        "name": "Madhu", 
        "age": 25, 
        "year":18
    }, 
    2: {
        "name": "John", 
        "age": 22, 
        "year": 20}
}

class Student(BaseModel):
    name : str
    age : int
    year : int

class UpdateStudent(BaseModel):
    name : Optional[str] = None
    age : Optional[int] = None
    year : Optional[int] = None

@app.get("/")
def index():
    return {"Message": "Hello, Madhu! you can do it" }

# we can also use the path parameter to get the student by id, but in this case we need to provide the id parameter in the path and we need to make sure that the id parameter is unique, otherwise it will return the first student with that id.
@app.get("/get-student/{student_id}")
def get_student(student_id : int = Path(description="The ID of the student to view")):
    if student_id in students:
        return students[student_id]
    else:
        return {"Error": "Student not found"}
   
@app.get("/get-by-name")
def get_student(*, name:Optional[str] = None, test : int): # we are using optional because we want to make the name parameter optional, if we don't provide the name parameter then it will return all the students.
# * is used to indicate that all the parameters after it are keyword only parameters, which means that they can only be passed as keyword arguments and not as positional arguments. This is useful when we want to make sure that the parameters are passed in a specific order or when we want to make sure that the parameters are passed with a specific name. In this case, we want to make sure that the name parameter is passed with the name "name" and not as a positional argument.
# test parameter is used to test the optional parameter, if we don't provide the name parameter then it will return all the students, but if we provide the name parameter then it will return the student with that name.
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]       
    return {"Data": "Not found"}

# we can also use the path parameter to get the student by name, but in this case we need to provide the name parameter in the path and we need to make sure that the name parameter is unique, otherwise it will return the first student with that name.
@app.get("/get-by-name/{student_id}")
def get_student(*, student_id: int, name:Optional[str] = None, test: int):
    for student_id in students:
        if students[student_id][name] == name:
            return students[student_id]       
    return {"Data": "Not found"}


@app.post("/crate-student/{student_id}")
def create_student(student_id : int, student : Student ):
    if student_id in students:
        return {"Error": "Student exists"}
    
    students[student_id] = student 
    return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id : int, student : UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    
    if student.name != None:
        students[student_id].name = student.name
    
    if student.age != None:
        students[student_id].age = student.age
    
    if student.year != None:
        students[student_id].year = student.year
    
    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id : int):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    
    del students[student_id]
    return {"Message": "Student deleted successfully"}
