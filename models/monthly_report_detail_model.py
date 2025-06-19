from app.extensions import db

class MonthlyReportDetail(db.Model):
    __tablename__ = 'tbl_monthly_report_details'

    flight_id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, primary_key=True)
    tickets_sold = db.Column(db.Integer, nullable=False)
    revenue = db.Column(db.Numeric(15), nullable=False)
    percentage = db.Column(db.Numeric(3, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime)
    deletion_status = db.Column(db.String, nullable=False, default='active')

    def to_dict(self):
        return {
            'flight_id': self.flight_id,
            'report_id': self.report_id,
            'tickets_sold': self.tickets_sold,
            'revenue': float(self.revenue),
            'percentage': float(self.percentage),
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deletion_status': self.deletion_status
        }
