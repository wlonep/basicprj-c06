import re
from msilib import add_data

from generator.train import calculate_fee
from model import Station, Train, User

class BookTrain:
    def __init__(self, train = None):
        self.user = User("test")
        self.train_data = []
        self.depart = ""
        self.arrive = ""
        self.train = train
        if not self.train:
            self.__get_train_list()


    def __get_train_list(self):
        print("[열차 예매]")
        stations = Station().get_stations("gyeongbu")
        while True:
            self.depart = input("출발역: ")
            if(self.depart[-1] != "역"):
                self.depart += "역"
            if self.depart in stations:
                break
            else:
                print("\033[31m"+"*잘못된 입력 형식입니다. 다시 입력해주세요."+"\033[0m")
        while True:
            while True:
                self.arrive = input("도착역: ")
                if (self.arrive[-1] != "역"):
                    self.arrive += "역"
                if self.arrive in stations:
                    break
                else:
                    print("\033[31m"+"*잘못된 입력 형식입니다. 다시 입력해주세요."+"\033[0m")

            weight = stations[self.depart] - stations[self.arrive]
            if weight > 0:
                self.train = Train("upward")
                break
            elif weight < 0:
                self.train = Train("downward")
                break
            else:
                print("출발역과 도착역이 같습니다.")

    def reserve_ticket(self):
        while True:
            tn = input("선택하실 열차 번호를 입력해주세요:")

            if re.fullmatch(r"[1-9]*\n", tn):
                if int(tn) in self.train_data[0]["TRAIN_ID"]:
                    if self.train_data[-1]["BOOKED"] < self.train.book_limit:
                        break
                    else:
                        print("\033[31m" + "*열차에 남은 좌석이 없습니다. 다시 입력해 주세요." + "\033[0m")
                        continue
                else:
                    print("\033[31m" + "*예매 가능한 열차가 아닙니다. 다시 입력해 주세요." + "\033[0m")
                    continue
            else:
                print("\033[31m" + "*잘못된 입력 형식입니다. 다시 입력해 주세요." + "\033[0m")

        seat = self.train.book_limit
        for t in self.train_data:
            if t["TRAIN_ID"] == tn:
                print("====================")
                self.print_train(t)
                print("====================")
                seat -= len(t["BOOKED"])


        choose = input("해당 열차로 예매를 진행하시겠습니까? ( 예 y / 아니오 n):")
        if(choose == 'y'):
            self.train.book_seat(tn, seat)
            self.user.add_booking(tn, self.depart, self.arrive)
            print("예매가 완료되었습니다. 메뉴로 돌아갑니다.")
        elif(choose == 'n'):
            print("에매가 취소되었습니다. 메뉴로 돌아갑니다.")
        else:
            print("\033[31m" + "*잘못된 입력 형식입니다. 다시 입력해 주세요." + "\033[0m")

    def print_train(self, t: dict):
        tid = t["TRAIN_ID"]

        fee = t["FEE"]
        base_fee = t["BASE_FEE"]

        all_st = len(t["STATION"])
        stop_st = 0


        flag = False
        for ts in t["STATION"]:
            if ts[:-1] == self.depart:
                flag = True
            if flag:
                stop_st += 1
            if ts[:-1] == self.arrive:
                break

        seat = self.train.book_limit - len(t["BOOKED"])
        total_fee = calculate_fee(fee, base_fee, all_st, stop_st)

        print(tid,' / ',total_fee,' / ',seat)

        flag = False
        for ts in t["STATION"]:
            if ts[:-1] == self.depart:
                flag = True
            if flag:
                stop_st += 1
            if ts[:-1] == self.arrive:
                break
            print(ts[:-1],'-',end="")

    def print_menu(self):
        self.train_data = self.train.get_train_data(self.depart, self.arrive)
        print("====================")
        print("열차 번호 / 비용(원) / 남은 좌석(석)")
        print("정차역")
        print("====================")
        for t in self.train_data:
            self.print_train(t)
            print("-----------------------")
        self.reserve_ticket()
