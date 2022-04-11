"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""


from app import app
from flask import render_template, request, jsonify, send_file
import os
from app.forms import UploadForm
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf



###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###
@app.route('/api/upload', methods=['POST'])
def upload():
    form = UploadForm()   
    if request.method == "POST":
        formobj = UploadForm()
        if formobj.validate_on_submit():
            fileobj = request.files['photo']
            sanitizedname = secure_filename(fileobj.filename)
            fileobj.save(os.path.join(app.config['UPLOAD_FOLDER'], sanitizedname))
            jsonMessage= {
                "message": "File Upload Successful",
                "filename": sanitizedname,
                "description": formobj.description.data
            }
            return jsonify(jsonMessage)
        return jsonify(form_errors(formobj))
@app.route('/api/csrf-token', methods=['GET'])
def get_csrf():
 return jsonify({'csrf_token': generate_csrf()})

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

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