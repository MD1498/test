#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 20:49:26 2021

@author: mdiedrichsen
"""

import glob
import pandas as pd
import numpy as np
from dateutil.parser import parse
import datefinder
import datetime
import time

configfiles = glob.glob('/home/mdiedrichsen/Data/newqc/flight_190527_4.dat', recursive = True)
files = configfiles[0:]

for f in files:
    #date = parse(f, fuzzy=True, yearfirst=True)
    #parse can isolate the date/time from a string, but has string format issues
    #eg: "Wind_20190524" and "Wind_20190524_01" works, but "Lid2_20190524" and Wind_20190524_1" doesn't
    df = pd.read_csv(f, sep = ' ', engine='python')
    df.columns = list(df)
    Lat = df[str([col for col in df.columns if "lat" in col][0])]
    #latitude = df[str(Lat[0])]
    filedate = f.split("/")[5]
    date = datetime.datetime.strptime(str(filedate).split("_")[1], "%y%m%d")
    julianday = date.strftime('%j')
    hour = df[str([col for col in df.columns if "hour" in col][0])]
    #t = [col for col in df.columns if "hour" and "time" in col]
    #working on adding multiple keywords to look for in column headers
    hours = []
    for t in hour:
        if t != float(t):
            h = round((pd.Timedelta(hours=int(t.split(':')[0]),minutes=int(t.split(':')[1]),seconds=int(t.split(':')[2]))).total_seconds()/3600, 4)
            if h<12.1:
                h = h+24.
        else:
            h = t
        hours.append(h)
    #i = pd.to_numeric(df.iloc[:,1], errors = 'coerce')
    for i in np.arange(0, len(hours)):
        if hours[i]<12:
            hours[i]= hours[i]+24
    julianthisyear = pd.Series(float(julianday)+np.asarray(hours)/24.)
