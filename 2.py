#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Gilbert Zhu

Application of the SA-CCR to sample portfolios:
https://www.bis.org/publ/bcbs279.pdf

This script generates results for Example 2 in the above document.
"""

import math
import numpy as np
import pandas as pd
from scipy.stats import norm
from SA_CCR_helper import *

alpha = 1.4
Floor = 0.05

df = pd.read_csv('Input_2.csv')

V = float(df['Market value (thousands)'].sum())
C = 0.0
RC = RC_unmargined(V, C)

# PFE Add-On:
#IR, CR, CO, EQ, FX

# Start date:
df['S'] = [0, 0, 0]
# End date:
df['E'] = [3, 6, 5]
# Supervisory duration:
df['SD'] = df.apply(lambda x: SD_IR_CR(x['S'], x['E']), axis=1)
# Adjusted notional:
df['d'] = df['Notional (thousands)'].multiply(df['SD'])
# Supervisory delta:
df['delta'] = [1, -1, 1]
# Maturity factor:
df['MF'] = [1, 1, 1]
# Supervisory factors:
df['SF'] = [0.0038, 0.0054, 0.0038]

df['AddOn'] = df['delta'].multiply(df['d']).multiply(df['MF']).multiply(df['SF'])
# Correlation factor:
df['rho'] = [0.5, 0.5, 0.8]
df['AddOn times rho'] = df['AddOn'].multiply(df['rho'])
df['AddOn**2'] = df['AddOn'].multiply(df['AddOn'])
df['1 - rho**2'] = 1 - df['rho'].multiply(df['rho'])
df['AddOn**2 times (1-rho**2)'] = df['AddOn**2'].multiply(df['1 - rho**2'])

Systematic = (df['AddOn times rho'].sum())**2
Idiosyncratic = df['AddOn**2 times (1-rho**2)'].sum()

AddOn_CR = math.sqrt(Systematic + Idiosyncratic)
AddOn_agg = AddOn_CR

if (V - C >= 0) and (V >= 0):
    multiplier = 1.0
else:
    multiplier = multiplier_activated(Floor, V, C, AddOn_agg)

EAD = Compute_EAD(alpha, RC, multiplier, AddOn_agg)

results = [(RC, Systematic, Idiosyncratic, AddOn_agg, multiplier, EAD)]
result_cols = ['RC', 'Systematic', 'Idiosyncratic', 'AddOn', 'Multiplier', 'EAD']

df2 = pd.DataFrame(results, columns = result_cols)

writer = pd.ExcelWriter('Output_2.xlsx')
df.to_excel(writer,'Sheet1',index=False)
df2.to_excel(writer,'Sheet2',index=False)
writer.save()

