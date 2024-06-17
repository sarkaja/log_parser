from setuptools import setup, find_packages

setup(
    name='log_parser',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'chardet==5.2.0',
        'numpy==2.0.0',
        'pandas==2.2.2',
        'python-dateutil==2.9.0.post0',
        'pytz==2024.1',
        'six==1.16.0',
        'tzdata==2024.1'
    ],
    entry_points={
        'console_scripts': [
            'log_parser_package=log_parser.log_structurer:main',
        ],
    },
    author='Šárka Jadviščoková',
    author_email='sarka.jadviscokova@gmail.com',
    description='Package for parsing certain text log files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vasuzivatel/my_log_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
