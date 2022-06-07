import dotenv
import os
import asyncio
from datetime import datetime
from earnapi.client import Client

dotenv.load_dotenv()

client = Client(os.getenv("EAUTH"))


async def main():
    # Get user information
    user = await client.get_user_data()
    print("User data:")
    print("Username:", user.name)
    print("Email:", user.email)
    print("First name:", user.first_name)
    print("Last name:", user.last_name)
    print("Locale:", user.locale)
    print("Referral code:", user.referral_code)

    print()
    # Get information about earnings
    earnings = await client.get_earnings()
    print("Earnings:")
    print("Multiplier:", earnings.multiplier)
    print("Current balance:", earnings.balance)
    print("Lifetime earnings:", earnings.earnings_total)

    print()
    # Get a list of devices and their status
    devices = await client.get_devices()
    device_statuses = await client.get_device_statuses()
    print("Devices:")
    for device in devices:
        print("\tDevice:", device.title)
        print("\tCountry:", device.country)
        print("\tRate:",  device.rate)
        print("\tBandwidth:", device.bw, "bytes")
        print("\tTotal bandwidth:", device.total_bw, "bytes")
        print("\tEarned:", device.earned)
        print("\tTotal earned:", device.earned_total)
        print("\tUUID:", device.uuid)
        status = device_statuses[device.uuid]
        print("\tStatus:", "online" if status["online"] else "offline", end=" ")
        if status["online"]:
            print("since", status["online_since"], "for", datetime.fromtimestamp(status["uptime_today"]).time())
        else:
            print()

        print()

    print()
    # Get your transactions
    transactions = await client.get_transactions()
    print("Transactions:")
    for trans in transactions: # hi
        print("\tDate:", trans.date)
        print("\tAmount:", trans.money_amount)
        print("\tStatus:", trans.status)
        print()

    print()
    # Get referrals
    referrals = await client.get_referrals()
    print("Referrals:")
    for refer in referrals:
        print("\tID:", refer.id)
        print("\tFrom:", refer.email)
        print("\tBonus:", refer.bonuses)
        print("\tTotal bonuses:", refer.bonuses_total)
        print()

    print()
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
