from datetime import datetime
import numpy as np
import pandas as pd

time_range = pd.date_range(start='2021-01-01', end='2022-01-01', freq='MS')

df = pd.DataFrame(data={'t':time_range, 'y1':np.sin(np.linspace(0, 2*np.pi, 13)), 'y2':np.cos(np.linspace(0, 2*np.pi, 13))})

x_ticks = []
for tick_ind, tick in enumerate(df.t.tolist()):
    if tick_ind%3 == 0:
        x_ticks.append(tick)

plot(df['t'], df[['y1','y2']], filename='time_example.svg', x_label='x label',
            y_label='y label', title='Time Example', labels=df.columns[1:].tolist(),
            x_ticks=x_ticks, y_ticks=[-1, 0, 1])