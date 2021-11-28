import csv
from datetime import datetime

log_list = []
with open('cdn_access_log.txt', newline='') as logfile:
    logfile_reader = csv.DictReader(logfile, delimiter='\t')
    for request in logfile_reader:
        # Remove the '#' from the column name for better readability
        log_list.append({"date" if k == "# date" else k: v for k, v in request.items()})


def check_date(date_sting):
    """
    Whether the date is within 24th Aug to 25th Aug ignore the year
    @param date_sting: date in string
    @return: boolean
    """
    temp_year = 2021
    start_date = datetime(temp_year, 8, 24)
    end_date = datetime(temp_year, 8, 25)
    compare_date = datetime.strptime(date_sting, '%d/%m/%Y').replace(year=temp_year)
    return start_date <= compare_date <= end_date


def check_url(url):
    """
    Whether the url is end with '.jpg'
    @param url: url
    @return: boolean
    """
    return url.endswith('.jpg')


log_list_filtered = [log for log in log_list if check_date(log['date']) and check_url(log['url'])]

total_data_transfer = sum(int(log['size']) for log in log_list_filtered)
print(total_data_transfer)
