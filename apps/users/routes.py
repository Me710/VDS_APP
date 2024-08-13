from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from apps import db
from apps.authentication.models import Users
from apps.users.forms import UserForm
from . import blueprint

@blueprint.route('/users')
@login_required
def list_users():
    users = Users.query.all()
    return render_template('users/list.html', users=users)

@blueprint.route('/users/create', methods=['GET', 'POST'])
@login_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = Users(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            adresse=form.adresse.data,
            ville=form.ville.data,
            pays=form.pays.data,
            bio=form.bio.data,
            pp=form.pp.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Utilisateur créé avec succès', 'success')
        return redirect(url_for('users.list_users'))
    return render_template('users/create.html', form=form)

@blueprint.route('/users/<int:id>')
@login_required
def view_user(id):
    user = Users.query.get_or_404(id)
    return render_template('users/view.html', user=user)

@blueprint.route('/users/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = Users.query.get_or_404(id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash('Utilisateur mis à jour avec succès', 'success')
        return redirect(url_for('users.view_user', id=user.id))
    return render_template('users/edit.html', form=form, user=user)

@blueprint.route('/users/<int:id>/delete', methods=['POST'])
@login_required
def delete_user(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('Utilisateur supprimé avec succès', 'success')
    return redirect(url_for('users.list_users'))