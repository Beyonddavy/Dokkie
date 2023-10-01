from app.db import execute_query, select_all, select_one
from flask import Blueprint
from datetime import datetime


bp = Blueprint('events', __name__)


def create_event(creator_id: int, description: str, date: datetime):
    query = "INSERT INTO Event (description, eventDate, creationDate, participantId, \
        isExpired, totalAmount, paidAmount) VALUES (%s, %s, %s, %s, 0, 0, 0);"
    execute_query(query, (description, date, datetime.now(), creator_id))
    last_insert = select_one("SELECT LAST_INSERT_ID() AS id")
    return last_insert['id'] if last_insert else None


def update_event(event_id: int, description: str, date: datetime):
    query = "UPDATE Event SET description = %s, eventDate = %s WHERE eventId = %s"
    execute_query(query, (description, date, event_id))


def fetch_event(event_id):
    return select_one("SELECT * FROM Event WHERE eventId = %s", event_id)


def fetch_participants(event_id):
    query = "SELECT u.participantId, u.firstname, u.lastname \
        FROM Participant AS u INNER JOIN ParticipantEvent AS p \
        ON u.participantId = p.participantId AND p.eventId = %s"
    return select_all(query, event_id)


def fetch_candidates(event_id):
    # Find all users who are not participants of this event. They
    # are candidates for the purpose of adding new participants.
    query = "SELECT u.participantId, u.firstname, u.lastname \
        FROM Participant AS u LEFT OUTER JOIN ParticipantEvent AS p \
        ON u.participantId = p.participantId AND p.eventId = %s \
        WHERE p.eventId IS NULL"
    return select_all(query, event_id)


def add_participant(event_id, user_id):
    query = "INSERT INTO ParticipantEvent (eventId, participantId) VALUES (%s, %s)"
    execute_query(query, (event_id, user_id))


def remove_participant(event_id, user_id):
    # TO-DO: handle clean up of related transactions
    query = "DELETE FROM ParticipantEvent WHERE eventId = %s AND participantId = %s"
    execute_query(query, (event_id, user_id))


from app.events import routes
