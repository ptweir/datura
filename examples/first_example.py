import datura

datura.plot([[1, 2, 3], [1, 2, 3]], [[0, 1, 3], [1, 2, 5]], yus=None, yls=None,
            filename='examples/first_example.svg', x_label='x label',
            y_label='y label', title='First Example',
            labels=['good', 'better'], x_ticks=[1, 2, 3], y_ticks=[0, 2, 4])
