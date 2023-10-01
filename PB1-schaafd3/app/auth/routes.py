from app.auth import bp, add_user, update_user, login_required, encrypt_string
from app.db import select_all, select_one

from flask import abort, flash, redirect, render_template, url_for, g, request, session

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('emailaddress')
        phone = request.form.get('telephonenumber')
        password = request.form.get('password')
        add_user(firstname, lastname, email, 0, phone, password)
        return redirect(url_for('main.index'))

    return render_template("auth/register.html")

@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        email = request.form.get('emailaddress')
        phone = request.form.get('telephonenumber')
        # password = request.form.get('password')
        update_user(g.user['participantId'], firstname, lastname, email, email != '', phone)
        return redirect(url_for('auth.edit'))

    return render_template("auth/edit.html", user=g.user)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('emailaddress')
        password = request.form.get('password')
        password_hash = encrypt_string(password)
        print(password)

        if not email or not password:
            flash("Email en wachtwoord zijn verplicht", 'error') #error bericht voor een missende wachtwoord/email
        else:
            user = select_one(f"SELECT * FROM Participant WHERE emailaddress = '{email}' AND password_hash = '{password_hash}'")
        if user:
                session.clear()
                session['user_id'] = user['participantId']
                return redirect(url_for('events.index'))
        else: 
            flash("E-mailadres of wachtwoord onjuist", 'error') #het error bericht voor een onjuiste wachtwoord/email 
 

    return render_template("auth/login.html")
        

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


@bp.route('/users')
def users():
    users = select_all("SELECT * from Participant", None)
    return render_template("auth/users.html", users=users)
