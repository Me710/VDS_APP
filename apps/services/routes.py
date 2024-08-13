from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from apps import db
from apps.authentication.models import Service
from apps.services.forms import ServiceForm
from . import blueprint



@blueprint.route('/')
@login_required
def list_services():
    services = Service.query.all()
    return render_template('back/services/services.html', services=services)

@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_service():
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(
            name=form.name.data,
            description=form.description.data,
            acronyme=form.acronyme.data,
            responsable=form.responsable.data,
            saint_patron=form.saint_patron.data,
            creer_le=form.creer_le.data,
            creer_par=form.creer_par.data,
            horaire_standard=form.horaire_standard.data,
            image=form.image.data
        )
        try:
            db.session.add(service)
            db.session.commit()
            flash('Service créé avec succès', 'success')
            return redirect(url_for('services_blueprint.list_services'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la création du service: {str(e)}', 'danger')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Erreur dans le champ {getattr(form, field).label.text}: {error}", 'danger')
    
    return render_template('back/services/create.html', form=form)

@blueprint.route('/<int:id>')
@login_required
def view_service(id):
    service = Service.query.get_or_404(id)
    return render_template('back/services/view.html', service=service)

@blueprint.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_service(id):
    service = Service.query.get_or_404(id)
    form = ServiceForm(obj=service)
    if form.validate_on_submit():
        form.populate_obj(service)
        db.session.commit()
        flash('Service mis à jour avec succès', 'success')
        return redirect(url_for('services_blueprint.view_service', id=service.id))
    return render_template('back/services/edit.html', form=form, service=service)

@blueprint.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash('Service supprimé avec succès', 'success')
    return redirect(url_for('services_blueprint.list_services'))