from app.auth import login_required
from app.db import execute_query, select_all, select_one
from app.events import bp, create_event, update_event, add_participant, remove_participant, fetch_event
from app.events import fetch_participants, fetch_candidates
from flask import abort, redirect, render_template, url_for, request, session
from datetime import datetime


@bp.route('/')
@login_required
def index():
    events = select_all("SELECT * FROM Event WHERE participantId = %s", session['user_id'])
    return render_template("events/index.html", events=events)


@bp.route('/view/<int:event_id>')
@login_required
def view_page(event_id):
    event = fetch_event(event_id) or abort(404)
    participants = fetch_participants(event_id)
    candidates = fetch_candidates(event_id)
    return render_template('events/view.html', event=event, participants=participants, candidates=candidates)


@bp.route('/create')
@login_required
def create_page():
    return render_template('events/create.html')


@bp.route('/create', methods=['POST'])
@login_required
def create_request():
    description = request.form['description']
    date = datetime.fromisoformat(request.form['date'])
    event_id = create_event(session['user_id'], description, date)
    if not event_id:
        return redirect(url_for('events.index'))
    add_participant(event_id, session['user_id'])
    return redirect(url_for('events.view_page', event_id=event_id))


@bp.route('/edit/<int:event_id>')
@login_required
def edit_page(event_id):
    event = fetch_event(event_id) or abort(404)
    return render_template('events/edit.html', event=event)


@bp.route('/edit/<int:event_id>', methods=['POST'])
@login_required
def edit_request(event_id):
    event = fetch_event(event_id) or abort(404)
    if event['participantId'] != session['user_id']:
        abort(403)
    description = request.form['description']
    date = datetime.fromisoformat(request.form['date'])
    update_event(event_id, description, date)
    return redirect(url_for('events.view_page', event_id=event_id))


@bp.route('/add-participant', methods=['POST'])
@login_required
def add_participant_request():
    event_id = request.form['event_id']
    user_id = request.form['user_id']
    event = fetch_event(event_id) or abort(422)
    if event['participantId'] != session['user_id']:
        abort(403)
    add_participant(event_id, user_id)
    return redirect(url_for('events.view_page', event_id=event_id))


@bp.route('/remove-participant')
@login_required
def remove_participant_request():
    event_id = request.args['event_id']
    user_id = request.args['user_id']
    event = fetch_event(event_id) or abort(422)
    if event['participantId'] != session['user_id']:
        abort(403)
    remove_participant(event_id, user_id)
    return redirect(url_for('events.view_page', event_id=event_id))
