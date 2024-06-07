from setuptools import setup, find_packages

setup(
    name="nthscraper",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests==2.31.0",
        "lxml==5.2.1",
        "pandas==2.2.2",
        "urllib3==2.2.1",
        "flask==3.0.3",
        "flask-apscheduler==1.13.1",
        "psutil==5.9.8",
        "pyyaml==6.0.1",
    ],
    entry_points={"console_scripts": ["nthscraper=nthscraper.cli:main"]},
)
