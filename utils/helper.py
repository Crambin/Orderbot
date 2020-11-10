import datetime


async def get_next_birthday_info(birthday):
    today = datetime.date.today()
    birth_year = birthday.year
    birthday = datetime.date(year=today.year, month=birthday.month, day=birthday.day)
    if birthday < today:
        birthday = datetime.date(year=today.year + 1, month=birthday.month, day=birthday.day)

    days_left = (birthday - today).days
    next_date = birthday.strftime("%d/%m/%Y")
    next_age = birthday.year - birth_year
    age_msg = str(next_age) + (
        "th" if 4 <= next_age % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(next_age % 10, "th"))

    return days_left, next_date, age_msg
