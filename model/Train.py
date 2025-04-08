import os


class Train:
    def __init__(self):
        self.__train_data = {}
        self.__load_train_data("src/train/upward")
        self.__load_train_data("src/train/downward")

    def __load_train_data(self, directory: str):
        if not os.path.isdir(directory):
            raise FileNotFoundError("train files are missing.")
        way = directory.split('/')[-1]
        for sf in os.listdir(directory):
            self.__train_data[way][sf.replace(".txt", "")] = {}
            with open(f"{directory}/{sf}", 'r', encoding='UTF-8') as file:
                lines = file.readlines()
            for line in lines:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    if key == "BOOKED" and value == "":
                        self.__train_data[way][sf.replace(".txt", "")][key] = {}
                    else:
                        self.__train_data[way][sf.replace(".txt", "")][key] = value
