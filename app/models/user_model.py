from app import db
from datetime import datetime
import bcrypt
from datetime import datetime
import bcrypt


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    role = db.Column(db.String(20), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    analysis_records = db.relationship('AnalysisRecord', backref='user', lazy=True)
    attack_results = db.relationship('AttackResult', backref='user', lazy=True)
    reports = db.relationship('Report', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    def __repr__(self):
        return f'<User {self.username}>'


class AnalysisRecord(db.Model):
    __tablename__ = 'analysis_records'

    record_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    password_tested = db.Column(db.String(255))
    password_length = db.Column(db.Integer)
    character_types = db.Column(db.String(50))
    entropy_value = db.Column(db.Float)
    strength_score = db.Column(db.Integer)
    strength_level = db.Column(db.String(20))
    time_to_crack_seconds = db.Column(db.BigInteger)
    time_to_crack_human = db.Column(db.String(100))
    is_common_password = db.Column(db.Boolean)
    improvement_suggestions = db.Column(db.Text)
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AnalysisRecord {self.record_id}>'

class AttackResult(db.Model):
    __tablename__ = 'attack_results'

    attack_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    attack_type = db.Column(db.String(20))
    target_password_hash = db.Column(db.String(255))
    wordlist_size = db.Column(db.Integer)
    match_found = db.Column(db.Boolean)
    attempts_made = db.Column(db.Integer)
    time_taken_seconds = db.Column(db.Float)
    success_rate = db.Column(db.Float)
    vulnerability_score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Report(db.Model):
    __tablename__ = 'reports'

    report_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    report_title = db.Column(db.String(255))
    report_type = db.Column(db.String(20))
    content_path = db.Column(db.String(255))
    analysis_records_count = db.Column(db.Integer)
    total_weak_passwords = db.Column(db.Integer)
    total_strong_passwords = db.Column(db.Integer)
    overall_security_score = db.Column(db.Float)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemLog(db.Model):
    __tablename__ = 'system_logs'

    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    event_type = db.Column(db.String(50))
    event_description = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    status = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
