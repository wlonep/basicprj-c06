import re

from model import Station, Train, User


class BookTrain:
    def __init__(self, user_id: str):
        self.user = User(user_id)
        self.train_data = []
        self.depart = ""
        self.arrive = ""
        self.train = None
        if not self.train:
            self.__get_train_list()

    def __get_train_list(self):
        print("[열차 예매]")
        stations = Station().get_stations("gyeongbu")
        while True:
            self.depart = input("출발역: ")
            if self.depart[-1] != "역":
                self.depart += "역"
            if self.depart in stations:
                break
            else:
                print("\033[31m" + "* 일치하는 역이 존재하지 않습니다. 다시 입력해주세요." + "\033[0m")
        while True:
            while True:
                self.arrive = input("도착역: ")
                if self.arrive[-1] != "역":
                    self.arrive += "역"
                if self.arrive in stations:
                    break
                else:
                    print("\033[31m" + "* 일치하는 역이 존재하지 않습니다. 다시 입력해주세요." + "\033[0m")
            weight = stations[self.depart] - stations[self.arrive]
            if weight < 0:
                way = "downward"
                break
            elif weight > 0:
                way = "upward"
                break
            else:
                print("\033[31m" + "* 출발지와 도착지가 같습니다. 다시 입력해주세요." + "\033[0m")

        self.train = Train(way)
        self.train_data = self.train.get_train_data(self.depart, self.arrive)


    def reserve_ticket(self):
        while True:
            tn = input("선택하실 열차 번호를 입력해주세요: ")

            if re.fullmatch(r"[1-9][0-9]*", tn):
                pass
            else:
                print("\033[31m" + "*잘못된 입력 형식입니다. 다시 입력해 주세요." + "\033[0m")
                continue
            fl = False

            if int(tn) in list(self.user.user_data["booked_list"].keys()):
                print("\033[31m" + "* 이미 동일한 열차의 좌석을 예매하였습니다. 다시 입력해주세요." + "\033[0m")
                continue

            for t in self.train_data:
                if int(tn) == t["TRAIN_ID"]:
                    fl = True
            if fl:
                break
            else:
                print("\033[31m" + "*예매 가능한 열차가 아닙니다. 다시 입력해주세요." + "\033[0m")

        while True:
            seat = 1
            for t in self.train_data:
                if int(tn) == t["TRAIN_ID"]:
                    print("====================")
                    self.print_train(t)
                    print("====================")
                    seat += len(t["BOOKED"])

            choose = input("해당 열차로 예매를 진행하시겠습니까? ( 예 y / 아니오 n): ")
            if choose == 'y':
                self.train.book_seat(int(tn), seat)
                self.user.add_booking(int(tn), self.depart[:-1], self.arrive[:-1], seat)
                print("예매가 완료되었습니다. 메뉴로 돌아갑니다.")
                return
            elif choose == 'n':
                print("에매가 취소되었습니다. 메뉴로 돌아갑니다.")
                return
            else:
                print("\033[31m" + "*잘못된 입력 형식입니다. 다시 입력해 주세요." + "\033[0m")

    def print_train(self, t: dict):
        tid = t["TRAIN_ID"]

        fee = t["FEE"]
        base_fee = t["BASE_FEE"]

        all_st = len(t["STATION"])
        stop_st = 0
        stop_stations = []

        flag = False
        for ts in t["STATION"]:
            if ts == self.depart:
                flag = True
            if flag:
                stop_stations.append(ts)
                stop_st += 1
            if ts == self.arrive:
                break

        seat = self.train.book_limit - len(t["BOOKED"])
        total_fee = self.train.calc_fee(fee, base_fee, all_st, stop_st)

        print(tid, ' / ', total_fee, ' / ', seat)
        print("-".join([ts[:-1] for ts in stop_stations]))
        return

    def print_menu(self):
        print("====================")
        print("열차 번호 / 비용(원) / 남은 좌석(석)")
        print("정차역")
        print("====================")
        if len(self.train_data) == 0:
            print("\033[31m" + "* 해당 출발지에서 도착지로 가는 모든 열차의 좌석이 매진되었습니다. 메뉴로 돌아갑니다." + "\033[0m")
            return
        for t in self.train_data:
            self.print_train(t)
            print("-----------------------")
        self.reserve_ticket()
        return
