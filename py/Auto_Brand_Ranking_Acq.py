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
import locale



with requests.Session() as s:
    checker = s.get('http://www.thetruthaboutcars.com/2017/06/usa-auto-brand-sales-results-may-2017-ytd/')
    data = checker.text
    soup = BeautifulSoup.BeautifulSoup(data)

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


table=soup.findAll("tbody")[0]

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
                th_tags = row.findAll('td')
                if len(th_tags) > 0 and len(column_names) == 0:
                    for th in th_tags:
                        column_names.append(th.getText())

    columns=column_names if len(column_names) > 0 else range(0,n_columns)


    df = pd.DataFrame(columns = range(0,n_columns), index= range(0,n_rows))
    row_marker = 0
    for row in table.findAll('tr'):
        column_marker = 0
        columns = row.findAll('td')
        for column in columns:
            #print(row_marker,column_marker)
            df.iat[row_marker,column_marker] = column.getText()
            column_marker += 1
        if len(columns) > 0:
            row_marker += 1
    df.columns = df.iloc[0]
    df = df[df.index!= 0]

    return df

brand=(parse_html_table(table))
leng=len(brand['2017 YTD'])
for i in range(1,leng):
    "".join(brand['2017 YTD'][i].split(','))
    #brand['2017 YTD'][i].replace(',','')
    print(brand['2017 YTD'][i])
print(brand['2017 YTD'].dtypes)
# directory  = '/Users/ShuSir/Desktop/Sublime/dashboard/data'
# filename= 'Brand.csv'
# local_filename=os.path.join(directory, filename)
# print(local_filename)
# brand.to_csv(local_filename, encoding='utf-8')

