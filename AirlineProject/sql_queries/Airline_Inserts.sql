insert into airline
    values('Jet Blue');

insert into airline
    values('United');

insert into airline
    values('Delta');

insert into airport
    values('JFK','New York','USA','Both');

insert into airport
    values('LGA','New York','USA','Domestic');

insert into airport
    values('HSV','Huntsville','USA','Domestic');

insert into airport
    values('PVG','Shanghai','China','International');

insert into customer
    values('ajk8685@nyu.edu','abc123','Arnav Kanwal',55,'Clark St','Brooklyn','7206069174',
    '675843948567', DATE '2025-12-05','USA',DATE '2002-07-05');

insert into customer
    values('jd1122@nyu.edu','slkjd$-56','John Doe',2,'MetroTech Ctr','Brooklyn','9204448960',
    '123567893212', DATE '2023-7-12','USA',DATE '1999-07-01');

insert into customer
    values('bross@msn.com','rossiscute123','Betsy Ross',1010,'Pine Ridge Ct','Ann Arbor','7349895566',
    '098345678514', DATE '2024-08-09','USA',DATE '1990-08-09');

insert into customer
    values('jackdaniel@gmail.com','slajdks#','Jack Daniel',280,'Lynchburg Hwy','Lynchburg','4340070007',
    '000078934643', DATE '2030-01-20','USA',DATE '1911-10-09');

insert into airplane
    values(7471,'United',410,'Boeing',5);

insert into airplane
    values(7371,'Jet Blue',138,'Boeing',10);

insert into airplane
    values(3201,'Jet Blue',150,'Airbus',15);

insert into airplane
    values(3202,'Jet Blue',150,'Airbus',15);

insert into airline_staff
    values('allenjackson','aj3355','Jet Blue','Allen','Jackson',DATE '1992-05-23','ajackson@jetblue.com');

insert into airline_staff
    values('shawdavis22','iamshawdavis4','Jet Blue','Shaw','Davis',DATE '1990-11-11','shawdavis@jetblue.com');

insert into airline_staff
    values('robinhayes','ceo','Jet Blue','Robin','Hayes',DATE '1969-06-12','robinhayes@jetblue.com');

insert into flight
    values(NULL,'2022-07-30 13:00:00','Jet Blue', 3201,'LGA','HSV',
     '2022-07-30 16:00:00','On-Time',200);

insert into flight
    values(NULL,'2022-08-01 06:00:00','Jet Blue', 3202,'HSV','LGA',
     '2022-08-01 09:30:00', 'Delayed',175);

insert into flight
    values(NULL,'2022-07-30 08:45:00','United',7471,'JFK','PVG',
     '2022-07-31 10:00:00', 'On-Time',800);

insert into flight
    values(NULL,'2022-08-02 13:00:00','Jet Blue',7371,'LGA','HSV',
     '2022-08-02 16:00:00', 'On-Time',190);

insert into ticket
    values(null,100,'2022-07-30 13:00:00','Jet Blue','LGA',240,'jackdaniel@gmail.com',
    'Credit', 0004999811, 'Jack Daniel', 
    DATE '2026-12-01', NOW(), null, null);

insert into ticket
    values(null,101,'2022-08-01 06:00:00','Jet Blue','HSV', 175,'ajk8685@nyu.edu',
    'Credit', 0007300489, 'Arnav Kanwal', 
    DATE '2026-03-10', NOW(),null,null);

insert into ticket
    values(null,102,'2022-07-30 08:45:00','United','JFK',800,'jd1122@nyu.edu',
    'Debit', 1010234588, 'John Doe', 
    DATE '2030-10-10',NOW(),null,null);

insert into ticket
    values(null,103,'2022-08-02 13:00:00','Jet Blue','LGA',190,'ajk8685@nyu.edu',
    'Credit', 0007300489, 'Arnav Kanwal', 
    DATE '2026-03-10', NOW(),null,null);

