from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from apps import db
from apps.authentication.models import Event
from apps.events.forms import EventForm
from . import blueprint


@blueprint.route('/events')
@login_required
def list_events():
    events = Event.query.all()
    return render_template('events/list.html', events=events)

@blueprint.route('/events/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            name=form.name.data,
            description=form.description.data,
            event_date=form.event_date.data,
            user_id=current_user.id,
            creer_par=current_user.username,
            image=form.image.data
        )
        db.session.add(event)
        db.session.commit()
        flash('Événement créé avec succès', 'success')
        return redirect(url_for('events.list_events'))
    return render_template('events/create.html', form=form)

@blueprint.route('/events/<int:id>')
@login_required
def view_event(id):
    event = Event.query.get_or_404(id)
    return render_template('events/view.html', event=event)

@blueprint.route('/events/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    event = Event.query.get_or_404(id)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        form.populate_obj(event)
        db.session.commit()
        flash('Événement mis à jour avec succès', 'success')
        return redirect(url_for('events.view_event', id=event.id))
    return render_template('events/edit.html', form=form, event=event)

@blueprint.route('/events/<int:id>/delete', methods=['POST'])
@login_required
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    flash('Événement supprimé avec succès', 'success')
    return redirect(url_for('events.list_events'))