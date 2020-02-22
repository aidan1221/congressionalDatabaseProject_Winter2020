import pandas as pd


class CSV_Editor:

    @staticmethod
    def remove_column(csv_file, column_key):
        df = pd.read_csv(csv_file)
        df.drop(column_key)
        df.to_csv(csv_file)


