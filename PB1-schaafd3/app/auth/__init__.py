from flask import Blueprint, redirect, url_for, session, g
from app.db import execute_query, select_one
import functools
import hashlib
bp = Blueprint('auth', __name__)

def encrypt_string(hash_string):
    sha_signature = \
    hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature
def add_user(firstname, lastname, email, organizer, phone, password):
    print(password)
    password_hash = encrypt_string(password)
    query = "INSERT INTO Participant (firstname, lastname, emailaddress, \
        isOrganizer, telephonenumber, password_hash) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (firstname, lastname, email, organizer, phone, password_hash)
    execute_query(query, values)

def update_user(id, firstname, lastname, email, organizer, phone):
    query = "UPDATE Participant SET firstname = %s, lastname = %s, emailaddress = %s, \
        isOrganizer = %s, telephonenumber = %s WHERE participantId = %s"
    values = (firstname, lastname, email, organizer, phone, id)
    execute_query(query, values)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is not None:
        g.user = select_one("SELECT * FROM Participant WHERE participantId = %s", user_id)
    else:
        g.user = None

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

from app.auth import routes