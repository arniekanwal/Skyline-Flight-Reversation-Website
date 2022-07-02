SKYLINE FLIGHT REVERSATION

Authors: Arnav Kanwal
CS-UY 3083 Databases
==================================
DESCRIPTION:

This project features several simple interfaces to create an airline ticketing
system and flight reservation system. This was implemented using a 
MySQL Database, Python Flask, and simple html pages.

Features include a login page for Airline Staff to register with their respective
airlines and have the ability to add flights, tickets, update the status of flights,
and add airports/airplanes for which their airline can fly to or use.

The website also provides a backend for customers where customers can log in,
purchase/cancel tickets, view their upcoming flight statuses, search for flights,
and leave reviews on their past flights.

-----------------------------------
DESCRIPTION OF HTML PAGES:

There are 10 different HTML pages to host the various features allowed on 
this flight reservation system. 

Cust_home, cust_login, cust_register all provide separate pages for customers
to view their upcoming flights, login into their account, or register as a new user.
From the customer home page, they can also view their monthly expenditures throughout
the whole year.

The mainpage, index.html, uses Jinja2 to vary control based on what user is signed in.
When no one is logged in, general users are allowed to search for upcoming flights
based on arrival, departure airports and their flight dates. If logged in as a customer,
the user is allowed to then also purchase tickets for any of the following flights. If 
logged in as staff, then they can only view upcoming flights for their particular airline
employer and have the ability to update flight-statuses.

ticket.html, review_ticket.html are also pages only allowed to be used by the customer
which generates a page to enter credit/debit card information to purchase a ticket
and review/rate their flights which have already landed.

staff_home, staff_login, and staff_register are the final pages which provide login/registration
pages for staff members. New staff members can only register if registed by another staff member.
In addition, their homepage allows many additional features like adding new planes to their airline,
viewing customer's ratings on flights, and searching for their premium customers through frequent
flyers. 
--------------------------
PYTHON FLASK:

The interactive features on the website are handled by Python Flask's micro web framework
which handles the interaction between physical users of the webpage and the database.
All python files also handle specific SQL queries to pull information from the database
such as customer's monthly expenditures and display it on the appropiate web page. 

The main code is placed on airline.py and private information/keys are stored on config.py

--------------------------
SQL Files:

The appropiate SQL files have also been provided should another person want to implement this
project.

It contains files for how different tables were created as well as a second sql file for example
insertions in the database to test the website. 




