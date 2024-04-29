import dotenv
import os
import asyncio
import aiohttp
from datetime import datetime
from earnapi.client import Client

dotenv.load_dotenv()
loop = asyncio.get_event_loop()
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
    if earnings.redeem_details:
        print("Redeem data:")
        print("\tPayment method:", earnings.redeem_details.payment_method)
        print("\tMinimum balance:", earnings.redeem_details.min_redeem)
        print("\tPayPal email:", earnings.redeem_details.email)
        print("\tEmail hash:", earnings.redeem_details.email_hash)
        print()

    print()
    # Get a list of devices and their status
    devices = await client.get_devices()
    statuses = await client.get_online_devices()
    print("Devices:")
    for device in devices:
        print("\tDevice:", device.title)
        print("\tCountry:", device.country)
        print("\tRate:", device.rate)
        print("\tBandwidth:", device.bw, "bytes")
        print("\tTotal bandwidth:", device.total_bw, "bytes")
        print("\tEarned:", device.earned)
        print("\tTotal earned:", device.earned_total)
        print("\tUUID:", device.uuid)
        # We could also use device.get_status() to get the status of the device,
        # which would return None if it was offline, but that would require
        # one more request per device, which is not what we want here, to avoid
        # rate limits.
        status = list(filter(lambda x: x.uuid == device.uuid, statuses))
        print("\tStatus:", "online" if status else "offline", end=" ")
        if status:
            print(
                "since",
                status[0].since,
                "for",
                datetime.fromtimestamp(status[0].uptime_today).time(),
            )
        else:
            print()

        print()

    print()
    # Get your transactions
    transactions = await client.get_transactions()
    print("Transactions:")
    for transaction in transactions:
        print("\tDate:", transaction.date)
        print("\tAmount:", transaction.money_amount)
        print("\tStatus:", transaction.status)
        print()

    print()
    # Get referrals
    referrals = await client.get_referrals()
    print(referrals)
    print("Referrals:")
    for refer in referrals:
        print("\tID:", refer.id)
        print("\tFrom:", refer.email)
        print("\tBonus:", refer.bonuses)
        print("\tTotal bonuses:", refer.bonuses_total)
        print()

    print()
    # IP check
    async with aiohttp.ClientSession() as session:
        async with session.get("https://ifconfig.me/ip") as resp:
            ip_allowed = await client.check_ip(await resp.text())
            print("This IP", "is" if ip_allowed else "is not", "allowed to use EarnApp")

    # Redeem to PayPal, may raise an exception
    ch = await loop.run_in_executor(
        None, input, "Do you want to try to redeem your balance to PayPal? [y/N] "
    )
    if ch.lower() == "y":
        match = False
        while not match:
            email = await loop.run_in_executor(None, input, "Enter your PayPal email: ")
            confirm = await loop.run_in_executor(
                None,
                input,
                "Re-enter your PayPal email, just to be sure you're not going to lose your money: ",
            )
            if email != confirm:
                print("Emails do not match.")
            else:
                match = True

        try:
           redeemed = await client.redeem_to_paypal(email)
        except Exception as e:
            print("Could not redeem your balance to PayPal:", e)
        else:
            print("Redeemed" if redeemed else "Could not redeem", "your balance to PayPal.")

    # Add a device (not tested)
    # await client.add_device("sdk-xxxxx-xxxxxxxxxxxx")
    # Delete a device (not tested)
    # await client.delete_device("sdk-xxxxx-xxxxxxxxxxxx")


loop.run_until_complete(main())
