CREATE TABLE aircrafts_data (
    aircraft_code VARCHAR(3) NOT NULL PRIMARY KEY,
    model VARCHAR(255) NOT NULL,
    `range` INT NOT NULL
);

CREATE TABLE airports_data (
    airport_code VARCHAR(3) NOT NULL PRIMARY KEY,
    airport_name VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    coordinates POINT NOT NULL,
    timezone VARCHAR(50) NOT NULL
);

CREATE TABLE boarding_passes (
    ticket_no VARCHAR(13) NOT NULL,
    flight_id INT NOT NULL,
    boarding_no INT NOT NULL,
    seat_no VARCHAR(4) NOT NULL,
    PRIMARY KEY (ticket_no, flight_id)
);

CREATE TABLE bookings (
    book_ref VARCHAR(6) NOT NULL PRIMARY KEY,
    book_date DATETIME NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL
);

CREATE TABLE flights (
    flight_id INT NOT NULL PRIMARY KEY,
    flight_no VARCHAR(6) NOT NULL,
    scheduled_departure DATETIME NOT NULL,
    scheduled_arrival DATETIME NOT NULL,
    departure_airport VARCHAR(3) NOT NULL,
    arrival_airport VARCHAR(3) NOT NULL,
    status VARCHAR(20) NOT NULL,
    aircraft_code VARCHAR(3) NOT NULL,
    actual_departure DATETIME,
    actual_arrival DATETIME
);

CREATE TABLE seats (
    aircraft_code VARCHAR(3) NOT NULL,
    seat_no VARCHAR(4) NOT NULL,
    fare_conditions VARCHAR(10) NOT NULL,
    PRIMARY KEY (aircraft_code, seat_no)
);

CREATE TABLE ticket_flights (
    ticket_no VARCHAR(13) NOT NULL,
    flight_id INT NOT NULL,
    fare_conditions VARCHAR(10) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (ticket_no, flight_id)
);

CREATE TABLE tickets (
    ticket_no VARCHAR(13) NOT NULL PRIMARY KEY,
    book_ref VARCHAR(6) NOT NULL,
    passenger_id VARCHAR(20) NOT NULL
);