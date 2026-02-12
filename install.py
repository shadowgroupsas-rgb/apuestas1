import sys
import os
from app import app, db, User

def install():
    if os.path.exists('sports_ai.db'):
        print("La base de datos ya existe. Si quieres reinstalar, elimina 'sports_ai.db'.")
        # Ask for confirmation? No, let's just create if not exists or update.

    with app.app_context():
        print("Creando tablas de base de datos...")
        db.create_all()

        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Creando usuario Super Admin...")
            admin = User(username='admin', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Usuario 'admin' creado con contraseña 'admin123'.")
        else:
            print("El usuario 'admin' ya existe.")

    print("Instalación completada correctamente.")

if __name__ == '__main__':
    install()
