"""Setup script for the muppy package."""
from distutils.core import setup
import os
import shutil

_version = '0.1'

_description = '(Yet another) memory usage profiler for Python.'
_long_description = 'Muppy tries to help developers to identity memory leaks of Python ' +\
'applications. It enables the tracking of memory usage during runtime and the ' +\
'identification of objects which are leaking. Also, tools are provided which ' +\
'allow to locate the source of not released objects.'

doc_dir = 'doc'
compiled_doc_dir = os.path.join(doc_dir, 'build', 'html')

def copy_doc():
    """Copy all docs to root doc-directory.

    Returns a list of all copied files and directories.
    """
    res = []
    
    files = os.listdir(compiled_doc_dir)
    for entry in files:
        src = os.path.join(compiled_doc_dir, entry)
        dst = os.path.join(doc_dir, entry)
        if os.path.exists(dst):
            if os.path.isfile(dst):
                os.remove(dst)
            elif os.path.isdir(dst):
                shutil.rmtree(dst)
        if os.path.isfile(src):
            shutil.copy2(src, doc_dir)
        elif os.path.isdir(src):
            shutil.copytree(src, os.path.join(doc_dir, entry))
        else:
            raise ValueError, src + " is neither file nor directory"
        res.append(dst)
    return res

def del_copied_docs(files):
    """Delete all files."""
    for file in files:
        if os.path.isfile(file):
            os.remove(file)
        elif os.path.isdir(file):
            shutil.rmtree(file)
        else:
            raise ValueError, file + " is neither file nor directory"

def run_setup():
    setup(name='muppy',
          description=_description,
          long_description = _long_description,

          author='Robert Schuppenies',
          author_email='robert.schuppenies@gmail.com',
          url='http://pypi.python.org/pypi/muppy/' + _version,
          version=_version,
          packages=['muppy'],
          package_dir = {'muppy':'.'},
          license='Apache License, Version 2.0',
          platforms = ['any'],
          classifiers=['Development Status :: 3 - Alpha',
                       'Environment :: Console',
                       'Intended Audience :: Developers',
                       'License :: OSI Approved :: Apache Software License',
                       'Operating System :: OS Independent',
                       'Programming Language :: Python',
                       'Topic :: Software Development :: Bug Tracking',
                       ],
          )

files = copy_doc()
run_setup()
del_copied_docs(files)

