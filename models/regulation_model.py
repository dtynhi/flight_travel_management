from app.extensions import db

class Regulation(db.Model):
    __tablename__ = 'regulations'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)      # ví dụ: QD1.total_airports
    value = db.Column(db.String(255), nullable=False)                 # lưu giá trị dạng chuỗi
    description = db.Column(db.String(255), nullable=True)
