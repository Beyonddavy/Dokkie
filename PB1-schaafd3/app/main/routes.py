from app.main import bp

from flask import request, render_template, url_for, redirect, g
from app.event import Event

from app.auth import login_required
from app.db import select_all, select_one, execute_query
from app.events import fetch_participants

@bp.route('/')
def index():
    return render_template("index.html")

def get_transactions_for_organizer(user_id):
    query = "SELECT e.description, e.eventDate, e.totalAmount, e.paidAmount, t.description AS type, \
        u.firstname, u.lastname, x.expenditureId, x.amount, x.isPaid FROM ParticipantEvent AS p \
        JOIN Participant      AS u ON p.participantId = u.participantId \
        JOIN Event            AS e ON p.eventId = e.eventId \
        JOIN Expenditure      AS x ON p.ParticipantEventId = x.ParticipantEventId \
        JOIN TransactionType  AS t ON x.transactionTypeId = t.typeId \
        WHERE e.participantId = %s"
    return select_all(query, user_id)

@bp.route('/mypayments')
@login_required
def mypayments():
    transactions = get_transactions_for_organizer(g.user['participantId'])
    return render_template("overViewPayments.html", transactions=transactions)

def send_reminder(transactionId: str) -> None:
    query = "SELECT e.amount, u.firstname, u.telephonenumber FROM Expenditure AS e \
        INNER JOIN ParticipantEvent AS p ON e.ParticipantEventId = p.ParticipantEventId \
        INNER JOIN Participant AS u ON p.participantId = u.participantId \
        WHERE expenditureId = %s"
    data = select_one(query, transactionId)
    if data:
        message = f"Beste {data['firstname']}, je dient nog het volgende bedrag te betalen: {data['amount']}."
        print(message)
        # pwk.sendwhatmsg_instantly(data['telephonenumber'], message, 10, True, 2)

@bp.route('/transaction_notify/<int:id>')
@login_required
def transaction_notify(id):
    send_reminder(id)
    return render_template('WhatsAppMessage.html')

@bp.route('/transaction_settle/<int:id>')
@login_required
def transaction_settle(id):
    query = "UPDATE Expenditure SET isPaid = %s WHERE expenditureId = %s"
    execute_query(query, (True, id))
    Event.addAmountToPaidAmount(id)
    return redirect(url_for('main.mypayments'))

def create_expenditure(event_id, user_id, amount, description):
    lender_query = "SELECT ParticipantEventId AS id FROM ParticipantEvent \
        WHERE eventId = %s AND participantId = %s"
    lender = select_one(lender_query, (event_id, user_id))
    if not lender:
        raise Exception(f"user {user_id} cannot create expenditure for event {event_id}")

    expenditure_query = "INSERT INTO Expenditure (ParticipantEventId, amount, \
        transactionTypeId, description, isPaid) VALUES (%s, %s, %s, %s, %s)"
    execute_query(expenditure_query, (lender['id'], amount, 'U', description, True))

    # distribute expenditure among participants
    borrowers_query = "SELECT ParticipantEventId AS id FROM ParticipantEvent \
        WHERE eventId = %s AND participantId <> %s"
    borrowers = select_all(borrowers_query, (event_id, user_id))
    split_amount = amount / (len(borrowers) + 1)
    for borrower in borrowers:
        execute_query(expenditure_query, (borrower['id'], split_amount, 'P', description, False))

@bp.route('/transaction/<int:event_id>', methods=['GET','POST'])
def add_expense(event_id):
    if request.method == 'POST':
        user_id = request.form['user_id']
        description = request.form['description']
        amount = float(request.form['amount'])
        create_expenditure(event_id, user_id, amount, description)
        return redirect(url_for('main.add_expense', event_id=event_id))

    participants = fetch_participants(event_id)
    return render_template('transaction.html', participants=participants)

@bp.route('/about')
def about():
    return render_template("html_sample.html")