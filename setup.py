# setup.py

from setuptools import setup, find_packages

setup(
    name='revCause',  # Replace with your package name
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'fastkde',
        'numpy',
        'scipy'
    ],
    author='Your Name',
    author_email='soumik@pitt.edu',
    description='A package for running reverse causality estimator function',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/soumikp/revCause',  # Optional, replace with your package URL
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
