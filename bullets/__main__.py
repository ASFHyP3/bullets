import sys
import logging
import argparse
from datetime import datetime

from dateutil import tz
from dateutil.parser import parse as parse_date
from dateutil.relativedelta import relativedelta

from bullets import generate_bullets


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    begin = parser.add_mutually_exclusive_group()
    begin.add_argument('-d', '--days-back', type=int, default=7,
                       help='Start search at 5:00 AM AKST this many days ago')
    begin.add_argument('-s', '--search-start', type=parse_date,
                       help='Start search at this time. Time must be parsable by dateutil '
                            'and AKST will be assumed for the time zone if not given.')

    parser.add_argument('--detailed', action='store_true',
                        help='Produce a detailed report that includes the Release/PR/Issue body. '
                             'EXPERIMENTAL! Report formatting is likely not great.')

    args = parser.parse_args()

    if args.search_start is None:
        args.search_start = datetime.now(tz.gettz('AKST')) \
                            - relativedelta(days=args.days_back, hour=5, minute=0, second=0, microsecond=0)

    out = logging.StreamHandler(stream=sys.stdout)
    out.addFilter(lambda record: record.levelno <= logging.INFO)
    err = logging.StreamHandler()
    err.setLevel(logging.WARNING)
    logging.basicConfig(format='%(message)s', level=logging.INFO, handlers=(out, err))

    generate_bullets(search_start=args.search_start, detailed=args.detailed)


if __name__ == '__main__':
    main()
