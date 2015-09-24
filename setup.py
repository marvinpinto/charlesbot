from setuptools import setup, find_packages

long_description = """
Full details available at https://github.com/marvinpinto/charlesbot
"""

setup(
    name='charlesbot',
    version='0.5.0',
    description='Slack Real Time Messaging robot written in Python 3!',
    long_description=long_description,
    author='Marvin Pinto',
    author_email='marvin@pinto.im',
    license='MIT',

   # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='slack robot chatops automation',

    url="https://github.com/marvinpinto/charlesbot",
    packages=find_packages(
        exclude=[
            'Makefile',
            'docker',
            'images',
            'requirements-dev.txt',
            'requirements.txt',
            'tests'
        ]
    ),

    entry_points={
        'console_scripts': ['charlesbot = charlesbot.__main__:main']
    },

    install_requires=[
        "slackclient",
        "websocket-client",
        "cchardet",
        "aiohttp",
        "PyYAML",
        "aiocron",
        "croniter",
        "python-dateutil",
    ],

    test_suite='nose.collector'
)
