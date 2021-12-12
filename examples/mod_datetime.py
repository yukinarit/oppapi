from oppapi import oppapi, from_args
from datetime import datetime, date, time
from typing import Optional


@oppapi
class Opt:
    """
    Option parser using oppapi
    """

    datetime: datetime
    date: Optional[date]
    time: Optional[time]


def main():
    opt = from_args(Opt)
    print(opt)


# python mod_datetime.py 2021-10-23T11:11:11 -d 2021-10-23 -t 11:11:11
if __name__ == "__main__":
    main()
