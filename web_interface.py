from flask import Flask, render_template

# Initializes flask based on the name of the file
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)