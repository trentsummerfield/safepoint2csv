from setuptools import setup

setup(
    name='safepoint2csv',
    version='1.0.0',
    packages=['safepoint2csv'],
    entry_points={
        'console_scripts': ['safepoint2csv = safepoint2csv.__main__:main']
    })
