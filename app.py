from flask import Flask, url_for, request

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

if __name__=='__main__':
    app.run(debug=True)
