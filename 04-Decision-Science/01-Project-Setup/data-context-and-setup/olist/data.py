import os
import pandas as pd

class Olist:
    def get_data(self):
        """
        This function returns a Python dict.
        Its keys should be 'sellers', 'orders', 'order_items' etc...
        Its values should be pandas.DataFrames loaded from csv files
        """
        # Hints 1: Build csv_path as "absolute path" in order to call this method from anywhere.
            # Do not hardcode your path as it only works on your machine ('Users/username/code...')
            # Use __file__ instead as an absolute path anchor independant of your usename
            # Make extensive use of `breakpoint()` to investigate what `__file__` variable is really
        # Hint 2: Use os.path library to construct path independent of Mac vs. Unix vs. Windows specificities

        file_dir = os.path.dirname(os.path.realpath(__file__))
        csv_path = os.path.join(file_dir, os.pardir, "data","csv")

        file_names = [name for name in os.listdir(csv_path) if ".csv" in name]

        key_names = [name.replace(".csv", "").replace("_dataset", "").replace("olist_", "") for name in file_names]

        data = {}

        for key, file in zip(key_names, file_names):
            data[key] = pd.read_csv(os.path.join(csv_path, file))

        return data


    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")
