import os
import argparse
from nthscraper.utils import FileUtils


def main():
    parser = argparse.ArgumentParser(description="NthScraper CLI tool")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    init_parser = subparsers.add_parser(
        "init", help="Initialize the nthscraper project in the current directory"
    )
    init_parser.set_defaults(func=create_project)

    # Parse the arguments
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
    else:
        args.func()


class YamlGeneration:
    """
    this is a class to generate yaml files for web settings and initial
    """

    def generate_settings(self):
        """generate yaml settings for the web interface automation system"""
        settings = [
            "web:\n",
            " host: '0.0.0.0'\n",
            " port: '5001\n",
            "scheduler:\n",
            " type: 'threadpool'\n"
            " coalesce: False\n"
            " max_instances: 3\n"
            " max_workers: 20\n"
            " api_enabled: True\n"
            " db: 'sqlite:///jobs.sqlite'\n",
        ]
        file_path = os.path.join(os.getcwd(), "settings.yml")
        with open(file_path, "w", encoding="utf8") as f:
            for line in settings:
                f.write(line)


class NthScraperFileStructure:
    """nthscraper file structure"""

    def generate(self):
        """generate directory for"""
        FileUtils().create_directory("./projects")
        FileUtils().create_directory("./tests")
        FileUtils().create_directory("./admin")
        yaml_gen = YamlGeneration()
        yaml_gen.generate_settings()


def create_project():
    """generate yaml files for settings"""
    NthScraperFileStructure().generate()


if __name__ == "__main__":
    main()
