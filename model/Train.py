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

    @staticmethod
    def calc_fee(fee: int, base_fee: int, all_st: int, stop_st: int) -> int:
        return int(round(base_fee + (fee - base_fee) * (stop_st / all_st), -2))

    def __load_train_data(self, directory: str):
        """
        기차 데이터 로드 함수입니다.
        클래스 선언 시 init 함수에서 함께 실행됩니다.
        __train_data 배열에 상행/하행에 대한 기차 정보를 저장합니다.
        :param directory: 기차 데이터를 가져올 폴더(upward/downward 구분 위함)
        :return:
        """
        try:
            if not os.path.isdir(directory):
                raise FileNotFoundError("train files are missing.")

            data = {}
            for sf in os.listdir(directory):
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

            if not os.path.isdir(directory):
                raise FileNotFoundError("train files are missing.")
            data = {}
            for sf in os.listdir(directory):
                with open(f"{directory}/{sf}", 'r', encoding='UTF-8') as file:
                    lines = file.readlines()
                tid = int(lines[0].strip().split('=')[1])
                data[tid] = self.__add_data(lines)

            # noinspection PyTypeChecker
            self.train_data = dict(sorted(data.items()))
        except FileNotFoundError as e:
            print("\033[31m"+"해당 폴더가 존재하지 않습니다."+"\033[0m")

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

    def book_seat(self, train_id: int, seat_num: int) -> bool:
        """
        기차 파일에 예약된 좌석을 저장하는 함수입니다.
        :param train_id: 기차 아이디(int)
        :param seat_num: 예약할 좌석 번호(int)
        :return:
        """
        if seat_num < 1 or seat_num > self.book_limit:
            raise ValueError("Invalid seat number.")
        if str(seat_num) in self.train_data[train_id]["BOOKED"]:
            return False
        self.train_data[train_id]["BOOKED"].append(seat_num)
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
            file.write(f"TRAIN_ID={train_id}\n")
            for key, value in train.items():
                if isinstance(value, list):
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
