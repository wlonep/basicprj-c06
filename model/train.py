import os


class Train:
    def __init__(self, way: str = None, train_ids: list = None):
        self.way = way
        self.train_data = {}
        self.train_ids = train_ids
        if not self.train_ids:
            self.__load_train_data(f"src/train/{self.way}")
        self.book_limit = 20  # 예약 가능한 좌석 수

    @staticmethod
    def __add_data(lines: list) -> dict:
        data = {}
        for line in lines:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                if key == "BOOKED":
                    if value == "":
                        data[key] = []
                    else:
                        data[key] = value.split(",")
                elif key == "STATION":
                    data[key] = [s + "역" for s in value.split(",")]
                else:
                    try:
                        data[key] = int(value)
                    except ValueError:
                        data[key] = value.split(",")
        return data

    def __load_train_data(self, directory: str):
        """
        기차 데이터 로드 함수입니다.
        클래스 선언 시 init 함수에서 함께 실행됩니다.
        __train_data 배열에 상행/하행에 대한 기차 정보를 저장합니다.
        :param directory: 기차 데이터를 가져올 폴더(upward/downward 구분 위함)
        :return:
        """
        # directory가 없을 경우
        if not os.path.isdir(directory):
            raise NotADirectoryError("*파일을 불러오는 데 문제가 발생하였습니다.")

        # 파일이 없을 경우
        try:
            file_list = os.listdir(directory)
            if not file_list:
                raise FileNotFoundError("목록 내 열차가 존재하지 않습니다.")
        except FileNotFoundError:
            raise FileNotFoundError("목록 내 열차가 존재하지 않습니다.")

        data = {}
        for sf in file_list:
            with open(f"{directory}/{sf}", 'r', encoding='UTF-8') as file:
                lines = file.readlines()
            tid = int(lines[0].strip().split('=')[1])
            data[tid] = {}
            for line in lines:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    if key == "BOOKED":
                        if value == "":
                            data[tid][key] = []
                        else:
                            data[tid][key] = value.split(",")
                    elif key == "STATION":
                        data[tid][key] = [s + "역" for s in value.split(",")]
                    else:
                        try:
                            data[tid][key] = int(value)
                        except ValueError:
                            data[tid][key] = value.split(",")
        # noinspection PyTypeChecker
        self.train_data = dict(sorted(data.items()))

        data = {}
        for sf in os.listdir(directory):
            with open(f"{directory}/{sf}", 'r', encoding='UTF-8') as file:
                lines = file.readlines()
            tid = int(lines[0].strip().split('=')[1])
            data[tid] = self.__add_data(lines)

        # noinspection PyTypeChecker
        self.train_data = dict(sorted(data.items()))

    def get_train_data(self, depart: str, arrive: str) -> list:
        """
        출발지, 도착지까지의 경로가 존재하는 예매 가능한
        모든 기차 목록을 출력하는 함수입니다.
        :param depart: 출발지(string)
        :param arrive: 도착지(string)
        :return:
        """
        train_list = []
        for train in self.train_data:
            td = self.train_data[train]
            if depart in td["STATION"] and arrive in td["STATION"] \
                    and len(td["BOOKED"]) < self.book_limit:
                train_list.append(td)
        return train_list

    def book_seat(self, train_id: int, seat_id: int) -> bool:
        """
        기차 파일에 예약된 좌석을 저장하는 함수입니다.
        :param train_id: 기차 아이디(int)
        :param seat_id: 예약할 좌석 번호(int)
        :return:
        """
        if int(seat_id) < 1 or int(seat_id) > self.book_limit:
            raise ValueError("Invalid seat number.")
        if str(seat_id) in self.train_data[train_id]["BOOKED"]:
            return False
        self.train_data[train_id]["BOOKED"].append(str(seat_id))
        return self.update_data(train_id)

    def unbook_seat(self, train_id: int, seat_id: int) -> bool:
        if seat_id < 1 or seat_id > self.book_limit:
            raise ValueError("Invalid seat number.")
        if str(seat_id) not in self.train_data[train_id]["BOOKED"]:
            return False
        self.train_data[train_id]["BOOKED"].remove(str(seat_id))
        return self.update_data(train_id)

    def update_data(self, train_id: int) -> bool:
        """
        기차 데이터 파일을 업데이트하는 함수입니다.
        :param train_id: 기차 아이디(int)
        :return:
        """
        train = self.train_data[train_id]
        file_path = f"src/train/{self.way}/KTX-{train_id}.txt"
        with open(file_path, 'w', encoding='UTF-8') as file:
            # file.write(f"TRAIN_ID={train_id}\n")
            for key, value in train.items():
                if isinstance(value, list):
                    if key == "STATION":
                        value = [s[:-1] for s in value]
                    value = ','.join(map(str, value))
                file.write(f"{key}={value}\n")
        return True

    def get_trains(self) -> list:
        result = []
        for train in self.train_ids:
            if train % 2 == 0:
                for sf in os.listdir(f"src/train/upward"):
                    if sf == f"KTX-{train}.txt":
                        with open(f"src/train/upward/{sf}", 'r', encoding='UTF-8') as file:
                            lines = file.readlines()
                        result.append(self.__add_data(lines))
            else:
                for sf in os.listdir(f"src/train/downward"):
                    if sf == f"KTX-{train}.txt":
                        with open(f"src/train/downward/{sf}", 'r', encoding='UTF-8') as file:
                            lines = file.readlines()
                        result.append(self.__add_data(lines))
        return result
