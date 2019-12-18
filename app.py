from web import app
from flask import render_template

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True)
