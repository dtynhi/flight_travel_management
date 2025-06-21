from app.extensions import db

class MonthlyReport(db.Model):
    __tablename__ = 'tbl_monthly_reports'

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    total_tickets_sold = db.Column(db.Integer, nullable=False)
    total_revenue = db.Column(db.Numeric(15), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime)
    deletion_status = db.Column(db.String, nullable=False, default='active')

    def to_dict(self):
        return {
            'id': self.id,
            'month': self.month,
            'year': self.year,
            'total_tickets_sold': self.total_tickets_sold,
            'total_revenue': float(self.total_revenue),
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deletion_status': self.deletion_status
        }
