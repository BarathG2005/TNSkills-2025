create table Vehicles(
	VehicleID int primary key,
	RegNo varchar(200),
	Type varchar(200),
	LastServiceDate Date,
	CurrentOdometer long,
	LastServiceOdometer long
);

create table Trips(
	TripID int primary key ,
	VehicleID int ,
    DriverName varchar(200),
    StartDate date,
    EndDate date,
    DistanceKm long,
    
    constraint fk_veh
    foreign key  Vehicles(VehicleID)
    references  Vehicles(VehicleID)
);


create table  Service_History(
	ServiceID int primary key,
	VehicleID int ,
	ServiceDat date,
    OdometerReading long,
    Notes varchar(200),
    constraint ser_fk
    foreign key  Vehicles(VehicleID)
    references  Vehicles(VehicleID)
);

create table  Maintenance_Alerts(
	AlertID int primary key,
	VehicleID int ,
	AlertDate date,
    Reason varchar(500),
    constraint m_fk
    foreign key  Vehicles(VehicleID)
    references  Vehicles(VehicleID)
);


