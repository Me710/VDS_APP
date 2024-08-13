# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.replicate_utils import run_model_and_download


@blueprint.route('/index')
@login_required
def index():
    # Define the parameters
    #prompt = "faire un don pour soutenir 'Vie Des Saints'"
    #output_quality = 90
    #local_filename = "apps/static/front/assets/img/output.webp"  
    #run_model_and_download(prompt, output_quality, local_filename)
    return render_template('front/home/index.html', segment='index')

@blueprint.route('/back')
@login_required
def back():
    return render_template('back/home/index.html', segment='back')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("back/home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('back/home/page-404.html'), 404

    except:
        return render_template('back/home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
