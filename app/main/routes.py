from flask import Blueprint, render_template, session, request, redirect, url_for
from app.main import main

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        if client_id:    
            session['client_id'] = client_id
        session['action'] = request.form['action']
        if session['action'] == 'backup':
            return redirect(url_for('spotify.backup_options'))
        elif session['action'] == 'auto_like':
            return redirect(url_for('spotify.upload_like'))
    return render_template('index.html')
