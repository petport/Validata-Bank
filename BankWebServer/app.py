from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import pyodbc

app = Flask(__name__)

# This is a bad practice, just for the sake of the example
app.config['SECRET_KEY'] = 'your-secret-key'

class BankForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Add Bank')

# connect to the database
# Hardcoded values for the sake of the example
server = 'PETROS-DESKTOP\\SQLEXPRESS'
database = 'ValidataBank'
username = 'PETROS-DESKTOP\\Petros'
Authentication = 'Windows Authentication'
driver = '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect(
    'DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';Trusted_Connection=yes;')

cursor = cnxn.cursor()

# make sure the connection is working
# by printing the SQL Server version
cursor.execute("SELECT @@version;")
row = cursor.fetchone()
print(row)


@app.route('/add', methods=['GET', 'POST'])
def add_bank():
    form = BankForm()
    if form.validate_on_submit():
        name = form.name.data
        location = form.location.data
        cursor.execute("INSERT INTO banks (name, location) VALUES (?, ?)", name, location)
        cnxn.commit()
        return {'message': 'Bank created successfully!'}
    return render_template('add_bank.html', form=form)


# route to create a new bank using JSON
@app.route('/create', methods=['POST'])
def create():
    # get the JSON data
    data = request.json

    # insert the new bank into the database
    cursor.execute("INSERT INTO banks (name, location) VALUES (?, ?)", data['name'], data['location'])
    cnxn.commit()

    # return a success message
    return {'message': 'Bank created successfully!'}

# route to read a specific bank by ID
@app.route('/read/<id>')
def read_one(id):
    # get the bank from the database
    cursor.execute("SELECT * FROM banks WHERE id = ?", id)

    # if the bank does not exist, return an error message
    if cursor.rowcount == 0:
        return {'message': 'Bank not found!'}, 404
    bank = cursor.fetchone()

    columns = [column[0] for column in cursor.description]
    result = dict(zip(columns, bank))

    # return the bank as JSON
    return result


# route to read all banks and return them as JSON
@app.route('/read')
def read():
    cursor.execute("SELECT * FROM banks")
    banks = cursor.fetchall()

    columns = [column[0] for column in cursor.description]
    results = []
    for row in banks:
        results.append(dict(zip(columns, row)))

    return results

# Update a bank by ID
@app.route('/update/<id>', methods=['PUT'])
def update(id):
    # get the JSON data
    data = request.json

    # update the bank in the database
    cursor.execute("UPDATE banks SET name = ?, location = ? WHERE id = ?", data['name'], data['location'], id)
    cnxn.commit()

    # return a success message
    return {'message': 'Bank updated successfully!'}

# Delete a bank by ID
@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    # delete the bank from the database
    cursor.execute("DELETE FROM banks WHERE id = ?", id)
    cnxn.commit()

    if cursor.rowcount == 0:
        return {'message': 'Bank not found!'}, 404

    # return a success message
    return {'message': 'Bank deleted successfully!'}

# find a bank id by name
@app.route('/find/<name>', methods=['GET'])
def find(name):
    cursor.execute("SELECT * FROM banks WHERE name = ?", name)

    if cursor.rowcount == 0:
        return {'message': 'Bank not found!'}, 404

    bank = cursor.fetchone()
    columns = [column[0] for column in cursor.description]
    result = dict(zip(columns, bank))

    return result

if __name__ == '__main__':
    app.run()