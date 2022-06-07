import json
import re
import typing
from .errors import *
from .models import *
from urllib.parse import urljoin
from aiohttp import ClientResponseError, ClientSession

ip_regex = re.compile(
    "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
)


def is_a_valid_ip(ipaddress: str):
    return bool(ip_regex.search(ipaddress))


class Client:
    def __init__(self, auth_refresh_token) -> None:
        self.params = {"appid": "earnapp_dashboard"}
        self.headers = {}
        self.cookies = {
            "auth": "1",
            "auth-method": "google",
            "oauth-refresh-token": auth_refresh_token,
        }

    async def request(
        self,
        method: str,
        endpoint: str,
        cls: Model = None,
        listify=False,
        return_response=False,
        *args,
        **kwargs,
    ) -> typing.Any:
        ret = None
        if (
            self.cookies.get("xsrf-token") == None
            or self.headers.get("xsrf-token") == None
        ):
            self.cookies["xsrf-token"] = self.headers["xsrf-token"] = ""
            await self._rotate_xsrf()

        async with ClientSession() as session:
            async with session.request(
                method,
                endpoint,
                headers=self.headers,
                params=self.params,
                cookies=self.cookies,
                *args,
                **kwargs,
            ) as response:
                if return_response:
                    ret = response

                else:
                    response_content = (await response.content.read()).decode()

                try:
                    response.raise_for_status()
                except ClientResponseError as e:
                    if return_response:
                        e.response = response
                    else:
                        e.content = response_content

                    if response.status == 403:
                        raise AuthenticationError from None
                    else:
                        raise e

                if not return_response:
                    cls = cls.create_list if listify else cls
                    try:
                        ret = json.loads(response_content)
                        if listify and "list" in ret and isinstance(ret["list"], list):
                            ret = ret["list"]

                    except json.JSONDecodeError:
                        ret = response_content

                    ret = cls(ret)

        return ret

    async def _rotate_xsrf(self):
        resp = await self.request("GET", Endpoint.XSRF, str, False, True)
        token = resp.cookies["xsrf-token"].coded_value
        self.cookies["xsrf-token"] = token
        self.headers["xsrf-token"] = token
        return token

    async def get_user_data(self, *args, **kwargs) -> User:
        return await self.request(
            "GET", Endpoint.USER_DATA, User, False, *args, **kwargs
        )

    async def get_earnings(self, *args, **kwargs) -> Earning:
        return await self.request(
            "GET", Endpoint.MONEY, Earning, False * args, **kwargs
        )

    async def get_devices(self, *args, **kwargs) -> typing.List[Device]:
        return await self.request(
            "GET", Endpoint.DEVICES, Device, True, *args, **kwargs
        )

    async def get_transactions(self, *args, **kwargs) -> typing.List[Transaction]:
        return await self.request(
            "GET", Endpoint.TRANSACTIONS, Transaction, True, *args, **kwargs
        )

    async def get_referrals(self, *args, **kwargs) -> typing.List[Referral]:
        return await self.request(
            "GET", Endpoint.REFEREES, Referral, True, *args, **kwargs
        )

    async def add_device(self, new_device_id, *args, **kwargs):
        data = {"uuid": new_device_id}
        try:
            content = await self.request(
                "POST",
                Endpoint.LINK_DEVICE,
                dict,
                False,
                data=data,
                *args,
                **kwargs,
            )
        except ClientResponseError as e:
            if e.status == 429:
                raise TooManyRequestsError(e.content)
            else:
                raise DeviceOperationError(f"Failed to add device: {e.content}")
        else:
            error_message = content.get("error", None)
            if error_message:
                if "already linked" in error_message:
                    raise DeviceAlreadyAddedError(error_message)
                elif "not found" in error_message:
                    raise DeviceNotFoundError(error_message)
                else:
                    raise DeviceOperationError(error_message)
            else:
                return content

    async def delete_device(self, device_uuid: str, *args, **kwargs) -> bool:
        try:
            content = await self.request(
                "DELETE",
                urljoin(Endpoint.DEVICE, device_uuid),
                dict,
                False,
                *args,
                **kwargs,
            )
        except ClientResponseError as e:
            if e.status == 429:
                raise TooManyRequestsError(e.content)
            else:
                raise DeviceOperationError(f"Failed to delete device: {e.content}")
        else:
            error_message = content.get("error", None)
            if error_message:
                raise DeviceOperationError(error_message)
            else:
                return True if content.get("status", None) == "ok" else False

    async def is_ip_allowed(self, ip_address: str, *args, **kwargs) -> bool:
        if not is_a_valid_ip(ip_address):
            raise IPCheckError("The IP address is not valid.")
        try:
            content = await self.request(
                "GET",
                urljoin(Endpoint.IP_CHECK, ip_address),
                dict,
                False,
                *args,
                **kwargs,
            )
        except ClientResponseError as e:
            if e.status in [429, 423]:
                raise TooManyRequestsError(e.content) from None
            else:
                raise IPCheckError(f"Failed to check IP Address: {e.content}") from None
        else:
            error_message = content.get("error", None)
            if error_message:
                raise IPCheckError(error_message)
            else:
                return not content.get("is_ip_blocked")

    async def redeem_to_paypal(self, paypal_email: str, *args, **kwargs) -> bool:
        data = {"to": paypal_email, "payment_method": "paypal.com"}
        try:
            content = await self.request(
                "POST", Endpoint.REDEEM, dict, False, data=data, *args, **kwargs
            )
        except ClientResponseError as e:
            if e.status == 429:
                raise TooManyRequestsError(e.content) from None
            else:
                raise RedeemError(f"Failed to redeem balance: {e.content}") from None
        else:
            error_message = content.get("error", None)
            if "ok" in content:
                return content.get("ok", False)
            if error_message:
                raise RedeemError(error_message)
            else:
                return content

    async def get_device_statuses(self) -> dict:
        devices = await self.get_devices()
        devices_req = []

        for device in devices:
            devices_req.append({"uuid": device.uuid, "appid": "node_earnapp.com"})

        try:
            content = await self.request(
                "POST",
                Endpoint.DEVICE_STATUSES,
                dict,
                False,
                json={"list": devices_req},
            )
        except ClientResponseError as e:
            if e.status == 429:
                raise TooManyRequestsError(e.content) from None
            else:
                raise Exception(f"Failed to get device statuses: {e.content}") from None
        else:
            error_message = content.get("error", None)
            if error_message:
                raise Exception(error_message)
            else:
                return content["statuses"]
