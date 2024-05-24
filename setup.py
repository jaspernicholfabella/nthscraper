from setuptools import setup, find_packages

setup(
    name="zenscraper",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests==2.31.0",
        "lxml==5.2.1",
        "pandas==2.2.2",
        "urllib3==2.2.1",
    ],
    entry_points={
            "console_scripts": ["zenscraper=zenscraper.cli:main"]
    },
)
