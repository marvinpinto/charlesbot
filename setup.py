from setuptools import setup

long_description = """
Full details available at https://github.com/marvinpinto/charlesbot
"""

setup(
    name='charlesbot',
    version='0.1.0',
    description='Slack Real Time Messaging robot written in Python 3!',
    long_description=long_description,
    author='Marvin Pinto',
    author_email='marvin@pinto.im',
    license='MIT',
    url="https://github.com/marvinpinto/charlesbot",
    packages=['charlesbot'],
    entry_points={
        'console_scripts': [
            'charlesbot = charlesbot.__main__:main'
            ]
    },
    install_requires=[],
    test_suite='nose.collector'
)
