from model import Train

class Admin:
    def __init__(self):
        """
        관리자 클래스입니다.
        Train 모델을 사용하여 관리자 기능을 구현하기 위해
        작성한 클래스입니다.
        """

    @staticmethod
    def get_train_list():
        print("[열차 목록 조회]")
        train = Train("downward")
        for tid, info in train.train_data.items():
            for key, value in  info.items():
                if key == "STATION":
                    value = ",".join([s.replace("역", "") for s in value])
                if key == "BOOKED":
                    if value == []:
                        value = ""
                print(f"{key}={value}")
            print("-----------------------------------------------\n\n\n")
        train2 = Train("upward")
        for tid, info in train2.train_data.items():
            for key, value in info.items():
                if key == "STATION":
                    value = ",".join([s.replace("역", "") for s in value])
                if key == "BOOKED":
                    if value == []:
                        value = ""
                print(f"{key}={value}")
            print("-----------------------------------------------\n\n\n")
        train3 = Train("전기프")
        for tid, info in train3.train_data.items():
            for key, value in info.items():
                if key == "STATION":
                    value = ",".join([s.replace("역", "") for s in value])
                if key == "BOOKED":
                    if value == []:
                        value = ""
                print(f"{key}={value}")
            print("-----------------------------------------------\n\n\n")
