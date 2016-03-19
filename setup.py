from setuptools import setup, find_packages
import codecs

# README into long description
with codecs.open('README.rst', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='charlesbot',
    version='0.10.1',
    description='CharlesBOT is a Python bot written to take advantage of Slack\'s Real Time Messaging API',
    long_description=readme,
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
        "slackclient==0.16",
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
