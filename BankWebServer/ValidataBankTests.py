import json

import pytest
from app import app, cursor, cnxn
from flask import url_for

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = '127.0.0.1:5000'
    with app.app_context():
        with app.test_client() as client:
            yield client

def test_add_bank(client):
    # POST request to /create
    response = client.post(url_for('create'), json={'name': 'Test Bank(add_bank)', 'location': 'Test Location(add_bank)'})
    assert response.status_code == 200
    assert b'Bank created successfully!' in response.data

    # Check if the bank was added to the database
    cursor.execute("SELECT * FROM banks WHERE name = 'Test Bank(add_bank)' AND location = 'Test Location(add_bank)'")
    assert (len(cursor.fetchall()) == 1 )

    # Clean up
    cursor.execute("DELETE FROM banks WHERE name = 'Test Bank(add_bank)' AND location = 'Test Location(add_bank)'")
    cnxn.commit()

def test_find(client):
    # Add a test bank
    cursor.execute("INSERT INTO banks (name, location) VALUES (?, ?)", 'Test Bank(test_find)', 'Test Location(test_find)')
    cnxn.commit()

    cursor.execute("SELECT * FROM banks WHERE name = 'Test Bank(test_find)' AND location = 'Test Location(test_find)'")
    assert (len(cursor.fetchall()) == 1 )

    response = client.get(url_for('find', name='Test Bank(test_find)'))
    assert response.status_code == 200
    assert b'Test Bank' in response.data

    # Clean up
    cursor.execute("DELETE FROM banks WHERE name = 'Test Bank(test_find)' AND location = 'Test Location(test_find)'")
    cnxn.commit()

def test_update(client):
    # Add a test bank
    cursor.execute("INSERT INTO banks (name, location) VALUES (?, ?)", 'Test Bank(test_update)', 'Test Location(test_update)')
    cnxn.commit()

    cursor.execute("SELECT * FROM banks WHERE name = 'Test Bank(test_update)' AND location = 'Test Location(test_update)'")
    assert (len(cursor.fetchall()) == 1 )

    response = client.get(url_for('find', name='Test Bank(test_update)'))
    assert response.status_code == 200
    assert b'Test Bank' in response.data
    response = client.put(url_for('update', id=json.loads(response.data)['id']), json={'name': 'Test Bank Updated', 'location': 'Test Location Updated'})
    assert response.status_code == 200
    assert b'Bank updated successfully!' in response.data

    # Check if the bank was updated
    cursor.execute("SELECT * FROM banks WHERE name = 'Test Bank Updated' AND location = 'Test Location Updated'")
    assert (len(cursor.fetchall()) == 1 )

    # Clean up
    cursor.execute("DELETE FROM banks WHERE name = 'Test Bank Updated' AND location = 'Test Location Updated'")
    cnxn.commit()

def test_delete(client):
    # Add a test bank
    cursor.execute("INSERT INTO banks (name, location) VALUES (?, ?)", 'Test Bank(test_delete)', 'Test Location(test_delete)')
    cnxn.commit()

    cursor.execute("SELECT * FROM banks WHERE name = 'Test Bank(test_delete)' AND location = 'Test Location(test_delete)'")
    assert (len(cursor.fetchall()) == 1 )

    response = client.get(url_for('find', name='Test Bank(test_delete)'))
    assert response.status_code == 200
    assert b'Test Bank' in response.data
    response = client.get(url_for('delete', id=json.loads(response.data)['id']))
    assert response.status_code == 200
    assert b'Bank deleted successfully!' in response.data

    # Check if the bank was deleted
    cursor.execute("SELECT * FROM banks WHERE name = 'Test Bank(test_delete)' AND location = 'Test Location(test_delete)'")
    assert (len(cursor.fetchall()) == 0 )

    # Clean up
    cursor.execute("DELETE FROM banks WHERE name = 'Test Bank(test_delete)' AND location = 'Test Location(test_delete)'")
    cnxn.commit()

def test_read(client):
    # Add a test bank
    cursor.execute("INSERT INTO banks (name, location) VALUES (?, ?)", 'Test Bank(test_read)', 'Test Location(test_read)')
    cnxn.commit()

    cursor.execute("SELECT * FROM banks WHERE name = 'Test Bank(test_read)' AND location = 'Test Location(test_read)'")
    assert (len(cursor.fetchall()) == 1 )

    response = client.get(url_for('read'))
    assert response.status_code == 200
    assert b'Test Bank' in response.data

    # Clean up
    cursor.execute("DELETE FROM banks WHERE name = 'Test Bank(test_read)' AND location = 'Test Location(test_read)'")
    cnxn.commit()