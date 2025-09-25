from flask import Flask

# flask app instance
app = Flask(__name__)

# define root for the root url ("/")
@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__=='__main__':
    app.run(debug=True)
