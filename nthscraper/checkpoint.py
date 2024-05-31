import csv
import pickle
from pathlib import Path
from nthscraper.logger import setup_logger
from typing import List, Optional

logger = setup_logger()


class Checkpoint:
    def __init__(self, pickle_file: str):
        self.pickle_path = Path(pickle_file).parent
        self.pickle_file = Path(pickle_file)
        self.csv_file = self.pickle_file.with_suffix(".list_data.csv")
        self.exists = self.pickle_file.exists()
        self.pickle_path.mkdir(parents=True, exist_ok=True)

    def save_checkpoint(self, list_data: List[str]):
        """
        Save data to a CSV file as checkpoints. Each item in the list is saved as a row
        :param list_data: the data to save, typically string of URL's
        """
        field_names = ["ListData"]
        dict_data = {"ListData": list_data}

        with open(self.csv_file, "a") as csv_file:
            dict_object = csv.DictWriter(csv_file, fieldnames=field_names)
            dict_object.writerow(dict_data)

        logger.info("Checkpoint saved to CSV at %s", self.csv_file)

    def load_checkpoint(
        self, filter_from_list: Optional[List[str]] = None
    ) -> List[str]:
        """
        Load checkpoint data from a CSV file. Optionally filter data from the
        provided list.

        :param filter_from_list: List to compare with checkpoint data.
        """
        if self.csv_file.exists():
            with self.csv_file.open("r") as f:
                reader = csv.reader(f)
                saved_list = [row[0] for row in reader]

            if filter_from_list is not None:
                return [val for val in filter_from_list if val not in saved_list]

            return saved_list

        return filter_from_list if filter_from_list is not None else []

    def save_data(self, object_to_save):
        """
        Save a Python object to a pickle file.
        :param object_to_save: the python object to save.
        """
        self.pickle_path.mkdir(parents=True, exist_ok=True)
        with self.pickle_file.open("wb") as handle:
            pickle.dump(object_to_save, handle, protocol=pickle.HIGHEST_PROTOCOL)
        logger.info("Data saved to pickle file at %s", self.pickle_file)

    def load_data(self):
        """
        Load data from a pickle file.
        :returns: loaded object from picke if file exists, otherwise None.
        """
        if self.pickle_file.exists():
            with self.pickle_file.open("rb") as handle:
                return pickle.load(handle)
        logger.warning(f"Pickle file does not exist {self.pickle_file}")
        return None
