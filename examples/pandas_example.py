import datura
import numpy as np
import pandas as pd

df = pd.DataFrame(data={'x':range(11), 'y1':np.arange(11)**2, 'y2':100-np.arange(11)**2})

datura.plot(df['x'], df[['y1','y2']], filename='examples/pandas_example.svg', x_label='x label',
            y_label='y label', title='Pandas Example', labels=df.columns[1:].tolist(),
            x_ticks=[0, 5, 10], y_ticks=[0, 25, 50, 75, 100])