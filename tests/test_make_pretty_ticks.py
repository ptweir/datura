import datura


def test_num2pretty_string():

    in_outs = [[0, '0'], [-10, '-10'], [10000, '10K'], [2e9, '2B']]
    for in_out in in_outs:
        _out = datura.draw._num2pretty_string(in_out[0])
        assert _out == in_out[1]
