# -*- coding: utf-8 -*-
"""
Created on Sun Jan 07 15:42:18 2018

@author: A

# load transaction page > right click table > inspect > paste cmd
# Use at beginning of next month
"""
import pyperclip
from bs4 import BeautifulSoup as bs
import pandas as pd

pyperclip.copy('copy(document.body.innerHTML)')
d = raw_input('Waiting for HTML copy... no = doing it early.')
html = pyperclip.paste()
soup = bs(html, 'lxml')
trans = soup.findAll("li", {"class": "point-events__list-item"})

pc_gas = []
pc_offers = []
pc_mc = []
pc_other = []
pc_redeem = []

currentday = pd.to_datetime('today')
if d == 'no':
    cutoffdate =  pd.Timestamp(str(currentday.year) + '-' + str(currentday.month) + '-21')
else:
    cutoffdate =  pd.Timestamp(str(currentday.year) + '-' + str(currentday.month-1) + '-21')
cutoffdate2 = cutoffdate - pd.DateOffset(months=1, days=1)

des = [] # debugging
desc2 = []
#pd.to_datetime("Mar 15, 2016", format="%b %d, %Y")

for i in range(len(trans)):
    points = str(trans[i].findAll("span", {"class": "point-event__diff-value"}))
    describe = str(trans[i].findAll("div", {"class": "point-event__subtitle"}))
    
    date = describe.split("<")[2]
    date = date.split(">")[1]
    date = date.split(" ")
    date = date[1][0:3] + " " + date[2] + ", " + str(currentday.year)
    
    des.append(date)
    desc2.append(points)    
    
    if pd.to_datetime(date) < cutoffdate and pd.to_datetime(date) > cutoffdate2:
        if points != '[]': # filter out points
            points = points.split("<")
            points = points[2].split(">")
            points = int(points[1].replace(",", ""))
        else: # no points = 0
            points = 0
        
        if describe.find('PC FINANCIAL MC') != -1: # append points
            points_test = float(points)/100
            if points_test.is_integer():  # find a way to determine PC points from store from PC Financial MC: crude is find double zeros, therefore probably from store
                if points_test > 0:
                    pc_offers.append(points)
                elif points_test < 0:
                    pc_redeem.append(points)
            else:
                pc_mc.append(points)
        elif describe.find('PC Optimum') != -1:
            pc_other.append(points)

pc = pd.DataFrame(index=[0], columns=['Gas','Offers','Card','Other','Redeem'])

pc['Gas'] = sum(pc_gas)
pc['Offers'] = sum(pc_offers)
pc['Card'] = sum(pc_mc)
pc['Other'] = sum(pc_other)
pc['Redeem'] = sum(pc_redeem)

print pc
pc.to_clipboard()

