from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from apps import db
from apps.authentication.models import Publication, Service
from datetime import datetime
from .forms import PublicationForm
from . import blueprint
from .utils import *
from apps.replicate_utils import run_model_and_download
from flask import send_file
import os
from flask import jsonify

@blueprint.route('/')
@login_required
def list_publications():
    query = db.session.query(Publication, Service)\
        .join(Service, Publication.service_id == Service.id)

    # Filter by service
    service_id = request.args.get('service_id', type=int)
    if service_id:
        query = query.filter(Publication.service_id == service_id)

    # Filter by status
    statut = request.args.get('statut')
    if statut:
        query = query.filter(Publication.statut == statut)

    # Filter by publication date range
    date_debut = request.args.get('date_debut')
    if date_debut:
        date_debut = datetime.strptime(date_debut, '%Y-%m-%d')
        query = query.filter(Publication.date_publication >= date_debut)

    date_fin = request.args.get('date_fin')
    if date_fin:
        date_fin = datetime.strptime(date_fin, '%Y-%m-%d')
        query = query.filter(Publication.date_publication <= date_fin)

    # Filter by author
    auteur = request.args.get('auteur')
    if auteur:
        query = query.filter(Publication.auteur.ilike(f'%{auteur}%'))

    # Filter by title
    title = request.args.get('title')
    if title:
        query = query.filter(Publication.title.ilike(f'%{title}%'))

    # Execute the query
    publications = query.all()

    # Get all services for the dropdown
    services = Service.query.all()

    return render_template('back/publications/publications.html', 
                           publications=publications, 
                           services=services,
                           current_filters=request.args)

@blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_publication():
    form = PublicationForm()
    if form.validate_on_submit():
        new_publication = Publication(
            title=form.title.data,
            content=form.content.data,
            publication_date=form.publication_date.data or datetime.utcnow(),
            user_id=current_user.id,
            service_id=form.service_id.data,
            auteur=form.auteur.data or current_user.username,
            statut=form.statut.data,
            date_publication=datetime.utcnow(),
            creer_par=current_user.username,
            creer_le=datetime.utcnow(),
            chemin_image=form.chemin_image.data,
            description=form.description.data
        )
        
        db.session.add(new_publication)
        db.session.commit()
        
        flash('Publication created successfully', 'success')
        return redirect(url_for('publications_blueprint.list_publications'))
    
    return render_template('back/publications/create.html', form=form)

@blueprint.route('/<int:id>')
@login_required
def view_publication(id):
    publication = Publication.query.get_or_404(id)
    return render_template('back/publications/view.html', publication=publication)

@blueprint.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_publication(id):
    publication = Publication.query.get_or_404(id)
    form = PublicationForm(obj=publication)
    
    if form.validate_on_submit():
        form.populate_obj(publication)
        db.session.commit()
        
        flash('Publication updated successfully', 'success')
        return redirect(url_for('publications_blueprint.view_publication', id=publication.id))
    
    return render_template('back/publications/edit.html', form=form, publication=publication)

@blueprint.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_publication(id):
    publication = Publication.query.get_or_404(id)
    
    db.session.delete(publication)
    db.session.commit()
    
    flash('Publication deleted successfully', 'success')
    return redirect(url_for('publications_blueprint.list_publications'))



@blueprint.route('/download/<int:id>/<string:service>')
@login_required
def download_publication(id, service):
    publication = Publication.query.get_or_404(id)
    prompt = f"genere à ton choix soit une belle image de {publication.auteur} ou une image de {publication.title} sachant qu'il s'agit de l'image de fond de {service}"
    output_quality = 90
    local_filename = "apps/static/front/assets/img/output.webp"
    
    # Use os.path.join for proper path handling
    file_path = os.path.join(os.getcwd(), "apps", "static", "assets", "img", "vds", f"generated_{id}.png")
    
    run_model_and_download(prompt, output_quality, local_filename)

    if service == "Pensée De Saint":
        superpose_images(
            image1_path=local_filename,
            image2_path="apps/static/assets/img/vds/layer2.png",
            image3_path="apps/static/assets/img/vds/layer3.png",
            output_path="apps/static/assets/img/vds/superposed_image_pds.png",
            opacity=0.7
        )
        fnt_pensee, fnt_auteur = load_fonts_pds()

    elif service == "Pensée Du Jour":
        superpose_images(
            image1_path=local_filename,
            image2_path="apps/static/assets/img/vds/layer2_pdj.png",
            image3_path="apps/static/assets/img/vds/layer3_pdj.png",
            output_path="apps/static/assets/img/vds/superposed_image_pdj.png",
            opacity=0.7
        )
        fnt_pensee, fnt_auteur = load_fonts_pdj()

    process_quote(service=service, author=publication.auteur, text=publication.content, fnt_pensee=fnt_pensee, fnt_auteur=fnt_auteur, filepath=file_path)

    # Wait for the file to be generated
    import time
    max_wait = 30  # Maximum wait time in seconds
    wait_time = 0
    while not os.path.exists(file_path) and wait_time < max_wait:
        time.sleep(1)
        wait_time += 1

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'File generation failed or timed out'}), 500