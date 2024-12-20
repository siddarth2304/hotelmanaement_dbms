from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Setup MySQL connection
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",  # your mysql host
        user="root",       # your mysql username
        password="Siddarth@@1",  # your mysql password
        database="hotel_management_system_1"
    )
    return connection


# Route to display all hotels
@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM hotel')  # Changed from hotels to hotel
    hotels = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', hotels=hotels)


# Route to display all employees
@app.route('/employees')
def employees():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM employee')  # Changed from employees to employee
    employees = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('employees.html', employees=employees)


@app.route('/hotel/<int:hotel_id>/menu')
def hotel_menu(hotel_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Retrieve menu items associated with the hotel
    query = '''
        SELECT fi.item_id, fi.name, fi.price, fi.type
        FROM food_item fi
        JOIN menu m ON fi.menu_id = m.menu_id
        WHERE m.hotel_id = %s
    '''
    cursor.execute(query, (hotel_id,))
    menu_items = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('menu.html', menu_items=menu_items, hotel_id=hotel_id)




# Route to show detailed info about a specific menu item
@app.route('/menu/item/<int:item_id>')
def menu_item(item_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM food_item WHERE item_id = %s', (item_id,))  # Changed from menu to food_item
    item = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('menu_item.html', item=item)
    # Route to add a new chef
@app.route('/add_chef', methods=['GET', 'POST'])
def add_chef():
    if request.method == 'POST':
        # Get data from the form
        ssn = request.form['ssn']
        name = request.form['name']
        date_of_join = request.form['date_of_join']
        cuisine = request.form['cuisine']
        hotel_id = request.form['hotel_id']
        
        # Validate input fields
        if not ssn or not name or not date_of_join or not cuisine or not hotel_id:
            error_message = "Please fill all the fields."
            return render_template('add_chef.html', error=error_message)
        
        # Insert into database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO chef (ssn, name, date_of_join, cuisine, hotel_id) VALUES (%s, %s, %s, %s, %s)",
            (ssn, name, date_of_join, cuisine, hotel_id)
        )
        connection.commit()
        cursor.close()
        connection.close()
        
        success_message = "Chef added successfully!"
        return render_template('add_chef.html', success=success_message)

    return render_template('add_chef.html')





@app.route('/hotel/<int:hotel_id>/chefs')
def hotel_chefs(hotel_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        'SELECT ssn, name, date_of_join, cuisine, hotel_id FROM chef WHERE hotel_id = %s', 
        (hotel_id,)
    )
    chefs = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('chefs.html', chefs=chefs, hotel_id=hotel_id)


# Route to add a new hotel
@app.route('/add_hotel', methods=['GET', 'POST'])
def add_hotel():
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        start_date = request.form['start_date']
        revenue_planned = request.form['revenue_planned']
        expenditure_expected = request.form['expenditure_expected']
        city = request.form['city']
        state = request.form['state']
        phone_no = request.form['phone_no']
        
        # Validate input fields
        if not name or not start_date or not revenue_planned or not expenditure_expected or not city or not state or not phone_no:
            error_message = "Please fill all the fields."
            return render_template('add_hotel.html', error=error_message)
        
        # Insert into hotel table
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO hotel (name, start_date, revenue_planned, expenditure_expected, city, state, phone_no) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (name, start_date, revenue_planned, expenditure_expected, city, state, phone_no)
        )
        
        # Get the hotel_id of the newly inserted hotel
        hotel_id = cursor.lastrowid
        
        # Commit the transaction
        connection.commit()
        cursor.close()
        connection.close()
        
        success_message = f"Hotel added successfully! The Hotel ID is {hotel_id}."
        return render_template('add_hotel.html', success=success_message)

    return render_template('add_hotel.html')




@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        # Get data from the form
        emp_id = request.form['emp_id']
        name = request.form['name']
        date_of_joining = request.form['date_of_joining']
        department = request.form['department']
        ssn = request.form['ssn']
        phone = request.form['phone']
        
        # Validate input fields
        if not emp_id or not name or not department or not ssn or not phone:
            error_message = "Please fill all the fields."
            return render_template('add_employee.html', error=error_message)
        
        # Insert into database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO employee (emp_id, name, date_of_joining, department, ssn, phone) VALUES (%s, %s, %s, %s, %s, %s)',
            (emp_id, name, date_of_joining, department, ssn, phone)
        )
        connection.commit()
        cursor.close()
        connection.close()
        
        success_message = "Employee added successfully!"
        return render_template('add_employee.html', success=success_message)

    return render_template('add_employee.html')


@app.route('/add_menu_item', methods=['GET', 'POST'])
def add_menu_item():
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        # Safely accessing form fields using .get() to prevent errors if fields are missing
        name = request.form.get('name')
        price = request.form.get('price')
        item_type = request.form.get('type')
        menu_id = request.form.get('menu_id')
        category_id = request.form.get('category_id') or None  # Default to None if category_id is not provided
        hotel_id = request.form.get('hotel_id')  # Added hotel_id for menu item

        # Check if required fields are provided, otherwise return an error message
        if not name or not price or not menu_id or not hotel_id:
            error_message = "Please fill in all required fields!"
            menus = get_menus()
            hotels = get_hotels()
            return render_template('add_menu_item.html', error=error_message, menus=menus, hotels=hotels)

        try:
            # Insert the menu item with the hotel_id
            cursor.execute(
                'INSERT INTO food_item (name, price, type, menu_id, category_id, hotel_id) VALUES (%s, %s, %s, %s, %s, %s)',
                (name, price, item_type, menu_id, category_id, hotel_id)
            )
            connection.commit()
            success_message = "Menu item added successfully!"
            # Fetch menus for the dropdown and pass hotels too
            return render_template('add_menu_item.html', success=success_message, menus=get_menus(), hotels=get_hotels())
        except mysql.connector.Error as err:
            error_message = f"An error occurred: {err}"
            return render_template('add_menu_item.html', error=error_message, menus=get_menus(), hotels=get_hotels())
    else:
        # Fetch the menus and hotels to populate the dropdowns
        menus = get_menus()
        hotels = get_hotels()  # Function to get hotels
        return render_template('add_menu_item.html', menus=menus, hotels=hotels)

    cursor.close()
    connection.close()

# Function to fetch hotels
def get_hotels():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT hotel_id, name FROM hotel")  # 'name' is the actual column for hotel name
    hotels = cursor.fetchall()
    cursor.close()
    connection.close()
    return hotels

# Function to fetch menus
def get_menus():
    """Fetch available menus from the database."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT menu_id, name FROM menu')
    menus = cursor.fetchall()
    cursor.close()
    connection.close()
    return menus



# Route to add new customer
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        c_id = request.form['c_id']
        name = request.form['name']
        address = request.form['address']
        phone_no = request.form['phone_no']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO customer (c_id, name, address, phone_no) VALUES (%s, %s, %s, %s)',  # Changed from customers to customer
            (c_id, name, address, phone_no)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('customers'))
    return render_template('add_customer.html')


# Route to show all customers
@app.route('/customers')
def customers():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM customer')
    customers = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('customers.html', customers=customers)


# Route to show all orders
@app.route('/orders')
def orders():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM orders')  # Changed from orders to orders (this one is correct)
    orders = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('orders.html', orders=orders)


# Route to add a new order
@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        order_date = request.form['order_date']
        amount = request.form['amount']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO orders (customer_id, order_date, amount) VALUES (%s, %s, %s)',
            (customer_id, order_date, amount)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('orders'))
    return render_template('add_order.html')


# Route to show all deliveries
@app.route('/deliveries')
def deliveries():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM delivery')  # Changed from deliveries to delivery
    deliveries = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('deliveries.html', deliveries=deliveries)


# Route to add a new delivery
@app.route('/add_delivery', methods=['GET', 'POST'])
def add_delivery():
    if request.method == 'POST':
        order_id = request.form['order_id']
        delivery_date = request.form['delivery_date']
        delivery_by = request.form['delivery_by']
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO delivery (order_id, delivery_date, delivery_by) VALUES (%s, %s, %s)',  # Changed from deliveries to delivery
            (order_id, delivery_date, delivery_by)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('deliveries'))
    return render_template('add_delivery.html')


if __name__ == '__main__':
    app.run(debug=True)

