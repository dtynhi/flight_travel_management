from datetime import datetime, timedelta

import pytz


class DateTimeUtils:
    DATE_TIME_PATTERN = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def now():
        timezone = pytz.timezone('Asia/Ho_Chi_Minh')
        return datetime.now(timezone)

    @staticmethod
    def parse_str_to_timestamp(value: str) -> int:
        try:
            return int(value) // 1000
        except Exception as error:
            print(f"Error in parse_str_to_timestamp: {error}")
            return 0

    @staticmethod
    def parse_date_time_str_to_timestamp(value: str) -> int:
        try:
            return int(datetime.strptime(value, DateTimeUtils.DATE_TIME_PATTERN).timestamp())
        except Exception as error:
            print(f"Error in parse_date_str_to_timestamp: {error}")
            return 0

    @staticmethod
    def format_timezone_offset(value: str, timezone_offset: int) -> str:
        try:
            local_time = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
            adjusted_time = local_time + timedelta(minutes=timezone_offset)
            return adjusted_time.strftime(DateTimeUtils.DATE_TIME_PATTERN)
        except Exception as error:
            print(f"Error in format_timezone_offset: {error}")
            return ''

    @staticmethod
    def format_timestamp_str(timestamp: str) -> str:
        try:
            timestamp = int(timestamp)
            if not timestamp:
                return ''
            dt = datetime.utcfromtimestamp(timestamp)
            return dt.strftime(DateTimeUtils.DATE_TIME_PATTERN)
        except Exception as error:
            print(f"Error in format_timestamp_str: {error}")
            return ''
