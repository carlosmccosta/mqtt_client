from setuptools import find_packages, setup

setup(
    name='mqtt_client',
    packages=find_packages(),
    version='1.0.0',
    description='mqtt_client',
    author='Carlos Miguel Correia da Costa',
    author_email='carloscosta.cmcc@gmail.com',
    license='MIT',
    install_requires=['paho_mqtt==1.6.1'],
)
