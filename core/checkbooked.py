import re
from model import User, Train


class CheckBooked:
    def __init__(self, user_id: str):
        self.user = User(user_id)

    def __get_info(self) -> dict:  # 사용자의 모든 예약된 열차 데이터 반환
        user_data = self.user.user_data["booked_list"]
        train_ids = [tid for tid in user_data.keys()]
        train_ids.sort()
        train = Train(train_ids=train_ids)
        booked_list = train.get_trains()  # 예약된 기차 정보
        return {
            "train_ids": train_ids,
            "user_data": user_data,
            "train": train,
            "booked_list": booked_list
        }

    @staticmethod
    def print_booked_info(info: dict, t_info: dict):
        tid = t_info["TRAIN_ID"]

        fee = t_info["FEE"]
        base_fee = t_info["BASE_FEE"]

        depart = info["user_data"][tid]["depart"]
        arrive = info["user_data"][tid]["arrive"]

        all_st = len(t_info["STATION"])
        stop_st = 0
        stop_stations = []

        flag = False
        for st in t_info["STATION"]:
            if st[:-1] == depart:
                flag = True
            if flag:
                stop_stations.append(st)
                stop_st += 1
            if st[:-1] == arrive:
                break
        remain = info["train"].book_limit - len(t_info["BOOKED"])
        final_fee = Train.calc_fee(fee, base_fee, all_st, stop_st)

        print(tid, '/', final_fee, '/', remain)
        print("-".join([ts[:-1] for ts in stop_stations]))

    def print_booked_lists(self) -> bool:
        try:
            info = self.__get_info()
        except NotADirectoryError:
            print("\033[31m" + "*예매된 기차가 없습니다." + "\033[0m")
            return False
        print("열차 번호 / 비용(원) / 예매 좌석(석)")
        print("정차역")
        print("==============================")
        for t_info in info["booked_list"]:
            self.print_booked_info(info, t_info)
            print("------------------------------")
        return True

    def cancel_booked(self):
        print("[예매 취소]")
        self.print_booked_lists()
        info = self.__get_info()

        while True:
            cancel = input("예매 취소를 원하는 열차 번호를 입력해 주세요: ")

            if re.fullmatch(r"[1-9]\d*", cancel):
                if int(cancel) not in info["train_ids"]:
                    print("\033[31m" + "*일치하는 예매 정보가 없습니다. 다시 입력해주세요." + "\033[0m")
                    continue
                else:
                    break
            else:
                print("\033[31m" + "*잘못된 입력 형식입니다. 다시 입력해주세요." + "\033[0m")

        t_info = {}
        for t in info["booked_list"]:
            if t["TRAIN_ID"] == int(cancel):
                t_info = t
                break

        print("==============================")
        self.print_booked_info(info, t_info)
        print("==============================")
        while True:
            yn = input("해당 열차 예매 취소를 진행하시겠습니까? ( 예 y / 아니오 n ): ")
            if yn == "y":
                self.user.cancel_booked(int(cancel))
                print("취소가 완료되었습니다. 메뉴로 돌아갑니다.")
                break
            elif yn == "n":
                print("취소가 중단되었습니다. 메뉴로 돌아갑니다.")
                break
            else:
                print("\033[31m" + "*잘못된 입력 형식입니다. 다시 입력해주세요." + "\033[0m")

    def menu(self):
        while True:
            print("[예매 정보 확인]")
            if self.print_booked_lists() is False:
                return
            print("1. 예매취소")
            print("2. 뒤로가기")
            sel = input("원하는 메뉴를 입력해 주세요: ")

            if sel == "1" or sel == "예매취소":
                self.cancel_booked()
                break
            if sel == "2" or sel == "뒤로가기":
                break
            else:
                print("\033[31m" + "* 잘못된 입력입니다. 올바른 메뉴의 숫자 또는 단어를 입력하세요." + "\033[0m")
