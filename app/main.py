# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import onnxruntime as ort
import numpy as np

app = FastAPI()

model_path = "with_least_rmse.onnx"
session = ort.InferenceSession(model_path)

class InputData(BaseModel):
    gender_F: int
    gender_M: int
    occupation_administrator: int
    occupation_artist: int
    occupation_doctor: int
    occupation_educator: int
    occupation_engineer: int
    occupation_entertainment: int
    occupation_executive: int
    occupation_healthcare: int
    occupation_homemaker: int
    occupation_lawyer: int
    occupation_librarian: int
    occupation_marketing: int
    occupation_none: int
    occupation_other: int
    occupation_programmer: int
    occupation_retired: int
    occupation_salesman: int
    occupation_scientist: int
    occupation_student: int
    occupation_technician: int
    occupation_writer: int
    genre_1: int
    genre_2: int
    genre_3: int
    genre_4: int
    genre_5: int
    genre_6: int
    genre_7: int
    genre_8: int
    genre_9: int
    genre_10: int
    genre_11: int
    genre_12: int
    genre_13: int
    genre_14: int
    genre_15: int
    genre_16: int
    genre_17: int
    genre_18: int
    genre_19: int
    age_age1: int
    age_age2: int
    age_age3: int
    age_age4: int


def validate_input(data: InputData):
    gender_count = data.gender_F + data.gender_M
    if gender_count != 1:
        raise HTTPException(status_code=400, detail="Exactly one gender should be 1, others should be 0")

    occupation_count = sum([
        data.occupation_administrator, data.occupation_artist, data.occupation_doctor, data.occupation_educator, 
        data.occupation_engineer, data.occupation_entertainment, data.occupation_executive, data.occupation_healthcare, 
        data.occupation_homemaker, data.occupation_lawyer, data.occupation_librarian, data.occupation_marketing, 
        data.occupation_none, data.occupation_other, data.occupation_programmer, data.occupation_retired, 
        data.occupation_salesman, data.occupation_scientist, data.occupation_student, data.occupation_technician, 
        data.occupation_writer
    ])
    if occupation_count != 1:
        raise HTTPException(status_code=400, detail="Exactly one occupation should be 1, others should be 0")

    age_count = data.age_age1 + data.age_age2 + data.age_age3 + data.age_age4
    if age_count != 1:
        raise HTTPException(status_code=400, detail="Exactly one age group should be 1, others should be 0")
    
@app.post("/predict/")
async def predict(data: InputData):
    validate_input(data)
    input_array = np.array([[data.gender_F, data.gender_M,
                             data.occupation_administrator, data.occupation_artist, data.occupation_doctor,
                             data.occupation_educator, data.occupation_engineer, data.occupation_entertainment,
                             data.occupation_executive, data.occupation_healthcare, data.occupation_homemaker,
                             data.occupation_lawyer, data.occupation_librarian, data.occupation_marketing,
                             data.occupation_none, data.occupation_other, data.occupation_programmer,
                             data.occupation_retired, data.occupation_salesman, data.occupation_scientist,
                             data.occupation_student, data.occupation_technician, data.occupation_writer,
                              data.genre_1, data.genre_2, data.genre_3, data.genre_4, data.genre_5, data.genre_6,
                               data.genre_7, data.genre_8, data.genre_9, data.genre_10, data.genre_11, data.genre_12,
                                data.genre_13, data.genre_14, data.genre_15, data.genre_16, data.genre_17, data.genre_18,data.genre_19,
                             data.age_age1, data.age_age2, data.age_age3, data.age_age4]], dtype=np.float32)

    inputs = {session.get_inputs()[0].name: input_array}
    output = session.run(None, inputs)
   
    prediction = output[0].tolist()
    return {"predicted_rating": prediction}
