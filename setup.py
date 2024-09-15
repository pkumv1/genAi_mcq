from setuptools import find_packages, setup


setup(
    name="mcq generator",
    version="0.0.1",
    author="pavan",
    author_email="pkumv1@gmail.com",
    install_requires=[
        "openai",
        "langchain",
        "pandas",
        "numpy",
        "seaborn",
        "matplotlib",
        "streamlit",
        "pyPDF",
        "python-dotenv",
    ],
    packages=find_packages(),
)
