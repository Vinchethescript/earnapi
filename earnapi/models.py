from urllib.parse import urljoin
from datetime import datetime
from dataclasses import dataclass


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
        for k, v in kwargs.items():
            if callable(getattr(self, f"_transform_{k}", None)):
                kwargs[k] = getattr(self, f"_transform_{k}")(v)

    def __dir__(self):
        ret = dir(super())
        ret += self.___kwargs.keys()
        return ret

    def __getattr__(self, item):
        return self.___kwargs.get(item, None)

    def __getitem__(self, item):
        return self.___kwargs.get(item)

    def __repr__(self):
        args = []
        for key, value in self.___kwargs.items():
            args.append(f"{key}={value!r}")
        return f"{self.__class__.__name__} <{' '.join(args)}>"

    @classmethod
    def create_list(cls, items: list) -> list:
        return [cls(item) for item in items]


class Interactable(Model):
    def __init__(self, client, kwargs):
        super().__init__(kwargs)
        from .client import Client

        self.client: Client = client

    @classmethod
    def create_list(cls, client, items: list) -> list:
        return [cls(client, item) for item in items]


class RedeemDetails(Model):
    email: str
    email_hash: str
    payment_method: str
    min_redeem: float


class EarningsData(Model):
    multiplier: int
    multiplier_icon: str
    multiplier_hint: str
    balance: float
    earnings_total: float
    ref_bonuses: float
    ref_bonuses_total: float
    promo_bonuses: float
    promo_bonuses_total: float
    ref_bvpn: float
    ref_bvpn_total: float
    ref_hola_browser: float
    ref_hola_browser_total: float
    referral_part: int
    redeem_details: RedeemDetails

    def _transform_redeem_details(self, value: dict):
        return RedeemDetails(value)

    def _transform_referral_part(self, value: str):
        return float(value.rstrip("%")) / 100

    @property
    def referral_bonus(self):
        return self.ref_bonuses

    @property
    def referral_bonus_total(self):
        return self.ref_bonuses_total

    @property
    def promo_bonus(self):
        return self.promo_bonuses

    @property
    def promo_bonus_total(self):
        return self.promo_bonuses_total

    @property
    def brightvpn_earnings(self):
        return self.ref_bvpn

    @property
    def bvpn_earnings(self):
        return self.ref_bvpn

    @property
    def brightvpn_earnings_total(self):
        return self.ref_bvpn_total

    @property
    def bvpn_earnings_total(self):
        return self.ref_bvpn_total


class User(Model):
    first_name: str
    last_name: str
    locale: str
    name: str
    picture: str
    referral_code: str
    onboarding: datetime
    email: str

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def image_url(self) -> str:
        return self.picture

    def _transform_onboarding(self, value: str):
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")


class BanDetails(Model):
    pass


class Referral(Model):
    id: int
    email: str
    bonuses: float
    bonuses_total: float


class Transaction(Model):
    uuid: str
    status: str
    email: str
    date: datetime
    payment_method: str
    payment_date: datetime
    money_amount: float
    ref_bonuses_amount: float
    promo_bonuses_amount: float
    ref_bvpn_amount: float
    ref_hola_browser_amount: float
    fee_amount: float

    def _transform_date(self, value: str):
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")

    def _transform_payment_date(self, value: str):
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")

    @property
    def id(self):
        return self.uuid

    @property
    def amount(self):
        return self.money_amount

    @property
    def ref_bonuses(self):
        return self.ref_bonuses_amount

    @property
    def promo_bonuses(self):
        return self.promo_bonuses_amount

    @property
    def ref_bvpn(self):
        return self.ref_bvpn_amount

    @property
    def ref_hola_browser(self):
        return self.ref_hola_browser_amount

    @property
    def fee(self):
        return self.fee_amount

    @property
    def referreal_bonus(self):
        return self.ref_bonuses

    @property
    def brightvpn_bonus(self):
        return self.ref_bvpn

    @property
    def hola_browser_bonus(self):
        return self.ref_hola_browser


class Device(Interactable):
    uuid: str
    title: str
    country: str
    rate: float
    bw: int
    total_bw: int
    earned: float
    earned_total: float
    ips: list[str]
    billing: str

    def _transform_banned(self, value: dict):
        return BanDetails(value)

    @property
    def id(self):
        return self.uuid

    @property
    def name(self):
        return self.title

    @property
    def bandwidth(self):
        return self.bw

    @property
    def total_bandwidth(self):
        return self.total_bw

    async def hide(self):
        await self.client.request(
            "POST", Endpoint.HIDE_DEVICE, json={"uuid": self.uuid}
        )

    async def show(self):
        await self.client.request(
            "POST", Endpoint.SHOW_DEVICE, json={"uuid": self.uuid}
        )

    async def change_name(self, title: str):
        resp = await self.client.request(
            "PUT",
            urljoin(Endpoint.EDIT_DEVICE, self.uuid),
            json={"name": title},
        )
        return resp["status"] == "ok"

    async def get_status(self):
        ret = await self.client.get_online_devices(self.uuid)
        if not ret:
            return

        return ret[0]

    async def is_online(self):
        status = await self.get_status()
        return status is not None

    def __str__(self):
        return self.title


# this can't be used as model as the response is not a dict
@dataclass
class OnlineDeviceStatus:
    uuid: str
    since: datetime
    uptime_today: float
