from setuptools import setup

setup(
    name='streak',
    version='0.1.0',
    py_modules=['streak'],
    install_requires=[
        'Click', 'pandas'
    ],
    entry_points={
        'console_scripts': [
            'streak = streak:cli',
        ],
    },
)