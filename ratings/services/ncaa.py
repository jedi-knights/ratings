import csv
import requests


# https://web3.ncaa.org/directory/api/directory/memberList?type=12&division=I
# https://web3.ncaa.org/directory/api/directory/memberList?type=12&division=II
# https://web3.ncaa.org/directory/api/directory/memberList?type=12&division=III

HOSTNAME = 'web3.ncaa.org'
RESOURCE = '/directory/api/directory/memberList'

# Define the subset of fields to save
MEMBER_FIELDS_TO_SAVE = [
    'orgId',
    'nameOfficial',
    'divisionRoman',
    'conferenceId',
    'conferenceName',
    'webSiteUrl',
    'athleticWebUrl',
]

def _generate_url(division: str) -> str:
    """
    Generate a URL for the specified division

    :param division:
    :return:
    """
    return f'https://{HOSTNAME}{RESOURCE}?type=12&division={division}'


def get_members(division: str) -> list[dict]:
    """
    Get NCAA members by division

    :param division: Division (I, II, III
    :return:
    """
    payload = {}
    headers = {}

    url = _generate_url(division)
    response = requests.request(method='GET', url=url, data=payload, headers=headers)

    json_data = response.json()

    return json_data


def save_to_csv(data: list[dict], filename: str, fields: list[str]):
    """
    Save data to a CSV file

    :param data: List of dictionaries
    :param filename: Name of the file
    :param fields: List of fields to save
    :return:
    """
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=fields)
        dict_writer.writeheader()
        for item in data:
            filtered_item = {key: item[key] for key in fields if key in item}
            dict_writer.writerow(filtered_item)

if __name__ == '__main__':
    save_to_csv(get_members('I'), filename='d1.csv', fields=MEMBER_FIELDS_TO_SAVE)
    save_to_csv(get_members('II'), filename='d2.csv', fields=MEMBER_FIELDS_TO_SAVE)
    save_to_csv(get_members('III'), filename='d3.csv', fields=MEMBER_FIELDS_TO_SAVE)
