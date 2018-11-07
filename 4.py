#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Gilbert Zhu

Application of the SA-CCR to sample portfolios:
https://www.bis.org/publ/bcbs279.pdf

This script generates results for Example 4 in the above document.
"""

import math
import numpy as np
import pandas as pd
from scipy.stats import norm
from SA_CCR_helper import *

alpha = 1.4
Floor = 0.05

df1 = pd.read_csv('Input_1.csv')
df2 = pd.read_csv('Input_2.csv')
df4 = pd.read_csv('Input_4.csv')

V = float(df1['Market value (thousands)'].sum() + df2['Market value (thousands)'].sum())
C = 0.0
RC = RC_unmargined(V, C)

AddOn_agg = float((df4['AddOn_IR'] + df4['AddOn_CR']).sum())

if (V - C >= 0) and (V >= 0):
    multiplier = 1.0
else:
    multiplier = multiplier_activated(Floor, V, C, AddOn_agg)

EAD = Compute_EAD(alpha, RC, multiplier, AddOn_agg)

results = [(RC, AddOn_agg, multiplier, EAD)]
result_cols = ['RC', 'AddOn', 'Multiplier', 'EAD']

dfout = pd.DataFrame(results, columns = result_cols)

writer = pd.ExcelWriter('Output_4.xlsx')
dfout.to_excel(writer,'Sheet1',index=False)
writer.save()




