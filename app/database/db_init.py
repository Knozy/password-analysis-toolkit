from app import create_app, db
from app.models.user_model import (
    User,
    AnalysisRecord,
    AttackResult,
    Report,
    SystemLog
)

def init_database():
    app = create_app()

    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(username='admin').first()

        if not admin:
            admin = User(
                username='admin',
                email='admin@localhost.local',
                full_name='Administrator',
                role='admin',
                is_active=True
            )

            admin.set_password('ChangeMe123!')
            db.session.add(admin)

        demo = User.query.filter_by(username='demo').first()

        if not demo:
            demo = User(
                username='demo',
                email='demo@localhost.local',
                full_name='Demo User',
                role='user',
                is_active=True
            )

            demo.set_password('DemoPassword123!')
            db.session.add(demo)

        db.session.commit()

        print("Database initialized successfully")

if __name__ == '__main__':
    init_database()
