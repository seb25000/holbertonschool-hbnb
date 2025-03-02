from flask import Flask

app = Flask(__name__)

@app.route("/")  # This defines the route for the root URL
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run(debug=True)
    