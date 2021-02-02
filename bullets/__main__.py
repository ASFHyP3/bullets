import argparse
from datetime import datetime

from dateutil import tz
from dateutil.parser import parse as parse_date
from dateutil.relativedelta import relativedelta

from bullets import generate_bullets
from bullets.generate import _DAYS_BACK, _RD_ARGS


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    begin = parser.add_mutually_exclusive_group()
    begin.add_argument('-d', '--days-back', type=int, default=_DAYS_BACK,
                       help='Start search at 2:00 PM this many days ago')
    begin.add_argument('-s', '--start-search', type=parse_date,
                       help='Start search at this time. Time must be parsable by dateutil '
                            'and AKST will be assumed for the time zone if not given.')

    parser.add_argument('--detailed', action='store_true',
                        help='Produce a detailed report that includes the Release/PR/Issue body. '
                             'EXPERIMENTAL! Report formatting is likely not great.')

    args = parser.parse_args()

    if args.start_search is None:
        args.start_search = datetime.now(tz.gettz('AKST')) - relativedelta(days=args.days_back, **_RD_ARGS)

    if args.start_search.tzinfo is None:
        args.start_search = args.start_search.replace(tzinfo=tz.gettz('AKST'))

    generate_bullets(search_start=args.start_search, detailed=args.detailed)


if __name__ == '__main__':
    main()
