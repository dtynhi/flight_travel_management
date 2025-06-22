from flask import Blueprint, request, jsonify
from services.app.report_service import ReportService
from payload.api_response import SuccessApiResponse

report_bp = Blueprint('report', __name__)

@report_bp.route('/monthly', methods=['GET'])
def get_monthly_reports():
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    data = ReportService.get_all_monthly_reports(year=year, month=month)
    return jsonify(SuccessApiResponse(data=data).__dict__)

@report_bp.route('/monthly/<int:report_id>/details', methods=['GET'])
def get_monthly_report_details(report_id):
    data = ReportService.get_monthly_report_details(report_id)
    return jsonify(SuccessApiResponse(data=data).__dict__)

@report_bp.route('/yearly', methods=['GET'])
def get_yearly_reports():
    year = request.args.get('year', type=int)
    data = ReportService.get_yearly_reports(year)
    return jsonify(SuccessApiResponse(data=data).__dict__)