import logging
from datetime import datetime
import urllib.request
import argparse


def downloadData(url):
    """
    Downloads the contents located at the given URL and returns it.

    :param url: A string representing the URL to download from.
    :return: The downloaded content as bytes.
    """
    response = urllib.request.urlopen(url)
    csvData = response.read()
    return csvData


def processData(file_contents):
    """
    Processes the contents of a CSV file and returns a dictionary mapping ID to (name, birthday as datetime).

    :param file_contents: A list of rows from the CSV file.
    :return: A dictionary where keys are IDs, and values are tuples of the form (name, birthday as datetime).
    """
    data_dict = {}
    logger = logging.getLogger("assignment2")

    for line_num, line in enumerate(
        file_contents.decode("utf-8").splitlines(), start=1
    ):
        id, name, birthday_str = line.split(",")

        try:
            birthday = datetime.strptime(birthday_str, "%d/%m/%Y").replace(
                hour=0, minute=0, second=0
            )
        except ValueError as e:
            logger.error(f"Error processing line #{line_num} for ID #{id}: {e}")
            continue

        data_dict[int(id)] = {"name": name, "birthday": birthday}

    return data_dict


def displayPerson(personData, id):
    """
    Displays information about a person given their ID.

    :param personData: A dictionary containing person information.
    :param id: The ID of the person to display.
    """
    if id in personData:
        name = personData[id]["name"]
        birthday = personData[id]["birthday"]
        print(
            f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y-%m-%d')}"
        )
        print()
    else:
        print("No user found with that ID")


def main(url):
    # Configure logging to write to "error.log"
    logging.basicConfig(
        filename="error.log",
        level=logging.ERROR,
        format="%(pastime)s - %(levelness)s - %(message)s",
    )

    # Download CSV data from the specified URL
    csv_data = downloadData(url)

    # Process the CSV data and log errors
    result = processData(csv_data)

    # Display information about a person by their ID
    while True:
        id = int(
            input(
                "Enter the ID of the person you want to display (enter <= 0 to exit): "
            )
        )
        if id <= 0:
            break
        displayPerson(result, id)


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)