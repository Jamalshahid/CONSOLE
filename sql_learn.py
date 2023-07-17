import sqlite3
from datetime import date, timedelta
import datetime

# conn = sqlite3.connect("console_database.sqlite3")  
# cursor = conn.cursor()

# line_chart_result = cursor.execute("""
#                 select COUNT(CASE WHEN status="Acceptable" THEN 1 END), COUNT(CASE WHEN status="Marginal" THEN 1 END), 
#                 COUNT(CASE WHEN status="Unacceptable" THEN 1 END), strftime("%Y-%m-%d",  datetime(date_of_inspection, 'unixepoch')) as 'month-year' 
#                 from bottles_inspection_result WHERE strftime("%Y-%m-%d", datetime(date_of_inspection, 'unixepoch')) BETWEEN strftime("%Y-%m-%d", date('now','localtime','-29 days')) AND 
#                 strftime("%Y-%m-%d", date('now','localtime'))  group by strftime("%d",  datetime(date_of_inspection, 'unixepoch'));
#                 """)

# line_chart_result_accept = []
# line_chart_result_margin = []
# line_chart_result_unaccept = []
# line_chart_result = line_chart_result.fetchall()
# today = date.today()
# Dateslist = [str(today - timedelta(days = day)) for day in range(29)]

# count = 0
# for i in range(len(Dateslist)):

#     for j in line_chart_result:
#         if j[-1] == Dateslist[i]:
#             line_chart_result_accept.append(j[0])
#             line_chart_result_unaccept.append(j[2])
#             line_chart_result_margin.append(j[1])
#             count += 1
#             break
#     Dateslist[i] = "/".join(Dateslist[i].split("-")[-1:0:-1])
#     if count > 0:
#         count = 0
#         continue
#     line_chart_result_accept.append(0)
#     line_chart_result_unaccept.append(0)
#     line_chart_result_margin.append(0)

# print(line_chart_result_accept)
# print(line_chart_result_margin)
# print(line_chart_result_unaccept)
# print(Dateslist)
# conn.close()




# date_format = "%Y-%m-%d"

# a = datetime.strptime('2008-8-18', date_format)
# b = datetime.strptime('2010-9-26', date_format)

# delta = b - a
# lst = [(i, datetime.time(i).strftime('%I %p')) for i in range(24)]

from datetime import timedelta, datetime

from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_months_between_dates(start_date, end_date):
    start_month = start_date.month
    start_year = start_date.year

    months = []

    while start_date <= end_date:
        months.append(start_date.strftime("%b %Y"))
        start_date += relativedelta(months=1)

    return months

# Example usage
start_date = datetime(2022, 3, 3)
end_date = datetime(2022, 12, 31)
months = get_months_between_dates(start_date, end_date)
print(months)


# print(lst) 