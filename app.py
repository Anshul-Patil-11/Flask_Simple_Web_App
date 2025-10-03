from flask import Flask, url_for, request, render_template_string, jsonify

# flask app instance
app = Flask(__name__)

# define root for the root url ("/")
@app.route('/')
def welcome():  # view function or endpoint
    return 'Welcome to my Flask App!'

# Type Conversion:

# Flask supports several type converters:

#     string (default): Accepts any text without a slash.
#     int: Accepts positive integers.
#     float: Accepts floating-point numbers.
#     path: Accepts any text including slashes.
#     uuid: Accepts UUID strings.


# String Route
@app.route('/greet/<name>') # Dynamic URL
def greet(name):
    return f'Hello {name}!'

# Add Route
@app.route('/add/<int:num1>/<int:num2>')
def add(num1,num2):
    return str(num1+num2)

# Float Route
@app.route('/square/<float:num>')
def square(num):
    return f'The square of {num} is {str(num*num)}'

# Path ROute
@app.route('/showpath/<path:subpath>')
def showpath(subpath):
    return f'The path you have entered is {subpath}'

# URL For
with app.test_request_context():
    print(url_for('greet',name='Anshul'))

# Handling Get Requests
@app.route('/query', methods=['GET'])
def query_example():
    # Accessing URL arguments
    name = request.args.get('name')
    age = request.args.get('age')

    if name and age:
        return f"Hello {name}, you are {age} years old."
    else:
        return "Please provide both name and age in the query string."

    # works with this url http://127.0.0.1:5000/query?name=Anshul&age=23

# Handling Post Requests
# HTML for demo
HTML_FORM = """
<form method="post">
    <label for="name">Name:</label><br>
    <input type="text" id="name" name="name"><br><br>
    <label for="age">Age:</label><br>
    <input type="number" id="age" name="age"><br><br>
    <input type="submit" value="Submit">
</form>
"""

@app.route('/form', methods = ['GET','POST'])
def form():
    if request.method=='POST':
        name = request.form['name']
        age = request.form['age']
        return f'Hello {name}, you are {age} years old!'
    else:
        return render_template_string(HTML_FORM)

# Handling Put and Delete Requests   
data = {'1': 'Item 1'} # Sample data store

@app.route('/item/<id>', methods=['GET','PUT', 'DELETE'])
def manage_item(id):
    if request.method == 'PUT':
        data[id] = request.get_data(as_text=True) # Assuming raw text data (after '-d')
        return f"Item {id} updated to {data[id]}"
    elif request.method == 'GET':
        if id in data:
            return f'The Item id is {id} and item is {data[id]}'
        else:
            return f'Item {id} not found!', 404
    elif request.method == 'DELETE':
        if id in data:
            del data[id]
            return f"Item {id} deleted"
        else:
            return f"Item {id} not found", 404
    else:
        return "Method not allowed", 405
    
#     # Update (PUT)
# curl -X PUT http://127.0.0.1:5000/item/1 -d 'Updated Item 1'
# # → Item 1 updated to Updated Item 1

# # Read (GET)
# curl http://127.0.0.1:5000/item/1
# # → The Item id is 1 and item is Updated Item 1

# # Delete (DELETE)
# curl -X DELETE http://127.0.0.1:5000/item/1
# # → Item 1 deleted

# # Read again (GET after delete)
# curl http://127.0.0.1:5000/item/1
# # → Item 1 not found!

@app.route('/api/data', methods=['POST'])
def receive_json():
    if request.is_json:
        data = request.get_json()
        # print(data) # For debugging
        return jsonify({"message": "Data received successfully!", "data": data}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400

# # Send JSON with POST
# curl -v -X POST -H "Content-Type: application/json" \
# -d '{"name": "John", "age": 30}' \
# http://localhost:5000/api/data

# {
#   "data": {
#     "age": 30,
#     "name": "John"
#   },
#   "message": "Data received successfully!"
# }

# Accessing Files

import os
from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename

# -----------------------------
# 1) Configuration for uploads
# -----------------------------

# Folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'

# Allowed file extensions for security reasons
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Store the upload folder in Flask's configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it does not exist yet
# exist_ok=True prevents error if folder already exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------------------
# 2) Helper function to validate file type
# -----------------------------------------

def allowed_file(filename):
    """
    Check if the file has a valid extension.

    Returns True if:
      - There is a dot in the filename (has an extension)
      - The extension (after the last dot) is in ALLOWED_EXTENSIONS
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------------------------------
# 3) HTML form for file uploads
# ---------------------------------

HTML_FORM = """
<form method="post" enctype="multipart/form-data">
    <!-- File picker input -->
    <input type="file" name="file"><br><br>
    <!-- Submit button -->
    <input type="submit" value="Upload">
</form>
"""

# --------------------------------------------------
# 4) Flask route to handle GET and POST requests
# --------------------------------------------------

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """
    Handles file upload requests:
    - GET: shows the HTML form
    - POST: processes the uploaded file
    """
    if request.method == 'POST':
        # Check if 'file' field is in request.files
        # If not, user did not submit a file
        if 'file' not in request.files:
            return 'No file part'

        # Retrieve the file from request.files dictionary
        file = request.files['file']

        # Check if user selected a file (filename will be empty if not)
        if file.filename == '':
            return 'No selected file'

        # Check if file exists and has allowed extension
        if file and allowed_file(file.filename):
            # Sanitize the filename to prevent directory traversal attacks
            filename = secure_filename(file.filename)

            # Save the file to the configured upload folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Success message
            return 'File uploaded successfully'
        else:
            # File exists but extension is not allowed
            return 'File type not allowed'

    # If GET request, render the HTML form
    return render_template_string(HTML_FORM)

# HTTP Error Codes

from flask import Flask, abort

# app = Flask(__name__)

@app.route('/user/<id>')
def get_user(id):
    users = {'1': 'John', '2': 'Jane', '3': 'Peter'}
    if id not in users:
        abort(404) # Raises a 404 exception
        # return f'User {id} not found!',404
        
    return f"User: {users[id]}"

# CUSTOM ERROR HANDLERS

from flask import Flask, render_template_string

# app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    return render_template_string("<h1>Page Not Found</h1><p>The requested URL was not found on the server.</p>"), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template_string("<h1>Internal Server Error</h1><p>An unexpected error occurred on the server.</p>"), 500

@app.route('/error')
def generate_error():
    raise Exception("This is a test error")

# -------------------------------
# 5) Run the Flask application
# -------------------------------


if __name__ == '__main__':
    app.run(debug=True)
