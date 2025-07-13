from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
import uuid
import boto3

bp = Blueprint('routes', __name__)

# Helper: Get DynamoDB table
def get_table(name):
    dynamodb = boto3.resource('dynamodb', region_name=current_app.config['DYNAMODB_TABLE'].meta.client.meta.region_name)
    return dynamodb.Table(name)

# --- User Authentication ---

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users_table = get_table('Users')
        response = users_table.get_item(Key={'username': username})
        user = response.get('Item')
        if user and user.get('password') == password:
            session['username'] = username
            return redirect(url_for('routes.dashboard'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users_table = get_table('Users')
        # Check if user exists
        response = users_table.get_item(Key={'username': username})
        if 'Item' in response:
            return render_template('register.html', error="Username already exists")
        users_table.put_item(Item={'username': username, 'password': password})
        return redirect(url_for('routes.login'))
    return render_template('register.html')

@bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('routes.login'))

# --- Movies and Bookings ---

@bp.route('/')
def home():
    # For demo, static movies; in production, fetch from DynamoDB
    movies = [
        {
            "title": "Inception",
            "poster_url": "https://image.tmdb.org/t/p/w300/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg",
            "city": "Hyderabad",
            "showtimes": [
                {"show_id": "1", "date": "2025-06-25", "time": "18:30"},
                {"show_id": "2", "date": "2025-06-25", "time": "21:00"}
            ]
        },
        {
            "title": "Interstellar",
            "poster_url": "https://image.tmdb.org/t/p/w300/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg",
            "city": "Hyderabad",
            "showtimes": [
                {"show_id": "3", "date": "2025-06-26", "time": "17:00"},
                {"show_id": "4", "date": "2025-06-26", "time": "20:15"}
            ]
        },
        {
            "title": "The Dark Knight",
            "poster_url": "https://image.tmdb.org/t/p/w300/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
            "city": "Hyderabad",
            "showtimes": [
                {"show_id": "5", "date": "2025-06-27", "time": "19:00"},
                {"show_id": "6", "date": "2025-06-27", "time": "22:00"}
            ]
        },
        {
            "title": "Avatar: The Way of Water",
            "poster_url": "https://image.tmdb.org/t/p/w300/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg",
            "city": "Hyderabad",
            "showtimes": [
                {"show_id": "7", "date": "2025-06-28", "time": "16:00"},
                {"show_id": "8", "date": "2025-06-28", "time": "19:30"}
            ]
        },
        {
            "title": "Dune: Part Two",
            "poster_url": "https://image.tmdb.org/t/p/w300/8b8R8l88Qje9dn9OE8PY05Nxl1X.jpg",
            "city": "Hyderabad",
            "showtimes": [
                {"show_id": "9", "date": "2025-06-29", "time": "15:45"},
                {"show_id": "10", "date": "2025-06-29", "time": "18:45"}
            ]
        },
        {
            "title": "Avengers: Endgame",
            "poster_url": "https://image.tmdb.org/t/p/w300/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
            "city": "Hyderabad",
            "showtimes": [
                {"show_id": "11", "date": "2025-06-30", "time": "20:00"},
                {"show_id": "12", "date": "2025-06-30", "time": "23:00"}
            ]
        },
        {
            "title": "Oppenheimer",
            "poster_url": "https://image.tmdb.org/t/p/w300/ptpr0kGAckfQkJeJIt8st5dglvd.jpg",
            "city": "Hyderabad",
            "showtimes": [
                {"show_id": "13", "date": "2025-07-01", "time": "17:45"},
                {"show_id": "14", "date": "2025-07-01", "time": "21:15"}
            ]
        },
        {
            "title": "Spider-Man: No Way Home",
            "poster_url": "https://image.tmdb.org/t/p/w300/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg",
            "city": "Hyderabad",
            "showtimes": [
                {"show_id": "15", "date": "2025-07-02", "time": "18:00"},
                {"show_id": "16", "date": "2025-07-02", "time": "20:45"}
            ]
        }
    ]
    return render_template('index.html', movies=movies)

@bp.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('routes.login'))
    movies = [
       {
            "title": "Inception",
            "poster_url": "https://image.tmdb.org/t/p/w300/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg",
            "city": "Hyderabad",
            "showtimes": [
                {"show_id": "1", "date": "2025-06-25", "time": "18:30"},
                {"show_id": "2", "date": "2025-06-25", "time": "21:00"}
            ]
        },
        {
            "title": "Interstellar",
            "poster_url": "https://image.tmdb.org/t/p/w300/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg",
            "city": "Hyderabad",
            "showtimes": [
                {"show_id": "3", "date": "2025-06-26", "time": "17:00"},
                {"show_id": "4", "date": "2025-06-26", "time": "20:15"}
            ]
        },
        {
            "title": "The Dark Knight",
            "poster_url": "https://image.tmdb.org/t/p/w300/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
            "city": "Hyderabad",
            "showtimes": [
                {"show_id": "5", "date": "2025-06-27", "time": "19:00"},
                {"show_id": "6", "date": "2025-06-27", "time": "22:00"}
            ]
        },
        {
            "title": "Avatar: The Way of Water",
            "poster_url": "https://image.tmdb.org/t/p/w300/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg",
            "city": "Hyderabad",
            "showtimes": [
                {"show_id": "7", "date": "2025-06-28", "time": "16:00"},
                {"show_id": "8", "date": "2025-06-28", "time": "19:30"}
            ]
        },
        {
            "title": "Dune: Part Two",
            "poster_url": "https://image.tmdb.org/t/p/w300/8b8R8l88Qje9dn9OE8PY05Nxl1X.jpg",
            "city": "Hyderabad",
            "showtimes": [
                {"show_id": "9", "date": "2025-06-29", "time": "15:45"},
                {"show_id": "10", "date": "2025-06-29", "time": "18:45"}
            ]
        },
        {
            "title": "Avengers: Endgame",
            "poster_url": "https://image.tmdb.org/t/p/w300/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
            "city": "Hyderabad",
            "showtimes": [
                {"show_id": "11", "date": "2025-06-30", "time": "20:00"},
                {"show_id": "12", "date": "2025-06-30", "time": "23:00"}
            ]
        },
        {
            "title": "Oppenheimer",
            "poster_url": "https://image.tmdb.org/t/p/w300/ptpr0kGAckfQkJeJIt8st5dglvd.jpg",
            "city": "Hyderabad",
            "showtimes": [
                {"show_id": "13", "date": "2025-07-01", "time": "17:45"},
                {"show_id": "14", "date": "2025-07-01", "time": "21:15"}
            ]
        },
        {
            "title": "Spider-Man: No Way Home",
            "poster_url": "https://image.tmdb.org/t/p/w300/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg",
            "city": "Hyderabad",
            "showtimes": [
                {"show_id": "15", "date": "2025-07-02", "time": "18:00"},
                {"show_id": "16", "date": "2025-07-02", "time": "20:45"}
            ]
        }
    ]
    return render_template('dashboard.html', movies=movies)

@bp.route('/select-seats')
def select_seats():
    show_id = request.args.get("show_id")
    seats = []
    # Fetch booked seats from DynamoDB
    bookings_table = get_table('Bookings')
    response = bookings_table.get_item(Key={'show_id': show_id})
    booked_seats = response.get('Item', {}).get('seats', [])

    for row in "ABCDEFG":
        if row in "AB":
            seats_in_row = 10
        elif row in "CD":
            seats_in_row = 12
        else:
            seats_in_row = 14
        for num in range(1, seats_in_row + 1):
            seat_id = f"{row}{num}"
            seats.append({
                "id": seat_id,
                "booked": seat_id in booked_seats
            })
    return render_template("seat_map.html", seats=seats, show_id=show_id)

@bp.route('/payment', methods=["GET", "POST"])
def payment():
    if request.method == "POST":
        selected_seats = request.form.get("selected_seats", "")
        show_id = request.form.get("show_id")
        return render_template("payment.html", selected_seats=selected_seats.split(","), show_id=show_id)
    return render_template("payment.html", selected_seats=[], show_id=None)

@bp.route('/confirm-booking', methods=["POST"])
def confirm_booking():
    if 'username' not in session:
        return redirect(url_for('routes.login'))
    selected_seats = request.form.get("selected_seats")
    show_id = request.form.get("show_id")
    if not selected_seats or not show_id:
        return render_template("confirmation.html", seats=[])
    seats_list = selected_seats.split(",")
    username = session['username']

    # Update DynamoDB: add booked seats for the show
    bookings_table = get_table('Bookings')
    response = bookings_table.get_item(Key={'show_id': show_id})
    item = response.get('Item', {})
    already_booked = set(item.get('seats', []))
    new_booked = set(seats_list)
    if already_booked & new_booked:
        # Some seats already booked
        return render_template("confirmation.html", seats=[], error="Some seats already booked. Please try again.")
    updated_seats = list(already_booked | new_booked)
    bookings_table.put_item(Item={'show_id': show_id, 'seats': updated_seats})

    # Optionally, store user booking history
    user_bookings_table = get_table('UserBookings')
    user_bookings_table.put_item(Item={
        'username': username,
        'show_id': show_id,
        'seats': seats_list,
        'booking_id': str(uuid.uuid4())
    })

    # Send SNS notification
    sns = current_app.config['SNS_CLIENT']
    topic_arn = current_app.config['SNS_TOPIC_ARN']
    sns.publish(
        TopicArn=topic_arn,
        Message=f"User {username} booked seats {', '.join(seats_list)} for show {show_id}",
        Subject="New Booking"
    )

    return render_template("confirmation.html", seats=seats_list)
