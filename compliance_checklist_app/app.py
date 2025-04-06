from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'segredo-simples'

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    respostas = json.loads(request.form["respostas"])
    with open("respostas.txt", "a", encoding="utf-8") as f:
        f.write(json.dumps(respostas, ensure_ascii=False) + "\n")
    return "Checklist submetido com sucesso!"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin":
            session["user"] = "admin"
            return redirect("/admin")
        return "Credenciais inválidas"
    return render_template("login.html")

@app.route("/admin")
def admin():
    if session.get("user") != "admin":
        return redirect("/login")
    linhas = []
    try:
        with open("respostas.txt", "r", encoding="utf-8") as f:
            for line in f:
                linhas.append(json.loads(line.strip()))
    except FileNotFoundError:
        pass
    return render_template("admin.html", respostas=linhas)

if __name__ == "__main__":
    app.run(debug=True)
