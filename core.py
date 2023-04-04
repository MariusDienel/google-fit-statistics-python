import datetime
import os

# Path to folder 'Aktivitäten'
PATH_TO_SEARCH = ''
STARTING_DATE = datetime.datetime(2019, 4, 1)
END_DATE = datetime.datetime(2023, 10, 31)


def get_files(filetype):
    filenames = os.listdir(PATH_TO_SEARCH)
    files_with_type = list(filter(lambda filename: filename.__contains__(filetype), filenames))
    files_with_valid_date = filter(lambda filename: has_valid_date(filename), files_with_type)
    return list(files_with_valid_date)


def has_valid_date(filename: str):
    file_date_string = filename[0:10]
    file_date = datetime.datetime.strptime(file_date_string, '%Y-%m-%d')
    return STARTING_DATE.timestamp() < file_date.timestamp() < END_DATE.timestamp()


def get_value_from_line(line: str):
    value_string = line.strip().removeprefix('<DistanceMeters>').removesuffix('</DistanceMeters>')
    return float(value_string)


def get_distance_in_m(filename):
    file = open(PATH_TO_SEARCH + '\\' + filename, 'r')
    lines = file.readlines()
    distance_elements = list(filter(lambda line: line.__contains__('DistanceMeters'), lines))
    distance_values = list(map(lambda element: get_value_from_line(element), distance_elements))
    # there is always one value that is the sum of all values, so we can just use that
    total_distance = max(distance_values)
    return float(total_distance)


if __name__ == "__main__":
    bike_files = get_files("Radfahren")
    distances_in_m = map(lambda file: get_distance_in_m(file), bike_files)
    result = str(sum(distances_in_m))
    message = f'Du bist insgesamt {result} meter mit dem Rad gefahren'
    print(message)
