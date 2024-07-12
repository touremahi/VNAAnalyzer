from setuptools import setup, find_packages

setup(
    name="VNAAnalyzer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "PySide6",
        "matplotlib",
        "scikit-rf",
    ],
    entry_points={
        'console_scripts': [
            'vna-analyzer = vna_analyzer.main:main',
        ],
    },
)
