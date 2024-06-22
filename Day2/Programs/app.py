from flask import Flask

print("__name__" ,__name__)

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/welcome')
def welcome():
    return 'Welcome to Flask'
 
if __name__ == '__main__':
    app.run()