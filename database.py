# create_db.py

from app import db, app

def create_database():
    with app.app_context():
        db.create_all()
        print("Tabelas do banco de dados criadas com sucesso.")

if __name__ == "__main__":
    create_database()
