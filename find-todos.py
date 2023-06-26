from __future__ import annotations

import os


def main():
    TODOs = {'folders': [], 'files': []}
    for root, dirs, filenames in os.walk('../projects-dev'):
        for dir in dirs:
            if 'TODO' in dir:
                TODOs['folders'].append(os.path.abspath(dir))

        for filename in filenames:
            if 'TODO' in filename:
                TODOs['folders'].append(os.path.abspath(filename))

    if len(TODOs["folders"]) > 0:
        print(f'{len(TODOs["folders"])} TODO Folders:')
        for folder in TODOs['folders']:
            print(f'\t{folder}')

    if len(TODOs["files"]) > 0:
        print(f'\n{len(TODOs["files"])} TODO Files:')
        for folder in TODOs['files']:
            print(f'\t{folder}')

    print()


if __name__ == '__main__':
    main()