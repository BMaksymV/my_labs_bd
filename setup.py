from setuptools import setup, find_packages

setup(
    name='fablab_backend',
    version='1.0.0',
    description='REST API for FabLab Database',
    author='Твоє Ім\'я',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask==3.0.0',
        'Flask-SQLAlchemy==3.1.1',
        'Flask-Marshmallow==0.15.0',
        'PyMySQL==1.1.0',
        'PyYAML==6.0.2'
    ],
)
