from hashlib import md5
from flask import Flask, render_template, request, session, redirect, url_for
from config import *
from datetime import datetime, timedelta
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password=PASSWORD,
                       db='AirlineProject',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define route to mainpage
@app.route('/')
def mainpage():
	return render_template('index.html')

'''
Define routes for all features related to Customer.
Includes handling login/logout, registration, authentication,
searching for flights, and other relevant features.
-------------------------------------------------------
'''
@app.route('/custLogin')
def cust_login():
	return render_template('cust_login.html')

@app.route('/custRegister')
def cust_register():
	return render_template('cust_register.html')

@app.route('/custLoginAuth', methods=['GET', 'POST'])
def custLoginAuth():
	email = request.form['email']
	p_entry = request.form['password']
	password = str(md5(p_entry.encode('utf-8')).digest())

	#cursor used to send/execute queries
	cursor = conn.cursor()
	query = 'SELECT * FROM customer WHERE email_address = %s and password = %s'
	cursor.execute(query, (email, password))
	data = cursor.fetchone()
	cursor.close()

	if(data):
		# create session (built-in) for customer
		session['customer'] = {'email': email, 'name': data['name']}
		return redirect('/cust_home')
	else:
		error = 'Invalid login or email address'
		return render_template('cust_login.html', error=error)

@app.route('/custRegisterAuth', methods=['GET', 'POST'])
def custRegisterAuth():
	# collect info from the form
	info = []
	for i in range(1,12):
		form = request.form[f'item{i}']
		info.append(form)
		if i == 2:
			info.pop()
			password = str(md5(form.encode('utf-8')).digest())
			info.append(password)

	cursor = conn.cursor()
	query = 'SELECT * FROM customer WHERE email_address = %s'
	cursor.execute(query, (info[0]))
	data = cursor.fetchone()
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('cust_register.html', error = error)
	else:
		ins = f'INSERT INTO customer VALUES{*info,}'
		cursor.execute(ins)
		conn.commit()
		cursor.close()
		return redirect('/')

@app.route('/cust_logout')
def cust_logout():
	session.pop('customer')
	return redirect('/')

# Customer Home Page
@app.route('/cust_home', defaults={'error': None})
@app.route('/cust_home/<error>')
def cust_home(error):
	customer = session['customer']
	cursor = conn.cursor()
	# Find all Upcoming Flights
	query = "SELECT %s from flight natural join ticket WHERE email_address='%s' and NOW() %s departure_date_and_time ORDER BY departure_date_and_time" 
	cursor.execute((query % ('flight.*', customer['email'], '<')))
	upcoming = cursor.fetchall()
	# Find all Past Flights
	cursor.execute((query % ('flight.*, ticket_ID, sale_price, rating', customer['email'], '>')))
	past_flights = cursor.fetchall()
	# Get Spending
	query = "SELECT date_format(departure_date_and_time, '%%M') as month, sum(sale_price) as expenditures FROM ticket WHERE email_address=%s GROUP BY date_format(departure_date_and_time, '%%M')"
	cursor.execute(query, (customer['email']))
	spending = cursor.fetchall()
	cursor.close()	
	
	return render_template('cust_home.html', name=customer['name'], upcoming=upcoming, past_flights=past_flights, error=error, spending=spending)

@app.route('/book_flight')
def book_flight():
	return render_template('index.html', name=session['customer']['name'], message=True, customer=True)

'''
Define routes for all actions related to Airline_Staff.
Includes handling login, registration, authentication,
logout, adding flights, and other relevant features.
-----------------------------------------------------
'''
@app.route('/staffLogin')
def staff_login():
	return render_template('staff_login.html')

@app.route('/staff_home', defaults={'success': None})
@app.route('/staff_home/<success>')
def staff_home(success):
	user = session['staff']
	cursor = conn.cursor()
	query = "SELECT airplane_ID FROM airplane where airline_name=%s"
	cursor.execute(query, (user['airline']))
	planes = cursor.fetchall()

	query = "SELECT airport_name FROM airport"
	cursor.execute(query)
	airports = cursor.fetchall()

	query = "SELECT email_address as flier, count(ticket_ID) as flight_amt FROM ticket where airline_name = %s group by email_address"
	cursor.execute(query, (user['airline']))
	flights = cursor.fetchall()
	cursor.close()

	sales = request.args.get('sales', None)
	num_sold = request.args.get('num_sold', None)

	return render_template('staff_home.html', name=user['name'], 
			planes=planes, airports=airports, airline=user['airline'],
			success=success, sales=sales, num_sold=num_sold, flights=flights)

@app.route('/staffLoginAuth', methods=['GET', 'POST'])
def staffLoginAuth():
	username = request.form['username']
	p_entry = request.form['password']
	password = str(md5(p_entry.encode('utf-8')).digest())

	cursor = conn.cursor()
	query = 'SELECT * FROM airline_staff WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	data = cursor.fetchone()
	cursor.close()
	# create a session for the staff or return error
	if(data):
		session['staff'] = {'username': username, 
							'name': data['first_name'] + " " + data['last_name'], 
							'airline': data['airline_name']}

		return redirect('/staff_home')
	else:
		error = 'Invalid login or username'
		return render_template('staff_login.html', error=error)

@app.route('/goToStaffRegister')
def goToStaffRegister():
	return render_template('staff_register.html')

@app.route('/staffRegisterAuth', methods=['GET', 'POST'])
def staffRegisterAuth():
	info = []
	for i in range(1,8):
		form = request.form[f'item{i}']
		info.append(form)
		if i == 2:
			info.pop()
			password = str(md5(form.encode('utf-8')).digest())
			info.append(password)

	phones = request.form['phone']
	result = [x.strip() for x in phones.split(";")]
	print(phones)
	cursor = conn.cursor()
	query = 'SELECT * FROM airline_staff WHERE username = %s'
	cursor.execute(query, (info[0]))
	data = cursor.fetchone()
	if(data):
		error = "This user already exists"
		return render_template('staff_register.html', error = error)
	else:
		ins = f'INSERT INTO airline_staff VALUES{*info, }'
		cursor.execute(ins)
		for phone in result:
			ins = 'INSERT INTO staff_phones VALUES(%s, %s)'
			cursor.execute(ins, (info[0], phone))
		conn.commit()
		cursor.close()
		return redirect('/staffLogin')

@app.route('/staff_logout')
def staff_logout():
	session.pop('staff')
	return redirect('/')

@app.route('/staff_main')
def view_flights():
	data = session['staff']
	return render_template('index.html', name=data['name'], airline=data['airline'], staff=True, message=True)

@app.route('/staff_flight_view', methods=['GET', 'POST'], defaults={'update': None})
@app.route('/staff_flight_view/<update>')
def staff_flight_view(update):
	user = session['staff']
	airline = user['airline']
	select = request.form.get('staff_flight_view')
	query = "SELECT * FROM flight natural join airplane WHERE departure_date_and_time BETWEEN %s AND %s AND airline_name='%s' ORDER BY departure_date_and_time"
	cursor = conn.cursor()
	if select == "month":
		cursor.execute((query % ('NOW()', 'NOW() + interval 1 month', airline)))
	elif select == "month3":
		cursor.execute((query % ('NOW()', 'NOW() + interval 3 month', airline)))
	elif select == "year":
		cursor.execute((query % ('NOW()', 'NOW() + interval 1 year', airline)))
	else:
		cursor.execute((query % ('NOW() - interval 1 year', 'NOW()', airline)))
	data = cursor.fetchall()

	query2 = "SELECT flight_number, total_seats, count(ticket_ID) as num_tickets FROM ticket natural join flight natural join airplane GROUP BY flight_number, airplane_ID"
	cursor.execute(query2)
	availability = cursor.fetchall()
	for i in range(len(data)):
		flight = list(filter(lambda x: x['flight_number'] == data[i]['flight_number'], availability))
		data[i]['seats'] = data[i]['total_seats']
		if len(flight) != 0:
			data[i]['seats'] -= flight[0]['num_tickets']

	cursor.close()
	return render_template('index.html', staff=True, message=True, 
						posts=data, name=user['name'], airline=airline, update=update)

@app.route('/create_flight', methods=['GET', 'POST'])
def create_flight():
	info = []
	for i in range(2, 10):
		form = request.form[f'item{i}']
		info.append(form)
	cursor = conn.cursor()
	p_info = f'{*info,}'[1:-1]
	ins = "INSERT INTO flight VALUES(null, %s)"
	ins = ins % (p_info)
	cursor.execute(ins)
	conn.commit()
	cursor.close()
	return redirect(url_for('staff_home',success="Successfully Added Flight"))

@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
	info = []
	for i in range(1, 5):
		form = request.form[f'item{i}']
		info.append(form)
	cursor = conn.cursor()
	ins = f"INSERT INTO airport VALUES{*info,}"
	cursor.execute(ins)
	conn.commit()
	cursor.close()
	return redirect(url_for('staff_home',success="Successfully Added Airport"))

@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
	info = []
	for i in range(1, 6):
		form = request.form[f'item{i}']
		info.append(form)
	cursor = conn.cursor()
	ins = f"INSERT INTO airplane VALUES{*info,}"
	cursor.execute(ins)
	conn.commit()
	cursor.close()
	return redirect(url_for('staff_home',success="Successfully Added Airplane"))

@app.route('/revenue', methods=['GET', 'POST'])
def revenue():
	airline = session['staff']['airline']
	type = request.form['select_period']
	query = "SELECT count(ticket_ID) as num_sold, sum(sale_price) as sales FROM ticket WHERE departure_date_and_time between NOW() - interval 1 %s and NOW() and airline_name='%s' group by airline_name"
	cursor = conn.cursor()
	if type == "month":
		cursor.execute((query % ('month', airline)))
	else:
		cursor.execute((query % ('year', airline)))
	data = cursor.fetchone()
	if data == None:
		return redirect('/staff_home')
	else:
		sales = data['sales']
		num_sold = data['num_sold']
	return redirect(url_for('staff_home', sales=sales, num_sold=num_sold))

@app.route('/update_status', methods=['GET', 'POST'])
def update_status():
	flight = request.form['flight_no']
	status = request.form['status']
	query = "UPDATE flight SET flight_status=%s where flight_number=%s"
	cursor = conn.cursor()
	cursor.execute(query, (status, flight))
	conn.commit()
	cursor.close()
	return redirect(url_for('staff_flight_view', update='Updated Status'))

@app.route('/flight_rating', methods=['GET', 'POST'])
def flight_rating():
	flight = request.form['flight_num']
	query = "SELECT email_address, rating, comments FROM ticket WHERE flight_number=%s"
	cursor = conn.cursor()
	cursor.execute(query, (flight))
	data = cursor.fetchall()
	cursor.close()
	return render_template('flight_rating.html', data=data)

'''
Define all routes related to ticketing. This includes
loading ticket html pages, leaving comments/ratings,
purchasing, and cancelling tickets. 

Also include methods to search for flights on home page
while no users are signed in.
'''

@app.route('/searchflights', methods=['GET', 'POST'])
def search_flights():
	dep_airport = request.form['dep_airport']
	arr_airport = request.form['arr_airport']
	dep_date = request.form['dep_date']
	dep_date2 = dep_date + " 23:59:59"
	dep_date += " 00:00:00"

	cursor = conn.cursor()
	query = "SELECT flight_number, departure_airport, arrival_airport, departure_date_and_time, arrival_date_and_time, airline_name FROM flight WHERE departure_airport=%s and arrival_airport=%s and departure_date_and_time >= %s and departure_date_and_time <= %s"
	cursor.execute(query, (dep_airport,arr_airport,dep_date, dep_date2))
	flight_data = cursor.fetchall()
	query2 = "SELECT flight_number, total_seats, count(ticket_ID) as num_tickets FROM ticket natural join flight natural join airplane GROUP BY flight_number, airplane_ID"
	cursor.execute(query2)
	availability = cursor.fetchall()

	for i in range(len(flight_data)):
		flight_num = flight_data[i]['flight_number']
		# look up if any tickets/seats have been purchased from the matching flight_number
		flight = list(filter(lambda x: x['flight_number'] == flight_num, availability))
		# If the flight is fully open (no seats are booked)
		if len(flight) == 0:
			query3 = "select total_seats from flight natural join airplane where flight_number=%s"
			cursor.execute(query3, (flight_num))
			seats = cursor.fetchone()['total_seats']
		else:
			seats = flight[0]['total_seats'] - flight[0]['num_tickets']
		flight_data[i]['seats'] = seats
	cursor.close()

	# if customer is logged in, allow them to also purchase tickets from available flights
	if session.get('customer') != None:
		cursor = conn.cursor()
		query = "SELECT name FROM customer WHERE email_address=%s"
		cursor.execute(query, (session['customer']['email']))
		name = cursor.fetchone()['name']
		cursor.close()
		return render_template('index.html', posts=flight_data, name=name, message=True, customer=True)
	else:
		return render_template('index.html', posts=flight_data)

@app.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
	name = session['customer']['name']
	flight_num = request.form['flight_no']
	cursor = conn.cursor()
	query = "SELECT * from flight where flight_number=%s"
	cursor.execute(query, (flight_num))
	data = cursor.fetchone()
	if data == None:
		return render_template('index.html', name=name, message=True, customer=True, error='Flight does not exist')
	query2 = "SELECT flight_number, total_seats, count(ticket_ID) as num_tickets FROM ticket natural join flight natural join airplane WHERE flight_number=%s GROUP BY flight_number, airplane_ID, base_price"
	cursor.execute(query2, (flight_num))
	seat_info = cursor.fetchone()

	if seat_info == None:
		query3 = "SELECT total_seats from flight natural join airplane where flight_number=%s"
		cursor.execute(query3, (flight_num))
		seats = cursor.fetchone()['total_seats']
		total_seats = seats
	else:
		total_seats = seat_info['total_seats']
		seats = total_seats - seat_info['num_tickets']
	
	price = data['base_price']
	cursor.close()
	email = session['customer']['email']

	if (seats / total_seats) < 0.4:
		price *= 1.2

	return render_template('ticket.html', 
		flight=data['flight_number'],
		dep_airport=data['departure_airport'],
		arrival_airport=data['arrival_airport'],
		dep_date=data['departure_date_and_time'],
		sale_price=price,
		airline=data['airline_name'],
		email=email
	)

@app.route('/purchase_ticket', methods=['GET', 'POST'])
def purchase_ticket():
	info = []
	for i in range(2,12):
		form = request.form[f'item{i}']
		info.append(form)
	cursor = conn.cursor()
	p_info = f'{*info,}'[1:-1]
	ins = "INSERT INTO ticket VALUES(null, %s, NOW(), null, null)"
	ins = ins % (p_info)
	cursor.execute(ins)
	conn.commit()
	cursor.close()
	return redirect('/cust_home')

@app.route('/review_ticket', methods=['GET', 'POST'])
def review_ticket():
	email = session['customer']['email']
	ticket_ID = request.form['ticket']
	cursor = conn.cursor()
	query = "SELECT * FROM ticket WHERE ticket_ID=%s and email_address=%s"
	cursor.execute(query, (ticket_ID, email))
	review = cursor.fetchone()
	cursor.close()
	return render_template('review_ticket.html', ticket_ID=ticket_ID, comments=review['comments'])

@app.route('/update_ticket', methods=['GET', 'POST'])
def update_ticket():
	rating = request.form['rating']
	comments = request.form['comments']
	ticket_ID = request.form['ticket_ID']

	update = "UPDATE ticket SET rating=%s, comments=%s WHERE ticket_ID=%s"
	cursor = conn.cursor()
	cursor.execute(update, (rating, comments, ticket_ID))
	conn.commit()
	cursor.close()
	return redirect('/cust_home')

@app.route('/cancel_ticket', methods=['GET', 'POST'])
def cancel_ticket():
	email = session['customer']['email']
	flight = request.form['flight_no']
	cursor = conn.cursor()
	query = "SELECT departure_date_and_time as date, ticket_ID FROM ticket where flight_number=%s and email_address=%s"
	cursor.execute(query, (flight, email))
	info = cursor.fetchone()
	date = info['date']
	ticket_ID = info['ticket_ID']
	if datetime.today() + timedelta(days=1) < date:
		delete = "DELETE FROM ticket WHERE ticket_ID = %s"
		cursor.execute(delete, (ticket_ID))
		conn.commit()
		cursor.close()
		return redirect('/cust_home')
	else:
		return redirect(url_for('cust_home', error='Cannot cancel flight 24 hours before departure'))
	
app.secret_key = SECRET_KEY
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
