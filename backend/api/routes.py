from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from config.database import get_db
import csv
from datetime import datetime, date
from typing import List, Dict, Any
import io
from config.database import get_db


valid_orders = {101, 102, 103, 104, 105, 106, 107}

@app.post("/upload-drivers")
async def show_all(file: UploadFile = File(...), db = Depends(get_db())
):
    if not file:
        raise HTTPException(status_code=400, detail="file is required")
    
    try:
        content = await file.read()
        csv_text = content.decode("utf-8")
        csv_file = io.StringIO(csv_text)
        reader = csv.DictReader(csv_file)
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to read CSV file")

    today = date("2025-12-19")
    rows_to_insert = []
    
    for row in reader:
        try:
           if type(row) == len:
               continue
           
        except (ValueError, KeyError) as e:
            continue
        