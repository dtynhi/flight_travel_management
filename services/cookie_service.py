from datetime import timedelta

from config.app_config import AppConfig


class CookieService:
    @staticmethod
    def set_cookie(response, name='', value='', sec=86400):
        response.set_cookie(
            key=name,
            value=value,
            max_age=timedelta(seconds=sec),
        )

    @staticmethod
    def set_access_token_cookie(response, access_token: str):
        CookieService.set_cookie(response, name=AppConfig.SESSION_COOKIE_NAME, value=access_token, sec=AppConfig.JWT_ACCESS_TOKEN_EXPIRES.total_seconds())

    @staticmethod
    def delete_access_token_cookie(response):
        CookieService.delete_cookie(response, AppConfig.SESSION_COOKIE_NAME)

    @staticmethod
    def get_cookie(request, name: str):
        return request.cookies.get(name)

    @staticmethod
    def delete_cookie(response, name: str):
        response.delete_cookie(name)

    @staticmethod
    def delete_all_cookies(response):
        for cookie in response.cookies:
            response.delete_cookie(cookie)
