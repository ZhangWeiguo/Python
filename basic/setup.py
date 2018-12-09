from setuptools import setup, find_packages


setup(
    name            = "testz",
    version         = "0.0",
    author          = "Wego",
    author_email    = "zhenyuan.zwg@alibaba-inc.com",
    description     = "Test File",
    packages        = ["testz"]
)

'''
testz is a Path with __init__.py
build
    python setup.py bdist
    python setup.py bdist_egg
install
    python setup.py install
    easy_install XXX.egg
uninstall
    pip uninstall XXX
    easy_install -m XXX

you can also use pyinstaller generate a executable file
    with some files:    pyinstaller XXX.py -n YYY  
    with one files:     pyinstaller XXX.py -F -n YYY
'''

