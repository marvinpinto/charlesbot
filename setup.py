from setuptools import setup

setup(
    name='charlesbot',
    version='0.1.0',
    author='Marvin Pinto',
    author_email='marvin@pinto.im',
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
