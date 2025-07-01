# services/app/report_service.py
from models.monthly_report_model import MonthlyReport
from models.monthly_report_detail_model import MonthlyReportDetail
from models.yearly_report_model import YearlyReport
from app.extensions import db


class ReportService:

    @staticmethod
    def get_all_monthly_reports(year=None, month=None):
        query = MonthlyReport.query
        if year is not None:
            query = query.filter_by(year=year)
        if month is not None:
            query = query.filter_by(month=month)
        reports = query.all()
        result = []
        for r in reports:
            # Lấy chi tiết báo cáo tháng tương ứng
            details = MonthlyReportDetail.query.filter_by(report_id=r.id).all()
            # Nếu có chi tiết, lấy tỉ lệ (percentage) đầu tiên (hoặc tính toán nếu cần)
            percentage = details[0].percentage if details else None
            d = r.to_dict()
            d["percentage"] = float(percentage) if percentage is not None else None
            result.append(d)
        return result

    @staticmethod
    def get_monthly_report_details(report_id):
        return [
            r.to_dict()
            for r in MonthlyReportDetail.query.filter_by(report_id=report_id).all()
        ]

    @staticmethod
    def get_monthly_report_details_by_month_year(year, month):
        # Lấy báo cáo tháng theo năm/tháng
        report = MonthlyReport.query.filter_by(year=year, month=month).first()
        if not report:
            return []
        return [
            r.to_dict()
            for r in MonthlyReportDetail.query.filter_by(report_id=report.id).all()
        ]

    @staticmethod
    def get_yearly_reports(year=None):
        query = YearlyReport.query
        if year:
            query = query.filter_by(year=year)
        return [r.to_dict() for r in query.all()]
