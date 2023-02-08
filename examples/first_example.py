import datura

datura.plot([[1, 2, 3], [1, 3]], [[0, 1, 3], [1, 4]],
            filename='examples/first_example.svg', x_label='x label',
            y_label='y label', title='First Example',
            labels=['good', 'better'])
