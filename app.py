import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    with sqlite3.connect('responses.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS responses (id INTEGER PRIMARY KEY, response TEXT)')

# Save response to the database
def save_response(response):
    with sqlite3.connect('responses.db') as conn:
        conn.execute('INSERT INTO responses (response) VALUES (?)', (response,))

# Get all responses from the database
def get_all_responses():
    with sqlite3.connect('responses.db') as conn:
        cursor = conn.execute('SELECT * FROM responses')
        return cursor.fetchall()

# Main page route
@app.route('/')
def index():
    return render_template('index.html')

# Question page route
@app.route('/response', methods=['GET', 'POST'])
def response():
    if request.method == 'POST':
        # Save the response to the database
        response_data = request.form['response']
        save_response(response_data)
        # Redirect to the thank you page after saving the response
        return redirect(url_for('thanks'))

    # If it's a GET request, show the question page
    return render_template('question.html')

# Thank you page route
@app.route('/thanks')
def thanks():
    return render_template('thankyou.html')

# View responses route
@app.route('/view_responses')
def view_responses():
    # Fetch responses from the database
    with sqlite3.connect('responses.db') as conn:
        cursor = conn.execute('SELECT * FROM responses')
        responses = cursor.fetchall()  # Get all responses

    # Pass the responses to the template
    return render_template('view_response.html', responses=responses)
if __name__ == '__main__':
    init_db()  # Create the database and table on startup
    app.run(debug=True)
