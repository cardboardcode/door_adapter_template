import os
from glob import glob
from setuptools import setup

package_name = 'door_adapter_mock'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
         glob(os.path.join('launch', '*launch.[pxy][yma]*')))
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Gary Bey',
    maintainer_email='beyhy94@gmail.com',
    description='A mock RMF Door Adapter',
    license='Apache 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'door_adapter_mock_node = door_adapter_mock.door_adapter:main',
            'mock_door_server = door_adapter_mock.mock_door_server:main'
        ],
    },
)
