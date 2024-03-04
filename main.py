import mysql.connector
from flask import Flask, render_template, request
from datetime import datetime


app = Flask(__name__)

connector = mysql.connector.connect(host="localhost", user="root", password="", database="Lib_man_sys")
cursor = connector.cursor()
# cursor.execute('TRUNCATE TABLE member')
# cursor.execute('CREATE TABLE member (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50), contact_info VARCHAR(50));')
# cursor.execute('CREATE TABLE book (id INT PRIMARY KEY AUTO_INCREMENT, title VARCHAR(50), author VARCHAR(50), genre VARCHAR(50));')
# cursor.execute('CREATE TABLE loaning (id INT PRIMARY KEY AUTO_INCREMENT, member_id VARCHAR(50), book_id VARCHAR(50), b_date DATE, r_date DATE);')
# cursor.close()

def connect_to_database():
    try:
    # Replace with your actual connection details
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lib_man_sys"
            )
        return connection
    except mysql.connector.Error as err:
        print("Connection error:", err)
        return None

def add_member(member_name, email):
    connection = connect_to_database()
    if connection:
        try:
            print("Connection Formed.")
            cursor = connection.cursor()
            sql = "INSERT INTO member (name, contact_info) VALUES (%s, %s)" 
            cursor.execute(sql, (member_name, email))
            connection.commit()
            print("Member added successfully.")
        except mysql.connector.Error as err:
            print("Error adding member: ", err)
        finally:
            if connection:
                connection.close()
    else:
        print("Failed to connect to databse.")

def add_book(title, author, genre):
    connection = connect_to_database()
    if connection:
        try:
            print("Connection Formed.")
            cursor = connection.cursor()
            sql = "INSERT INTO book (title, author, genre) VALUES (%s, %s, %s)" 
            cursor.execute(sql, (title, author, genre))
            connection.commit()
            print("Book added successfully.")
        except mysql.connector.Error as err:
            print("Error adding member: ", err)
        finally:
            if connection:
                connection.close()
    else:
        print("Failed to connect to databse.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/library')
def Library():
    return render_template('library.html')

@app.route('/projects')
def Projects():
    return render_template('projects.html')

@app.route('/recruitment')
def Recruitment():
    return render_template('recruitment.html')

@app.route('/reg_member', methods=['POST','GET'])
def Reg_member():
    if request.method == 'POST':
        member_name = request.form['member_name']
        email = request.form['email']
        add_member(member_name, email)
    return render_template('reg_member.html')

@app.route('/reg_book', methods=['POST','GET'])
def Reg_book():
    if request.method == 'POST':
        book_name = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        add_book(book_name, author, genre)
    return render_template('reg_book.html')

@app.route('/b_book', methods=['POST','GET'])
def B_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        connection = connect_to_database()
        cursor = connection.cursor()
        search_query = 'SELECT * FROM book WHERE '
        search_terms = []
        if title:
            # Search by exact title match (excluding wildcards)
            search_terms.append(f"title = '{title}'")  # Quote column name and value

        if author:
            search_terms.append(f"author LIKE '%{author}%'")  # Use wildcards for partial author match

        if genre:
            search_terms.append(f"genre LIKE '%{genre}%'")  # Use wildcards for partial genre match

        if search_terms:
            search_query += ' AND '.join(search_terms)
            search_query += ';'
        cursor.execute(search_query)
        books = cursor.fetchall()
        print(books)
        return render_template('b_book.html', books=books)
    #Handle GET request
    return render_template('b_book.html', books=None)
    
@app.route('/borrowing', methods=['POST','GET'])
def Borrowing():
    if request.method == 'POST':
        book_i = request.form.get('book_id')
        borrower = request.form.get('borrower', '')
        borrow_date = datetime.now()
        connection = connect_to_database()
        cursor = connection.cursor()

        sql = f'SELECT id FROM member WHERE name LIKE %s'
        cursor.execute(sql, ('%' + borrower + '%',))
        print(sql, ('%' + borrower + '%',))
        member_i = cursor.fetchone()

        if member_i:
            sql_query = 'INSERT INTO loaning (member_id, book_id, b_date) VALUES (%s,%s,%s)'
            cursor.execute(sql_query, (member_i[0], book_i, borrow_date.strftime('%Y-%m-%d')))
            connection.commit()
            print("Loan data inserted successfully.")
        else:
            print("Loan Data could not be inserted.")
    return render_template('b_book.html', book_id=book_i)


app.run(debug=True) 