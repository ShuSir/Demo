import urllib2
import pandas
import BeautifulSoup
import requests
import pandas as pd
from datetime import timedelta, date
import calendar
import re
import numpy as np
import xlsxwriter
import os
import sys


with requests.Session() as s:
    checker = s.get('https://data.bls.gov/timeseries/CEU3133600108?amp%253bdata_tool=XGtable&output_view=data&include_graphs=true')
    data = checker.text
    soup = BeautifulSoup.BeautifulSoup(data)

#souptext=soup.getText('\n')

REMOVE_ATTRIBUTES = [
    'lang','language','onmouseover','onmouseout','script','style','font',
    'dir','face','size','color','style','class','width','height','hspace',
    'border','valign','align','background','bgcolor','text','link','vlink',
    'alink','cellpadding','cellspacing']

for tag in soup.recursiveChildGenerator():
    try:
        tag.attrs = [(key,value) for key,value in tag.attrs
                     if key not in REMOVE_ATTRIBUTES]
    except AttributeError:
        pass

table=soup.findAll("tbody")[1]
#print(table)

def parse_html_table(table):
    n_columns = 0
    n_rows=0
    column_names = []

    for row in table.findAll('tr'):
        td_tags = row.findAll('td')
        if len(td_tags) > 0:
            n_rows=n_rows+1
            if n_columns == 0:
                n_columns = len(td_tags)

    df = pd.DataFrame(columns = range(0,n_columns), index= range(0,n_rows))
    row_marker = 0
    for row in table.findAll('tr'):
        column_marker = 0
        columns = row.findAll('td')
        for column in columns:
            df.iat[row_marker,column_marker] = column.getText()
            column_marker += 1
        if len(columns) > 0:
            row_marker += 1

    table_headers=[]
    for tx in table.findAll('th'):
        table_headers.append(tx.getText())

    df=df.set_index([table_headers])

    return df

salary=parse_html_table(table)
salary.columns = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

print(salary)

directory  = '/Users/ShuSir/Desktop/'
filename= 'Salary.csv'
local_filename=os.path.join(directory, filename)
print(local_filename)
salary.to_csv(local_filename, encoding='utf-8')
