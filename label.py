import pandas as pd

INPUT_FILE = "test.csv"
TARGET_COLUMN = "label"
SOURCE_COLUMNS = ["zip"]

LABEL_OPTIONS = ["First", "Second"]

PRINT_BUFFER = 5


def save_state(data, fname=None):
    if fname is None:
        fname = str(len(data))
    fname = fname + ".csv"
    data.to_csv(fname)


def print_options(label_keys):
    print("(s) Save | (e) Exit | (h) Help")
    for key, value in label_keys.items():
        print(f"({key}) {value}")


def load_existing():
    to_load = input("Enter save number: ")
    return pd.read_csv(str(to_load) + ".csv")


def label_data(data):
    data.loc[:, TARGET_COLUMN] = None
    label_keys = {}
    label_index = 1
    for option in LABEL_OPTIONS:
        label_keys[str(label_index)] = option
        label_index += 1
    print_options(label_keys)
    for index in range(len(data)):
        print(data.iloc[index][SOURCE_COLUMNS])
        user_input = input(">> ")
        for char in user_input:
            if char == "s":
                save_state(data)
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
                    print(data[:index + 1]
            if char in label_keys.keys():
                data.loc[index, TARGET_COLUMN] = label_keys[char]
                print("Labeled: ", label_keys[char])


if __name__ == "__main__":
    # load file
    data = pd.read_csv(INPUT_FILE)
    print(data)
    if TARGET_COLUMN in data.columns:
        raise Exception("The target column name already exists in the data")
    for column in SOURCE_COLUMNS:
        if column not in data.columns:
            raise Exception("Source column: " + str(column) + ", is not in the data")
    labeled_data = label_data(data)
    save_state(data, "final")
