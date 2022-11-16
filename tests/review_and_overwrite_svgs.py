import glob
import os
import webbrowser
import shutil

svg_filenames = list(glob.iglob('../**/*.svg', recursive=True))
svg_filenames.sort()
svg_filenames = [os.path.abspath(fn) for fn in svg_filenames]
for svg_filename in svg_filenames:
    persistent_name = svg_filename.split('.')[0] + '_persistent' + '.svg'
    backup_name = svg_filename.split('.')[0] + '_BACKUP' + '.svg'
    if persistent_name in svg_filenames:
        print(svg_filename)
        print(persistent_name)
        webbrowser.open('file://' + svg_filename, new=2)
        webbrowser.open('file://' + persistent_name, new=2)
        instr = input('replace? (y/n)')
        if instr == 'y':
            shutil.copyfile(persistent_name, backup_name)
            shutil.copyfile(svg_filename, persistent_name)
            print('done')
