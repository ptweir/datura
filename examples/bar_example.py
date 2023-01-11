import datura
import pandas as pd


x_ticks_text = ['Boreas', 'Zephryos', 'Notos', 'Euros']
df = pd.DataFrame(data={'Night': [2, 5, 8, 3],
                        'Day': [1, 5, 6, 4]})

datura.bar(df, filename='examples/bar_example.svg', x_ticks_text=x_ticks_text)
