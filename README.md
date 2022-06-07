# EarnAPI

Asynchronous EarnApp API wrapper written in Python based on [pyEarnapp](https://github.com/fazalfarhan01/EarnApp-API.git) (synchronous).

## Installation
```bash
pip install earnapi
```
## Example usage
```python
import asyncio
from earnapi import Client

loop = asyncio.get_event_loop()
client = Client("your_auth_token_cookie")
async def main():
    # Get user information
    userdata = await client.get_user_data()
    print("User data:", userdata)
    # Get information about earnings
    earnings = await client.get_earnings()
    print("Earnings:", earnings)
    # Get a list of devices
    devices = await client.get_devices()
    print("Devices:", devices)
    # Get your transactions
    transactions = await client.get_transactions()
    print("Transactions:", transactions)
    # Get referrals
    referrals = await client.get_referrals()
    print("Referrals:", referrals)
    # Device statuses
    device_statuses = await client.get_device_statuses()
    print("Device statuses:", device_statuses)
    # IP check
    ip_allowed = await client.is_ip_allowed("your_ip_address_here")
    print("IP", "is" if ip_allowed else "is not", "allowed to use EarnApp")
    # Redeem to PayPal, may raise an exception
    redeemed = await client.redeem_to_paypal("your_paypal@email_he.re")
    print("Redeemed" if redeemed else "Could not redeem", "your balance to PayPal.")
    # Add a device (not tested)
    #await client.add_device("sdk-xxxxx-xxxxxxxxxxxx")
    # Delete a device (not tested)
    #await client.delete_device("sdk-xxxxx-xxxxxxxxxxxx")

loop.run_until_complete(main())
```

## Exceptions
- The following exceptions are defined.
    Exception | Reason
    --- | ---
    `EarnAppError`: The exception all exceptions are based on.
    `AuthenticationError`: Raised on authentication failure.
    `DeviceOperationError`: Raised when any operation with a device fails.
    `DeviceNotFoundError`: Raised when a device to add wasn't found.
    `DeviceAlreadyAddedError`: Raised when a device is already added.
    `TooManyRequestsError`: Raised when you reach EarnApp's rate limit.
    `IPCheckError`: Raised when there's an error checking for the IP.
    `InvalidIPError`: Raised when the IP address isn't valid.
    `RedeemError`: Raised when an error occurs trying to redeem.