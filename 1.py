#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Gilbert Zhu

Application of the SA-CCR to sample portfolios:
https://www.bis.org/publ/bcbs279.pdf

This script generates results for Example 1 in the above document.
"""

import math
import numpy as np
import pandas as pd
from scipy.stats import norm
from SA_CCR_helper import *

alpha = 1.4
Floor = 0.05

df = pd.read_csv('Input_1.csv')

V = float(df['Market value (thousands)'].sum())
C = 0.0
RC = RC_unmargined(V, C)

# PFE Add-On:
#IR, CR, CO, EQ, FX

df['Hedging set'] = df['Base currency']
df['Time bucket'] = [3, 2, 3]
# Start date:
df['S'] = [0, 0, 1]
# End date:
df['E'] = [10, 4, 11]
# Supervisory duration:
df['SD'] = df.apply(lambda x: SD_IR_CR(x['S'], x['E']), axis=1)
# Adjusted notional:
df['d'] = df['Notional (thousands)'].multiply(df['SD'])
# Supervisory delta:
delta_3 = delta_options(False, False, 0.06, 0.05, 1, 0.5)
df['delta'] = [1, -1, delta_3]
# Maturity factor:
df['MF'] = [1, 1, 1]
# Effective notional:
df['D'] = df['delta'].multiply(df['d']).multiply(df['MF'])

EffectiveNotional_USD = EffectiveNotional_IR(0,df['D'][1],df['D'][0])
EffectiveNotional_EUR = EffectiveNotional_IR(0,0,df['D'][2])

# Supervisory factors:
SF_USD = 0.005
SF_EUR = 0.005

AddOn_IR = SF_USD * EffectiveNotional_USD + SF_EUR * EffectiveNotional_EUR
AddOn_agg = AddOn_IR

if (V - C >= 0) and (V >= 0):
    multiplier = 1.0
else:
    multiplier = multiplier_activated(Floor, V, C, AddOn_agg)

EAD = Compute_EAD(alpha, RC, multiplier, AddOn_agg)

results = [(RC, EffectiveNotional_USD, EffectiveNotional_EUR,
           AddOn_agg, multiplier, EAD)]
result_cols = ['RC', 'EffectiveNotional_USD', 'EffectiveNotional_EUR',
           'AddOn', 'Multiplier', 'EAD']

df2 = pd.DataFrame(results, columns = result_cols)

writer = pd.ExcelWriter('Output_1.xlsx')
df.to_excel(writer,'Sheet1',index=False)
df2.to_excel(writer,'Sheet2',index=False)
writer.save()
