from setuptools import setup

setup(
    name='usgs_api_client',
    version='0.1',
    py_modules=['usgs_api_client'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        usgs_api_client=usgs_api_client:cli
    ''',
)