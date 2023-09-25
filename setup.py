from setuptools import setup, find_packages

setup(
    name='users',
    version='0.1',
    description='users',
    author='jay',
    author_email='jay@atomicloops.com',
    packages=find_packages(),
    install_requires=[
        'Django==4.1.4',
        'django-filter==22.1',
        'djangorestframework==3.14.0'
        # Other dependencies
    ],
)
