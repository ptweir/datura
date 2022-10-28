import datura

datura.plot([[1, 2, 3], [1, 2, 3]], [[0, 1, 3], [1, 2, 5]], yus=None, yls=None,
            filename='first_example.svg', x_label='my x label', y_label='my y label',
            title='my title', labels=['good', 'better'], x_ticks=[1, 2, 3],
            y_ticks=[0, 2, 4])