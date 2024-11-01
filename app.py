import os
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Altere para um valor seguro
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    rating = db.Column(db.String(10), nullable=True)  # Nota do filme

    def __repr__(self):
        return "<Title: {}, Rating: {}>".format(self.title, self.rating)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        title = request.form.get("title")
        rating = request.form.get("rating")
        if title:
            try:
                book = Book(title=title, rating=rating)
                db.session.add(book)
                db.session.commit()
                flash("Filme adicionado com sucesso!", "success")
            except Exception as e:
                flash("Falha ao adicionar filme: {}".format(e), "danger")
        else:
            flash("O título do filme não pode estar vazio.", "warning")
    
    books = Book.query.all()
    return render_template("index.html", movies=books)

@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    if newtitle and oldtitle:
        book = Book.query.filter_by(title=oldtitle).first()
        if book:
            book.title = newtitle
            db.session.commit()
            flash("Filme atualizado com sucesso!", "success")
        else:
            flash("Filme não encontrado.", "warning")
    else:
        flash("Título antigo e novo são necessários.", "warning")
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        flash("Filme excluído com sucesso!", "success")
    else:
        flash("Filme não encontrado.", "warning")
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
