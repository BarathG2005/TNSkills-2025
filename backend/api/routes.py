from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from config.database import get_db
import csv
from datetime import datetime, date
from typing import List, Dict, Any
import io
from config.database import get_db


vehicle ={1,2,1,3,2,1,}

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
    cleaned_data = []
    dirty_data = []
    
    for row in reader:
        try:
           id  = int(row["VehcileID"])
           driver = row["Driver"]
           date = datetime.strptime(row["Date"].strip(), "%Y-%m-%d").date()
           odmeter = int(row["Odometer_Reading"])
           distance = int(row["Trip_Distance"])
           if id not in vehicle:
            continue
           cleaned_data.append((id,driver,date.today().data,distance))           
        except (ValueError, KeyError) as e:
            dirty_data.append({
                "VehcileID": row.get("VehcileID", "N/A"),
                "Date": row.get("Date", "N/A"),
                "Odometer_Reading": row.get("Odometer_Reading", "N/A"),
                " distance": row.get(" distance", "N/A"),
                "reason": f"Parsing error: {str(e)}"
            })
            continue
        if not cleaned_data:
            return {
                "inserted_data": [],
                "dirty_data": dirty_data,
                "message": "No valid rows found to insert"
            }
        cursor = db.cursor()
        sql = "INSERT INTO Trips (TripID, VehicleID,  DriverName,StartDate,EndDate,DistanceKm) VALUES (%s, %s, %s)"
        try:
            cursor.excutemany(sql,cleaned_data)
            db.commit()
            inserted_count = cursor.rowcount
            inserted_data = [
            {
                "order_id": row[0],
                "order_date": str(row[1]),
                "price": row[2]
            }
            for row in cleaned_data
            ]
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database Insert Failed: {str(e)}")
        finally:
            cursor.close()
            db.close()

        return {
            "inserted_data": inserted_data,
            "dirty_data": dirty_data,
            "inserted_count": inserted_count,
            "dirty_count": len(dirty_data)
        }