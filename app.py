from flask import Flask

# flask app instance
app = Flask(__name__)

# define root for the root url ("/")
@app.route('/')
def welcome():
    return 'Welcome to my Flask App!'

# String Route
@app.route('/greet/<name>')
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

@app.route('/showpath/<path:subpath>')
def showpath(subpath):
    return f'The path you have entered is {subpath}'

if __name__=='__main__':
    app.run(debug=True)
