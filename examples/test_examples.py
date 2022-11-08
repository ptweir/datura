import os
import runpy

example_filenames = [fn for fn in os.listdir('examples') if fn.endswith('_example.py')]

for example_filename in example_filenames:
    print(example_filename)

    runpy.run_path(os.path.join('examples', example_filename))

    out_svg = os.path.join('examples', example_filename.replace('.py', '.svg'))
    persistent_svg = os.path.join('examples', example_filename.replace('.py', '_persistent.svg'))
    print(out_svg)
    print(persistent_svg)
    with open(out_svg) as out_svg_file:
        with open(persistent_svg) as persistent_svg_file:
            assert out_svg_file.read() == persistent_svg_file.read()