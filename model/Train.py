import os


class Train:
    def __init__(self, way: str):
        self.way = way
        self.__train_data = []
        self.__load_train_data(f"src/train/{self.way}")

    def __load_train_data(self, directory: str):
        """
        기차 데이터 로드 함수입니다.
        클래스 선언 시 init 함수에서 함께 실행됩니다.
        __train_data 배열에 상행/하행에 대한 기차 정보를 저장합니다.
        :param directory: 기차 데이터를 가져올 폴더(upward/downward 구분 위함)
        :return:
        """
        if not os.path.isdir(directory):
            raise FileNotFoundError("train files are missing.")
        for sf in os.listdir(directory):
            data = {}
            with open(f"{directory}/{sf}", 'r', encoding='UTF-8') as file:
                lines = file.readlines()
            for line in lines:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    if key == "BOOKED" and value == "":
                        data[key] = []
                    else:
                        try:
                            data[key] = int(value)
                        except ValueError:
                            data[key] = value.split(",")
            self.__train_data.append(data)

    def get_all_train_data(self) -> dict:
        """
        기차 목록을 fetch하는 함수입니다.
        :param way: 기차 방향(string: upward, downward)
        :return:
        """
        try:
            return self.__train_data
        except KeyError:
            return {}
