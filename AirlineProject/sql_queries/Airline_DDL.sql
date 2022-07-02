create table airline
	(
    airline_name    varchar(20), 
	primary key (airline_name)
	);

create table airport
	(
    airport_name        varchar(3),
    city                varchar(20),
    country             varchar(20),
    airport_type        varchar(15)
        check (airport_type in ('Domestic', 'International', 'Both')),
    primary key (airport_name)
	);

create table airline_staff
	(
    username    varchar(20), 
    password    varchar(20) not null,
    airline_name     varchar(20), 
    first_name  varchar(15), 
    last_name   varchar(15),
    date_of_birth   DATE,
    email_address   varchar(30), 
    primary key (username),
    foreign key (airline_name) references airline(airline_name)
	);

create table staff_phones
    (
    username        varchar(20),
    phone_number    char(10),
    primary key (username),
    foreign key (username) references airline_staff(username)
        on delete cascade
    );

create table airplane
    (   
    airplane_ID     smallint,
    airline_name    varchar(20),
    total_seats     smallint,
    manufacturer    varchar(15),
    age             tinyint,
    primary key (airplane_ID),
    foreign key (airline_name) references airline(airline_name)
        on delete set null
    );

create table flight
    (
    flight_number           smallint auto_increment,
    departure_date_and_time DATETIME,
    airline_name            varchar(20),
    airplane_ID             smallint,
    departure_aiport        varchar(3),
    arrival_airport         varchar(3),
    arrival_date_and_time   DATETIME,
    flight_status           varchar(10)
        check (flight_status in ('Delayed', 'On-Time')),
    base_price              int,
    primary key (flight_number, departure_date_and_time, airline_name),
    foreign key (airline_name, airplane_ID) 
        references airplane(airline_name, airplane_ID),
    foreign key (departure_aiport) references airport(airport_name),
    foreign key (arrival_airport) references airport(airport_name)
    );


create table customer
    (
        email_address   varchar(40),
        password        varchar(20),
        name            varchar(40),
        building_number smallint,
        street          varchar(20),
        city            varchar(20),
        phone_number    char(10),
        passport_num    char(12),
        passport_exp    DATE,
        passport_country    varchar(20),
        date_of_birth   DATE,
        primary key (email_address)
    );

create table ticket
    (
    ticket_ID               int AUTO_INCREMENT,
    flight_number           smallint,
    departure_date_and_time DATETIME,
    airline_name            varchar(20),
    airport_name            varchar(3),
    sale_price              int,
    email_address           varchar(40),
    card_type               varchar(8)
        check (card_type in ('Credit', 'Debit')),
    card_number             char(10),
    name_on_card            varchar(40),
    exp_date                DATE,
    purchase_date_and_time  DATETIME,
    rating                  varchar(3),
    comments                varchar(80),
    primary key (ticket_ID),
    foreign key (email_address) references customer(email_address),
    foreign key (flight_number, departure_date_and_time, airline_name)
        references flight(flight_number,departure_date_and_time,airline_name)
    );

alter table ticket auto_increment=20;
alter table flight auto_increment=100;
