import pandas as pd
from urllib import parse
import pyperclip

PROJECT_NAME = "proj_name"

URL_COLUMN = "url"
INPUT_FILE = "origin.csv"
TARGET_COLUMN = "manual_label"
SOURCE_COLUMNS = ["First", "Second"]

LABEL_OPTIONS = ["0", "1"]

PRINT_BUFFER = 5


def save_state(data, fname=None):
    if fname is None:
        fname = str(len(data))
    # TODO make dir os agnostic
    fname = PROJECT_NAME + "/" + fname + ".csv"
    data.to_csv(fname)


def print_options(label_keys):
    print("(s) Save | (e) Exit | (h) Help | (l) Load | (t) Tail, | (c) Copy")
    for key, value in label_keys.items():
        print(f"({key}) {value}")


def load_existing():
    to_load = input("Enter save number: ")
    # TODO make OS agnostic
    return pd.read_csv(PROJECT_NAME + "/" + str(to_load) + ".csv")


def label_data(data):
    data.loc[:, TARGET_COLUMN] = None
    label_keys = {}
    label_index = 1
    for option in LABEL_OPTIONS:
        label_keys[str(label_index)] = option
        label_index += 1
    print_options(label_keys)
    index = 0
    while index < len(data):
        for column in SOURCE_COLUMNS:
            # TODO delete
            if column == URL_COLUMN:
                print(column, ":", parse.unquote(data.iloc[index][column]))
            else:
                print(column, ":", data.iloc[index][column])
        user_input = input(str(index) + ": ")
        for char in user_input:
            if char == "s":
                save_state(data, fname=str(index))
            if char == "e":
                exit()
            if char == "h":
                print_options(label_keys)
            if char == "l":
                data = load_existing()
            if char == "t":
                if index <= PRINT_BUFFER:
                    print(data.head())
                else:
                    print(data[: index + 1].tail())
            # TODO delete
            if char == "c":
                pyperclip.copy(parse.unquote(data.iloc[index][URL_COLUMN]))
            if char in label_keys.keys():
                data.loc[index, TARGET_COLUMN] = label_keys[char]
                print("Labeled: ", label_keys[char])
                index += 1


if __name__ == "__main__":
    # load file TODO make dir os agnostic
    data = pd.read_csv(PROJECT_NAME + "/" + INPUT_FILE)
    print(data)
    if TARGET_COLUMN in data.columns:
        raise Exception("The target column name already exists in the data")
    for column in SOURCE_COLUMNS:
        if column not in data.columns:
            raise Exception("Source column: " + str(column) + ", is not in the data")
    labeled_data = label_data(data)
    save_state(data, "final")
