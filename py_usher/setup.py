from setuptools import setup, find_packages

setup(
    name='py-usher',
    version='0.1.0',
    description='A package for managing events and operations using threading/multiprocessing',
    author='Amit Nakash',
    packages=find_packages(),
    install_requires=[
        'py-shiftmanager',
        'dill',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
