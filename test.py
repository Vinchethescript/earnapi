import dotenv
import os
import asyncio
from pyEarnapp.client import Client

dotenv.load_dotenv()

client = Client(os.getenv("EAUTH"))


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
    # Get referreals
    referreals = await client.get_referreals()
    print("Referreals:", referreals)
    # Device statuses
    device_statuses = await client.get_device_statuses()
    print("Device statuses:", device_statuses)
    # IP check
    ip_allowed = await client.is_ip_allowed("127.0.0.1")
    print("IP", "is" if ip_allowed else "is not", "allowed to use EarnApp")
    # Redeem to PayPal, may raise an exception
    redeemed = await client.redeem_to_paypal("your_paypal@email_he.re")
    print("Redeemed" if redeemed else "Could not redeem", "your balance to PayPal.")
    # Add a device (not tested)
    #await client.add_device("sdk-xxxxx-xxxxxxxxxxxx")
    # Delete a device (not tested)
    #await client.delete_device("sdk-xxxxx-xxxxxxxxxxxx")


asyncio.get_event_loop().run_until_complete(main())
