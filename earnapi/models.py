from urllib.parse import urljoin
from datetime import datetime


class Endpoint:  # there are still a lot to be implemented
    BASE_URL = "https://earnapp.com/dashboard/api/"

    # users
    USER = urljoin(BASE_URL, "user")
    USER_DATA = urljoin(BASE_URL, "user_data")
    DISABLE_USER = urljoin(BASE_URL, "user/disable")
    RESTORE_USER = urljoin(BASE_URL, "restore_user")
    HAS_USER = urljoin(BASE_URL, "has_user")

    # devices
    DEVICES = urljoin(BASE_URL, "devices")
    DEVICE = urljoin(BASE_URL, "device/")
    LINK_DEVICE = urljoin(BASE_URL, "link_device")
    EDIT_DEVICE = urljoin(BASE_URL, "edit_device/")
    SHOW_DEVICE = urljoin(BASE_URL, "show_device")
    HIDE_DEVICE = urljoin(BASE_URL, "hide_device")
    DEVICE_STATUSES = urljoin(BASE_URL, "device_statuses")

    # money
    MONEY = urljoin(BASE_URL, "money")
    BONUSES = urljoin(BASE_URL, "bonuses")
    REDEEM_DETAILS = urljoin(BASE_URL, "redeem_details")
    TRANSACTIONS = urljoin(BASE_URL, "transactions")
    REDEEM = urljoin(BASE_URL, "redeem")
    REFEREES = urljoin(BASE_URL, "referees")

    # other
    ONBOARDING = urljoin(BASE_URL, "onboarding")
    TOKEN = urljoin(BASE_URL, "token")
    COUNTERS = urljoin(BASE_URL, "counters")
    NOTIFS = urljoin(BASE_URL, "notifications")
    SPEEDTEST = urljoin(BASE_URL, "speedtest")
    SPEEDTEST_CSV = urljoin(BASE_URL, "speedtest_csv")
    DOWNLOADS = urljoin(BASE_URL, "downloads")
    P_METHODS = urljoin(BASE_URL, "payment_methods")
    LEADERBOARD = urljoin(BASE_URL, "leaderboard")
    USAGE = urljoin(BASE_URL, "usage")
    SPEEDTEST_SHARE = urljoin(BASE_URL, "speedtest_share")
    API_KEY = urljoin(BASE_URL, "api_key")
    XSRF = urljoin(BASE_URL, "sec/rotate_xsrf")
    IP_CHECK = urljoin(BASE_URL, "check_ip/")
    LOGOUT = urljoin(BASE_URL, "logout")


class Model:
    def __init__(self, kwargs) -> None:
        self.___kwargs = kwargs

    def __dir__(self):
        ret = dir(super())
        ret += self.___kwargs.keys()
        return ret

    def __getattr__(self, item):
        return self.___kwargs.get(item, None)

    def __getitem__(self, item):
        return self.___kwargs.get(item)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.___kwargs})"

    @classmethod
    def create_list(cls, items: list) -> list:
        return [cls(item) for item in items]


class Earning(Model):
    pass


class User(Model):
    pass


class BanDetails(Model):
    pass


class Referral(Model):
    pass


class RedeemDetails:
    pass


class Transaction(Model):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        self.date = datetime.strptime(self.date, "%Y-%m-%dT%H:%M:%S.%f%z")
        payment = self.payment_date
        if payment:
            self.payment_date = datetime.strptime(payment, "%Y-%m-%dT%H:%M:%S.%f%z")


class Device(Model):
    def __init__(self, kwargs):
        super().__init__(kwargs)
        if kwargs.get("banned", None):
            self.banned = BanDetails(kwargs["banned"])
