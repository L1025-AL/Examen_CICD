from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

class Mesaj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)

def create_app():
    app = Flask(name)

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
        f"@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        app.logger.info("Tabelele au fost create.")

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            titlu = request.form.get('titlu')
            if titlu:
                db.session.add(Mesaj(text=titlu))
                db.session.commit()
                app.logger.info(f"Titlu adaugat: {titlu}")
            return redirect('/')
        titluri = Mesaj.query.all()
        return render_template('index.html', titluri=titluri)

    return app