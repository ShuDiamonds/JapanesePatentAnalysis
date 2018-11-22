#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 18:14:52 2018

@author: shuichi
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.font_manager import FontProperties

df=pd.DataFrame({u"うし":[580, 420],
                 u"とり":[280, 260],
                 u"ぶた":[300, 320]},
               index=(u"肉屋", u"スーパー"))

ax=plt.figure().add_subplot(111, projection='3d')
fp=FontProperties(size=10)

xpos,ypos=np.meshgrid(np.arange(len(df.index)), np.arange(len(df.columns)))
xpos=xpos.flatten()
ypos=ypos.flatten()
zpos=np.zeros(len(xpos))
dx=np.full(len(xpos), 0.05)
dy=np.full(len(ypos), 0.1)
dz=df.as_matrix().flatten()
ax.bar3d(xpos, ypos, zpos, dx, dy, dz)

ax.set_xlabel(u"お店", fontproperties=fp)
ax.set_ylabel(u"種類", fontproperties=fp)
ax.set_zlabel(u"金額", fontproperties=fp)
plt.xticks(np.arange(len(df.index)),   df.index, fontproperties=fp)
plt.yticks(np.arange(len(df.columns)), df.columns, fontproperties=fp)

plt.axis([-0.5, len(df.index)-0.5, -0.5, len(df.columns)-0.5])
