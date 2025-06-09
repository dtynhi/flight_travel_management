from typing import Dict, Any, Optional
from utils.date_time_utils import DateTimeUtils


class BaseFilter:
    def __init__(self, request_params: Dict[str, Any] = None):
        params = request_params or {}     
        # Default pagination parameters
        self.page = self.parse_str_to_int(params.get('page', '0'))
        self.pageSize = self.parse_str_to_int(params.get('pageSize', '100'))      
        # Default time range parameters
        self.from_time = None
        self.to_time = None     
        # Default time range parameters: check if the params contain the keys 'from' and 'to'
        if params.get('from'):
            self.from_time = self.parse_str_to_datetime(params.get('from'))
        if params.get('to'):
            self.to_time = self.parse_str_to_datetime(params.get('to'))
        # Default search and sort parameters
        self.query = params.get('query', None)
        self.sort = params.get('sort', None)
        self.order = self.parse_str_to_order(params.get('order', 'ASC'))
    
    def parse_str_to_int(self, value: str) -> int:
        try:
            return int(value)
        except Exception as error:
            print(f"Error in parse_str_to_int: {error}")
            return 0
    
    def parse_str_to_datetime(self, value: str) -> int:
        return DateTimeUtils.parse_str_to_timestamp(value)
    
    def parse_str_to_order(self, value: str) -> str:
        if value and value.upper() in ['ASC', 'DESC']:
            return value.upper()
        return 'ASC'
        
    def build(self) -> Dict[str, Any]:
        return {}
    
    def get_limit(self) -> int:
        return self.pageSize
    
    def get_offset(self) -> int:
        return self.page * self.pageSize
    
    def get_order_by(self) -> Optional[str]:
        if not self.sort:
            return None 
        return f"{self.sort} {self.order}"
    
    def get_time_range(self) -> Dict[str, Any]:
        time_range = {}    
        if self.from_time is not None:
            time_range['from'] = self.from_time      
        if self.to_time is not None:
            time_range['to'] = self.to_time         
        return time_range
    
class ApprovalInstanceFilter(BaseFilter):
    def __init__(self, request_params: Dict[str, Any] = None):
        super().__init__(request_params or {})
        params = request_params or {}
        
        # Approval filters
        self.approval_id = self.parse_str_to_int(params.get('approval_id', '0'))
        self.approval_code = params.get('approval_code')
        
        # Time range filters
        self.start_at = None
        self.end_at = None
        if params.get('start_at'):
            self.start_at = DateTimeUtils.parse_date_time_str_to_timestamp(params.get('start_at'))
        if params.get('end_at'):
            self.end_at = DateTimeUtils.parse_date_time_str_to_timestamp(params.get('end_at'))
        
        # Other filters
        self.serial_no = params.get('serial_no')
        self.status = params.get('status')
        self.approval_by = params.get('approval_by')
        
        # Tracked status
        self.is_tracked = None
        if 'is_tracked' in params:
            is_tracked_str = params.get('is_tracked', '').lower()
            if is_tracked_str in ['true', 'false']:
                self.is_tracked = is_tracked_str == 'true'
    
    def build(self) -> Dict[str, Any]:
        """Build a dict of filter parameters for API calls"""
        result = super().build()
        
        if self.approval_id:
            result['approval_id'] = self.approval_id
        if self.approval_code:
            result['approval_code'] = self.approval_code
        if self.start_at:
            result['start_at'] = self.start_at
        if self.end_at:
            result['end_at'] = self.end_at
        if self.serial_no:
            result['serial_no'] = self.serial_no
        if self.status:
            result['status'] = self.status
        if self.approval_by:
            result['approval_by'] = self.approval_by
        if self.is_tracked is not None:
            result['is_tracked'] = 'true' if self.is_tracked else 'false'
        
        return result