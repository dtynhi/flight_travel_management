from models.monthly_report_model import MonthlyReport
from models.monthly_report_detail_model import MonthlyReportDetail
from models.yearly_report_model import YearlyReport
from app.extensions import db

class ReportService:

    @staticmethod
    def get_all_monthly_reports():
        return [r.to_dict() for r in MonthlyReport.query.all()]

    @staticmethod
    def get_monthly_report_details(report_id):
        return [r.to_dict() for r in MonthlyReportDetail.query.filter_by(report_id=report_id).all()]

    @staticmethod
    def get_yearly_reports(year=None):
        query = YearlyReport.query
        if year:
            query = query.filter_by(year=year)
        return [r.to_dict() for r in query.all()]
