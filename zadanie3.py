import argparse


MONTHS = (
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
)
DAYS = (
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
)
DAY_ALIASES = {
    "mon": "monday",
    "tue": "tuesday",
    "wed": "wednesday",
    "thu": "thursday",
    "fri": "friday",
    "sat": "saturday",
    "sun": "sunday",
}
DAY_ALIASES.update({day: day for day in DAYS})
TIME_ALIASES = {
    "m": "morning",
    "morning": "morning",
    "e": "evening",
    "evening": "evening",
}

def parse_day_range(value):
    """Return the days in a range, or an empty list for an invalid range."""
    if value in DAY_ALIASES:
        return [DAY_ALIASES[value]]

    for position in range(len(value)):
        if value[position] == "-":
            first_day = value[:position]
            last_day = value[position + 1:]
            if first_day not in DAY_ALIASES or last_day not in DAY_ALIASES:
                return []

            first = DAYS.index(DAY_ALIASES[first_day])
            last = DAYS.index(DAY_ALIASES[last_day])
            if first > last:
                return []
            return list(DAYS[first:last + 1])
    return []

def parse_arguments():
    """
        days contains one expanded range per month. 
        time contains one value per expanded day, 
        ordered first by month and then by day.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m", "--months", nargs="+",
        help="Required: lowercase English month names, e.g. january february.",
    )
    parser.add_argument(
        "-d", "--days", nargs="+",
        help=(
            "Required: one lowercase day or range per month, e.g. mon-tue fri. "
            + "Use mon, tue, wed, thu, fri, sat, sun or full names. "
            + "Ranges cannot wrap past Sunday."
        ),
    )
    parser.add_argument(
        "-t", "--time", nargs="*", default=[],
        help=(
            "Times for consecutive days: m/morning or e/evening. "
            + "Missing values at the end default to morning."
        ),
    )
    parser.add_argument(
        "-c", "--create", action="store_const", const=True, default=False,
        help="Select file creation. Cannot be combined with --read.",
    )
    parser.add_argument(
        "-r", "--read", action="store_const", const=True, default=False,
        help="Select file reading (default).",
    )
    parser.add_argument(
        "--csv", action="store_const", const=True, default=False,
        help="Select CSV format (default). Cannot be combined with --json.",
    )
    parser.add_argument(
        "--json", action="store_const", const=True, default=False,
        help="Select JSON format.",
    )

    args = parser.parse_args()
    if not args.months or not args.days:
        print("Error: provide both --months and --days. Use -h for help.")
        return
    if len(args.months) != len(args.days):
        print("Error: provide exactly one day range per month.")
        return
    if args.create and args.read:
        print("Error: choose either --create or --read.")
        return
    if args.csv and args.json:
        print("Error: choose either --csv or --json.")
        return

    for month in args.months:
        if month not in MONTHS:
            print("Error: invalid month:", month)
            return

    day_ranges = []
    day_count = 0
    for value in args.days:
        days = parse_day_range(value)
        if not days:
            print("Error: invalid day range:", value)
            print("Use lowercase day names in Monday-to-Sunday order, e.g. mon-fri.")
            return
        day_ranges.append(days)
        day_count += len(days)

    if len(args.time) > day_count:
        print("Error: more times of day were provided than days in the ranges.")
        return

    times = []
    for value in args.time:
        if value not in TIME_ALIASES:
            print("Error: time of day must be m/morning or e/evening.")
            return
        times.append(TIME_ALIASES[value])
    while len(times) < day_count:
        times.append("morning")

    file_format = "csv"
    if args.json:
        file_format = "json"

    return {
        "months": args.months,
        "days": day_ranges,
        "time": times,
        "create": args.create,
        "format": file_format,
    }


def main():
    args = parse_arguments()
    if not args:
        return

    # Example use of args:
    #
    # if args["create"]:
    #     print("Mode: create")
    # else:
    #     print("Mode: read")
    # print("Format:", args["format"])
    # print("Months:", args["months"])
    # print("Days:", args["days"])
    # print("Times of day:", args["time"])


main()
