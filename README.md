# HACKATHON: FLEET MANAGEMENT SOLUTIONS

**Theme:** Fleet Management with Conflict Detection & Maintenance Prediction  
**Duration:** 6 Hours

---

## SECTION 1: DATABASE ARCHITECTURE (30 Marks)

**Task:** Design a schema for tracking vehicle health.

1.  **Table: Vehicles**
    * `VehicleID` (PK, String/Varchar)
    * `RegNo` (String)
    * `Type` (String: Truck, Van, Car)
    * `LastServiceDate` (Date)
    * `CurrentOdometer` (Long/BigInt - Tracks total lifetime distance)
    * `LastServiceOdometer` (Long/BigInt)

2.  **Table: Trips**
    * `TripID` (PK, Auto-increment)
    * `VehicleID` (FK)
    * `DriverName` (String)
    * `StartDate` (Date)
    * `EndDate` (Date)
    * `DistanceKm` (Long/BigInt)

3.  **Table: Maintenance_Alerts**
    * `AlertID` (PK, Auto-increment)
    * `VehicleID` (FK)
    * `AlertDate` (Date)
    * `Reason` (String, e.g., "Odometer Limit Exceeded")

4.  **Table: Service_History**
    * `ServiceID` (PK, Auto-increment)
    * `VehicleID` (FK)
    * `ServiceDate` (Date)
    * `OdometerReading` (Long/BigInt)
    * `Notes` (String - Optional description)

---

## SECTION 2: APPLICATION DEVELOPMENT (70 Marks)

> **IMPORTANT ASSUMPTION:**
> For all logic involving "Today" or "Current Date" (e.g., availability checks, maintenance aging), **use the fixed date: 19th December 2025**. Do not use your computer's actual system date.

### MODULE A: THE "DIRTY" DATA CLEANUP (Complex Parsing)

**Input:** `driver_logs_raw.csv` (See Section 4)

**Data Challenges:**
1.  **Date Chaos:** The file contains four different date formats:
    * `dd-MM-yyyy` (e.g., 12-12-2025)
    * `yyyy/MM/dd` (e.g., 2025/12/13)
    * `yyyy-MM-dd` (e.g., 2025-12-16)
    * `dd/MMM/yyyy` (e.g., 15/Dec/2025)
2.  **Corrupt Data:** Some rows contain text (e.g., "CORRUPT_DATA") in numeric fields.

**Processing Logic:**
1.  **Parse Dates:** Normalize all dates into a standard SQL format. Treat these logs as Single-Day Trips (Set `Trip.StartDate` = `Trip.EndDate` = CSV Date).
2.  **Sanitize:** Skip any row where the **Odometer** OR **Trip_Distance** is non-numeric, or if the Date parsing fails.
3.  **State Update (The "High-Water Mark" Rule):**
    * Insert valid rows into the `Trips` table.
    * Update the `Vehicles` table: Set `CurrentOdometer` = `CSV Odometer_Reading` **ONLY IF** the CSV value is greater than the existing value in the database. (This prevents data regression if logs are processed out of order).

### MODULE B: THE BOOKING MANAGER (Algorithms & UX)

**UI Requirement:** A "New Trip" Booking Dashboard.

**Logic 1: Smart Availability & Conflict Detection**
* **User Interaction:** User selects a Date Range (Start to End) and clicks "Find Available Vehicles".
* **Algorithm:** Return a list of vehicles that have **NO overlaps** with existing trips.
* **Constraints:** You must handle all overlap edge cases:
    * New trip is strictly inside an existing trip.
    * New trip encompasses (surrounds) an existing trip.
    * New trip overlaps the start or end of an existing trip.
* **Validation:** If the user manually inputs a Vehicle ID that is busy, block the booking and show an error.
* **Test Case:**
    * *Pre-requisite:* Vehicle **V1** has a trip from **Dec 20** to **Dec 30** (See Seed Data).
    * *Action:* Search for availability from **Dec 24** to **Dec 26**.
    * *Result:* **V1** must **NOT** appear in the available list.

**Logic 2: Maintenance Predictor**
On application startup, run a background check to flag at-risk vehicles.
* **Rule:** A vehicle needs maintenance IF:
    ` (Current Date - LastServiceDate > 180 Days) OR (CurrentOdometer - LastServiceOdometer > 10,000 Km) `
    *(Note: Use 19 Dec 2025 as Current Date)*
* **Action:** Insert a record into `Maintenance_Alerts` for any vehicle meeting these criteria.

**Logic 3: "Close the Loop" (Service Workflow)**
The system must allow mechanics to resolve maintenance alerts.
1.  **UI:** Add a "Perform Service" button next to any active alert.
2.  **Action:** When clicked, execute a transaction:
    * **Archive:** Insert record into `Service_History` (Date = 19 Dec 2025, Odometer = Current).
    * **Reset:** Update `Vehicles` table (Set `LastServiceDate` = 19 Dec 2025, `LastServiceOdometer` = Current Total Distance).
    * **Clear:** Remove the flag from `Maintenance_Alerts`.

### MODULE C: VISUAL REPORTING

1.  **Chart:** A Pie Chart showing "Fleet Status" (Available vs On Trip vs In Maintenance).
    * *Priority Order (Mutually Exclusive):*
        1.  In Maintenance (Active Alert exists) -> **Red Slice**
        2.  On Trip (Current Date [19 Dec] is inside a Trip Duration) -> **Yellow Slice**
        3.  Available (Idle) -> **Green Slice**

2.  **PDF Report:** "Vehicle Health Card"
    * One page per vehicle.
    * List the last 5 trips.
    * **Conditional Formatting:** If the vehicle has an active Maintenance Alert, print "WARNING: SERVICE REQUIRED" in **Bold Red** text.

---

## SECTION 3: TECHNICAL GUIDELINES

1.  **Allowed Technology Stacks (Choose One):**
    * **Option A:** Java Desktop (Java 11+, JavaFX/Swing, SQLite/H2/Derby)
    * **Option B:** .NET/C# (WinForms/WPF, SQLite/LocalDB)
    * **Option C:** Java Web (Spring Boot/Servlets, HTML/CSS/JS, H2/SQLite)

2.  **Constraints:**
    * **CSV Parsing:** Do **not** use external libraries (like OpenCSV). Use native String splitting/parsing.
    * **PDF Generation:** External libraries allowed (iText, PDFBox, etc.).
    * **Database:** The DB file must be created automatically or included in submission.

3.  **Submission:**
    * Include a `README.txt` with build instructions.
    * Submit the project folder (exclude `target`/`bin`/`obj`/`node_modules`).

---

## SECTION 4: SAMPLE DATA

### PART 1: INITIAL DATABASE SEED
**CRITICAL:** You must populate your database with this data **BEFORE** processing any CSV logs. This establishes the baseline state.

**Table: Vehicles**

| VehicleID | RegNo | Type | LastServiceDate | CurrentOdometer | LastServiceOdometer |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **V1** | REG-001 | Truck | 2025-05-20 | 20,000 | 10,000 |
| **V_001** | REG-101 | Van | 2025-10-01 | 50,400 | 40,400 |
| **V_002** | REG-102 | Car | 2025-11-15 | 12,050 | 10,000 |
| **V_003** | REG-103 | Van | 2025-08-20 | 8,200 | 2,000 |

* *Hint: V1 LastServiceDate (May 20) is > 180 days from Current Date (Dec 19).*

**Table: Trips (Existing Bookings)**

| TripID | VehicleID | DriverName | StartDate | EndDate | DistanceKm |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **V1** | TestDriver | 2025-12-20 | 2025-12-30 | 500 |

---

### PART 2: CSV INPUT FILE
Create a file named `driver_logs_raw.csv` with the following content:

```csv
VehicleID,Driver,Date,Odometer_Reading,Trip_Distance
V_001,Ramesh,12-12-2025,50550,150
V_002,Sita,2025/12/13,12100,50
V_001,Ramesh,14-12-2025,50600,CORRUPT_DATA
V_003,Akbar,15/Dec/2025,8400,200
V_002,Sita,2025-12-16,12150,50
V_001,Ramesh,18-12-2025,50750,150
