import io
import os
from pydantic import BaseModel
from PIL import Image
import numpy as np
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import pydicom
from pydicom import dcmread
from pydicom.pixel_data_handlers.util import apply_voi_lut


import google.generativeai as genai
from langchain_community.llms import Ollama
class PatientInfo(BaseModel):
    PatientName: str
    PatientID: str
    PatientBirthDate: str
    PatientSex: str
    StudyDate: str
    StudyDescription: str
    ReferringPhysicianName: str
class PatientInfoPayload(BaseModel):
    patient_info: PatientInfo

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.post("/convert/")
async def convert_dcm_to_jpg(file: UploadFile = File(...)):

    contents = await file.read()
    dcm = dcmread(io.BytesIO(contents))


    data = apply_voi_lut(dcm.pixel_array, dcm)

    if data.max() > 255:
        data = (data / data.max()) * 255

    data = data.astype(np.uint8)

    image = Image.fromarray(data)

    image_io = io.BytesIO()
    image.save(image_io, format='JPEG')
    image_io.seek(0)

    temp_file = "temp.jpg"
    with open(temp_file, "wb") as f:
        f.write(image_io.read())

    return FileResponse(temp_file, media_type="image/jpeg")



@app.post("/extract-patient-info/")
async def extract_patient_info(file: UploadFile = File(...)):
    try:

        ds = pydicom.dcmread(file.file)

        # Extract patient information
        patient_info = {
            "PatientName": str(ds.get("PatientName", "N/A")),
            "PatientID": str(ds.get("PatientID", "N/A")),
            "PatientBirthDate": str(ds.get("PatientBirthDate", "N/A")),
            "PatientAge": str(ds.get("PatientAge", "N/A")),
            "PatientSex": str(ds.get("PatientSex", "N/A")),
            "StudyDate": str(ds.get("StudyDate", "N/A")),
            "Modality": str(ds.get("Modality", "N/A")),
            "StudyDescription": str(ds.get("StudyDescription", "N/A")),
            "ReferringPhysicianName": str(ds.get("ReferringPhysicianName", "N/A")),
        }

        return JSONResponse(content={"patient_info": patient_info})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

base_path = Path(__file__).parent
os.environ['GOOGLE_API_KEY'] = base_path.joinpath('gemini-api-key.txt').read_text().strip()

@app.post("/get-patient-summary/")
async def get_patient_summary(payload: PatientInfoPayload):
    try:
        patient_info = payload.patient_info

        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

        # Create a prompt with the patient information
        prompt = (
            f"Generate a detailed patient summary for the following details:\n\n"
            f"Name: {patient_info.PatientName}\n"
            f"ID: {patient_info.PatientID}\n"
            f"Birth Date: {patient_info.PatientBirthDate}\n"
            f"Sex: {patient_info.PatientSex}\n"
            f"Study Date: {patient_info.StudyDate}\n"
            f"Study Description: {patient_info.StudyDescription}\n"
            f"Referring Physician: {patient_info.ReferringPhysicianName}\n\n"
            f"Please provide a comprehensive summary in text format."
        )

        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt], safety_settings={'HATE_SPEECH': 'block_none'})

        return JSONResponse(content={"patient_summary": response.text})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/get-patient-summary-locally/")
async def get_patient_summary_locally(payload: PatientInfoPayload):
    try:
        patient_info = payload.patient_info
        # Create a prompt with the patient information
        prompt = (
            f"Generate a detailed patient summary for the following details:\n\n"
            f"Name: {patient_info.PatientName}\n"
            f"ID: {patient_info.PatientID}\n"
            f"Birth Date: {patient_info.PatientBirthDate}\n"
            f"Sex: {patient_info.PatientSex}\n"
            f"Study Date: {patient_info.StudyDate}\n"
            f"Study Description: {patient_info.StudyDescription}\n"
            f"Referring Physician: {patient_info.ReferringPhysicianName}\n\n"
            f"Please provide a short summary in text format less than 150 words."
        )

        model = Ollama(model="llama2")
        response = model.invoke(prompt)

        return JSONResponse(content={"patient_summary": response})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))