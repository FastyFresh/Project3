from setuptools import setup, find_packages

setup(
    name="bolt-master-agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "alpaca-trade-api>=3.0.0",
        "python-dotenv>=1.0.0",
        "redis>=5.0.0",
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.9",
        "firebase-admin>=6.2.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scikit-learn>=1.2.0",
        "tensorflow>=2.13.0",
        "click>=8.1.7",
        "cryptography>=43.0.3"
    ],
)

