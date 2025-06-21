from app.extensions import db

class YearlyReport(db.Model):
    __tablename__ = 'tbl_yearly_reports'

    year = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, primary_key=True)
    number_of_flights = db.Column(db.Integer, nullable=False)
    total_revenue = db.Column(db.Numeric(15), nullable=False)
    percentage = db.Column(db.Numeric(3, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime)
    deletion_status = db.Column(db.String, nullable=False, default='active')

    def to_dict(self):
        return {
            'year': self.year,
            'month': self.month,
            'number_of_flights': self.number_of_flights,
            'total_revenue': float(self.total_revenue),
            'percentage': float(self.percentage),
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deletion_status': self.deletion_status
        }
