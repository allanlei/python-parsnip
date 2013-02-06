"""
python-parsnip
----------

"""
from setuptools import setup
from setuptools import find_packages


setup(
    name='python-parsnip',
    version='0.1.0',
    url='https://github.com/allanlei/python-parsnip',
    license='BSD',
    author='Allan Lei',
    author_email='allanlei@helveticode.com',
    description='Configuration helpers',
    long_description=__doc__,
    packages=find_packages(),
    zip_safe=False,
    platforms='any',
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)