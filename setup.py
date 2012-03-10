import os
import glob

from distutils.core import setup

from Guanandy import getVersion

packages, other_files = [], [],
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('Guanandy/'):
    data_fullpath = []
    data_dirpath = []
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        for f in filenames:
            full = os.path.join(dirpath, f)
            data_dirpath.append(os.path.split(full)[0])
            data_fullpath.append(full)
    other_files.extend(zip(data_dirpath, [data_fullpath]))

data_files = [
    ('', glob.glob('teacher.py')),
    ('', glob.glob('student.py')),
    ]

data_files.extend(other_files)

setup(name='guanandy',
    version=getVersion().replace(' ', '-'),
    description='Guanandy',
    author='Wiliam Souza',
    author_email='wiliamsouza83@gmail.com',
    url='',
    download_url='',
    package_dir={'Guanandy': 'Guanandy'},
    packages=packages,
    data_files=data_files,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: GPL',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Libraries :: Python Modules',]
    )
