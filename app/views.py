"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
from app import app
from app.property_form import PropertyForm
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import psycopg2


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

def connect_db():
    return psycopg2.connect(host="localhost", database="proj", user="proj", password="masterjdh21")

@app.route('/property', methods=['GET', 'POST'])
def prop():
    form = PropertyForm()
    if request.method == "POST" and form.validate_on_submit():
        title = form.title.data
        numBathroom = form.numBathroom.data
        numBedroom = form.numBedroom.data
        location = form.location.data
        price = form.price.data
        description = form.description.data
        propertyType = form.propertyType.data

        upload = request.files['photo']
        filename = secure_filename(upload.filename)
        upload.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        ))

        db = connect_db()
        cur = db.cursor()
        cur.execute('insert into property_profiles (title, numbathroom, numbedroom, location, price, description, propertyType, filename) values (%s, %s, %s, %s, %s, %s, %s, %s)', (title, numBathroom, numBedroom, location, price, description, propertyType, filename))
        db.commit()

        flash('Added successfully,','success')
        return redirect(url_for('properties'))
    return render_template('property.html', form=form)

@app.route('/properties')
def properties():
    db = connect_db()
    cur = db.cursor()
    cur.execute('select * from property_profiles')
    profiles = cur.fetchall()
    '''lst = []
    for i in profiles:

    file_list = get_uploaded_images()'''

    return render_template('properties.html', profiles=profiles)

@app.route('/properties/<propertyid>')
def property_id(propertyid):
    db = connect_db()
    cur = db.cursor()
    query = 'select * from property_profiles where id=' + propertyid
    cur.execute(query)
    profile = cur.fetchall()

    return render_template('view_property.html', propertyid=profile)

@app.route('/uploads/<filename>')
def get_property(filename):
    root_dir = os.getcwd()

    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), filename)

def get_uploaded_images():
    rootdir = os.getcwd()
    lst = []
    for subdir, dirs, files in os.walk(rootdir + '/uploads'):
        for file1 in files:
            lst.append(file1)
    
    '''if(not(lst==[])):
        lst.pop(0)'''

    return lst

###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
