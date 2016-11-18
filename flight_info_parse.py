# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import requests
from bs4 import BeautifulSoup

airline_code = 'DL'
flight_number = '168'

status_url = 'http://www.flightstats.com/go/FlightStatus/flightStatusByFlight.do'
params = {'airlineCode' : airline_code, 
          'flightNumber' : flight_number}
res = requests.get(status_url, params=params)   

#%%

soup = BeautifulSoup(res.text, 'html.parser')
name_div = soup.find('div', class_='flightName')

for s in name_div.stripped_strings:
    flight_name = s
    break

#%%

route = soup.find('div', class_='route').string
route_no_space = route.replace(' ','').replace('\n','').replace('\t','')

import re
depart_pat = re.compile(r'(^[\s\S]+)to\(')
arr_pat =re.compile(r'to(\(.+$)')
depart_match = depart_pat.search(route_no_space)
arr_match = arr_pat.search(route_no_space)
assert depart_match and arr_match

depart = depart_match.group(1)
arr = arr_match.group(1)
print depart, arr

#%%

times_td = soup.find_all('td', class_='statusValue')
counter = 0
depart_time = times_td[0].string.replace(' ','').replace('\t', '').replace('\n','')
arr_time = times_td[1].string.replace(' ','').replace('\t', '').replace('\n','')

print depart_time
print arr_time

time_pattern = re.compile(r'^\d{1,2}:\d{1,2}[AM|PM]+')
d_time_match = time_pattern.search(depart_time)
a_time_match = time_pattern.search(arr_time)

assert d_time_match and a_time_match
depart_time = d_time_match.group(0)
arr_time = a_time_match.group(0)

print depart_time, arr_time
