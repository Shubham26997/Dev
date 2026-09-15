import math
from datetime import datetime
def amount_left_cal():
    amount = int(input("Enter the amount you have: "))
    item_price = 15
    tax = 0.03
    amount_left = amount - (item_price + (item_price*tax))
    return amount_left

def daystobirthday():

    try:
        days = datetime.date(input("Enter the number of days left: "))
    except ValueError:
        print("Enter valid days")
        return
    print(f"Total number of days left for your birthday {datetime}")
    if 0 < days < 366:
        weeks = math.trunc(days / 7)
        print(f"Good News!! only {weeks} weeks left for your birthday")
    else:
        print("Please Try again days mentioned are not in prescribed range of [0, 365]")

if __name__ == "__main__":
    # print(amount_left_cal())
    daystobirthday()