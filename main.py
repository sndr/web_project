from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/HTML/login.html")
def login():
    return render_template("login.html")

@app.route("/HTML/manutencao.html")
def manutenção():
    return render_template("manutencao.html")

@app.route("/HTML/remocao.html")
def remoção():
    return render_template("remocao.html")

@app.route("/HTML/instalacao.html")
def instalação():
    return render_template("instalacao.html")

if __name__ == '__main__':
    app.run(debug=True)