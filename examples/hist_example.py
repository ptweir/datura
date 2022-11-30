import datura
import numpy as np
import pandas as pd

rng = np.random.RandomState(10)

ar = np.vstack((rng.normal(loc=-2, scale=1.5, size=5000),
                rng.normal(loc=0, scale=2, size=5000),
                rng.normal(loc=3, scale=1.5, size=5000))).T

df = pd.DataFrame(data={'yb': ar[:, 0],
                        'yy': ar[:, 1],
                        'yg': ar[:, 2]})

datura.hist(data=df[['yb', 'yy', 'yg']],
            bin_edges=np.linspace(-10, 10, 100),
            filename='examples/hist_example.svg',
            x_label='Days until ready to eat',
            y_label='Number of bananas',
            colors=['brown', 'gold', 'green'],
            labels=['brown', 'yellow', 'green'],
            label_nudges=[0, 10, 20],
            x_ticks=[-10, -5, 0, 5, 10],
            y_ticks=[0])
