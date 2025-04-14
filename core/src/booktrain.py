import re
from model import Station, Train, User

class BookTrain:
    def __init__(self):
        self.user = User("test")

    def deter_updown(self) -> str:
        stations = Station().get_stations("gyeongbu")
        while True:
            self.depart = input("출발역: ")
            if(self.depart[-1] != "역"):
                self.depart += "역"
            if self.depart in stations:
                break
            else:
                print("잘못된 입력 형식입니다. 다시 입력해주세요.")
        while True:
            self.arrive = input("도착역: ")
            if (self.arrive[-1] != "역"):
                self.arrive += "역"
            if self.arrive in stations:
                break
            else:
                print("잘못된 입력 형식입니다. 다시 입력해주세요.")
        weight = stations[self.depart] - stations[self.arrive]
        if weight > 0:
            return "upward"
        elif weight < 0:
            return "downward"
        else:
            print("출발역과 도착역이 같습니다.")
            return ""

    def get_info(self, way: str):
        train = Train(way)
        train_data = train.get_train_data(self.depart, self.arrive)
        for tr in train_data:
            tn = tr["TRAIN_ID"]
            fee = tr["FEE"]
            base_fee = tr["BASE_FEE"]

            all_st = len(tr["STATION"])
            stop_st = 0

            flag = False
            tr["STATION"].reverse()
            for st in tr["STATION"]:
                if st == self.depart:
                    flag = True
                if flag:
                    stop_st += 1
                if st == self.arrive:
                    break

            remain = train.book_limit - len(tr["BOOKED"])
            f_fee = train.calc_fee(fee, base_fee, all_st, stop_st)

            print(tn, '/', f_fee, '/', remain)

            flag = False
            for st in tr["STATION"]:
                if st == self.depart:
                    flag = True
                if st == self.arrive:
                    if (st[-1] == "역"):
                        st = st[:-1]
                    print(st)
                    break
                if flag:
                    if(st[-1] == "역"):
                        st = st[:-1]
                    print(st + "-", end='')

            print("-----------------------")



def print_train(self):
        way = self.deter_updown()
        print("====================")
        print("열차 번호 / 비용(원) / 남은 좌석(석)")
        print("정차역")
        print("====================")
        self.get_info(way)

"""
    def reserve_ticket(self):
        tn = input("선택하실 열차 번호를 입력해주세요:")

        if(re.fullmatch(r"[1-9]*\n"),tn):
"""