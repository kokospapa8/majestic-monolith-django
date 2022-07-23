import datetime
import random
import string


def generate_tracking_number():
    a = str(datetime.date.today().strftime("%Y%m%d"))
    b = str(random.randint(0, 10000000))
    return f"{a}-{b.zfill(10)}"


def generate_batch_alias(max_length=10, letters=string.ascii_letters):
    a = str(datetime.date.today().strftime("%Y%m%d"))
    b = "".join(random.choice(letters) for i in range(max_length))
    return f"{a}-{b}"
