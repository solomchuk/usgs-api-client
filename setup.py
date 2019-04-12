from setuptools import setup

setup(
    name='usgs_api_client',
    version='0.2.1',
    url='https://github.com/solomchuk/usgs-api-client',
    author='Max Solomcuk',
    author_email='max.solomcuk@cgi.com',
    license='MIT',
    description='A Python client for the USGS EarthExplorer Inventory API',
    py_modules=['usgs_api_client'],
    install_requires=[
        'Click',
        'requests',
        'pyyaml',
    ],
    entry_points='''
        [console_scripts]
        usgs_api_client=usgs_api_client:cli
    ''',
)