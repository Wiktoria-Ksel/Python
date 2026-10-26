import argparse
import os
import random
import json

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

def create_csv(path):
    """
    Creates csv file using 'random' module.
    """

    model = random.choice(["A", "B", "C"])
    wynik = random.randint(0, 1000)
    czas = random.randint(0, 1000)

    with open(path, "w", encoding="utf-8") as f:
        f.write("Model; Wynik; Czas;\n")
        f.write(f"{model}; {wynik}; {czas}s;\n")

def read_csv(path):
    """
    Reads csv file and returns 'Czas' if 'Model' is 'A' (otherwise return 0).
    """

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

        if len(lines) >= 2:
            data = lines[1].strip().split(";")

            if data[0].strip() == "A" and len(data) >= 3:
                return int(data[2].strip().removesuffix("s"))

    return 0

def create_json(path):
    """
    Creates json file using 'random' and 'json' modules with function 'json.dump'.
    """

    model = random.choice(["A", "B", "C"])
    wynik = random.randint(0, 1000)
    czas = random.randint(0, 1000)

    data = {
        "Model" : model,
        "Wynik" : wynik,
        "Czas" : f"{czas}s"
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def read_json(path):
    """
    Reads json file and returns 'Czas' if 'Model' is 'A' (otherwise returns 0).
    """

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

        if data.get("Model") == "A":
            return int(data.get("Czas").removesuffix("s"))

    return 0

def create_process(file_path, dir_path, file_format):
    """
    Creates directory and calls 'create' function.
    """
    os.makedirs(dir_path, exist_ok=True)
    if file_format == "json":
        create_json(file_path)
    else:
        create_csv(file_path)

def read_process(file_path, file_format):
    """
    Calls for 'read' function and returns the time
    for model A, or 0 if doesn't exist.read_process
    """
    file_time = 0
    if os.path.exists(file_path):
        if file_format == "json":
            file_time = read_json(file_path)
        else:
            file_time = read_csv(file_path)
    else:
        print(f"Error: The given file {file_path} does not exist.")
    return file_time

def files_maker(args):
    """
    Generates the directory and file paths based on provided arguments.
    Sums up the times for model A and prints the final result.

    Args: A dictionary generated by the function parse_arguments():
    "months" a list: List of selected months.
    "days" a list of lists: Lists of days assigned to months.
    "time" a list: List of times assigned chronologically to every day.
    "create" bool: True = create, False = read.
    "format" str: 'csv' or 'json'.
    """
    index = 0
    times_sum = 0
    for i in range (len(args["months"])):
        month = args["months"][i]
        for day in args["days"][i]:
            day_time = args["time"][index]
            index += 1
            dir_path = os.path.join(month, day, day_time)

            if args["format"] == "json":
                file_path = os.path.join(dir_path, "Dane.json")
            else:
                file_path = os.path.join(dir_path, "Dane.csv")

            if args["create"]:
                create_process(file_path, dir_path, args["format"])
            else:
                times_sum += read_process(file_path, args["format"])

    if not args["create"]:
        print(f"Total time in all files with model A is {times_sum}")

def main():
    args = parse_arguments()
    if not args:
        return
    files_maker(args)

main()