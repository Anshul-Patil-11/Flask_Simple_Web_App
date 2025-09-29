from flask import Flask, url_for, request, render_template_string

# flask app instance
app = Flask(__name__)

# define root for the root url ("/")
@app.route('/')
def welcome():  # view function or endpoint
    return 'Welcome to my Flask App!'

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
        data[id] = request.get_data(as_text=True) # Assuming raw text data
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

if __name__=='__main__':
    app.run(debug=True)
