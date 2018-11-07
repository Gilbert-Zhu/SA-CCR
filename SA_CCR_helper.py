#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: Gilbert Zhu

This file contains several functions to help calculate some of the intermediate
steps and final numbers for SA-CCR: https://www.bis.org/publ/bcbs279.pdf

It currently supports Example 1, 2 and 4 in its Annex 4a.
More functions can be added to support more examples.
Most functions are self-explanatory and comments are omitted.

Make sure this file and the main scripting files are in the same directory.
"""

import math
import numpy as np
import pandas as pd
from scipy.stats import norm

def Compute_EAD(alpha, RC, multiplier, AddOn_agg):
    return alpha * (RC + multiplier * AddOn_agg)

def RC_unmargined(V, C):
    return max(V - C, 0.0)

def RC_margined(V, C, TH, MTA, NICA):
    return max(V - C, TH + MTA - NICA, 0.0)

def SD_IR_CR(S, E):
    return (math.exp(-0.05*S) - math.exp(-0.05*E))/0.05
     
def delta_options(is_Call, is_Bought, P, K, T, sigma):
    is_Call = 2 * int(is_Call) - 1
    is_Bought = 2 * int(is_Bought) - 1
    P, K, T, sigma = float(P), float(K), float(T), float(sigma)
    temp = (math.log(P/K) + 0.5 * (sigma**2) * T)/(sigma * math.sqrt(T))
    return is_Bought * norm.cdf(is_Call * temp)
    
def EffectiveNotional_IR(D1,D2,D3):
    return math.sqrt(D1**2 + D2**2 + D3**2 + 1.4*D1*D2 + 1.4*D2*D3 + 0.6*D1*D3)

def multiplier_activated(Floor, V, C, AddOn_agg):
    temp = math.exp( (V-C) / (2*(1-Floor)*AddOn_agg) )
    return min(1, Floor + (1-Floor) * temp)




