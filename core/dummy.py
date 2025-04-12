from model import User, Station, Train


class Dummy:
    def __init__(self):
        """
        더미 클래스입니다.
        실제 구현 시 이 파일은 삭제될 예정입니다.
        User, Train, Station 모델을 어떻게 사용하는지 예시를 보여주기 위해
        작성한 클래스입니다.
        """

    @staticmethod
    def test():
        user = User()
        is_exist = user.is_user_exist("test")
        if not is_exist:
            register = user.register("test", "1234")
            if register:
                print("회원가입 성공")
        else:
            print("회원가입 실패(이미 존재하는 계정)")

        stations = Station().get_stations("gyeongbu")   # 경부선 역 목록 받아오기
        depart_station = "서울역"
        arrive_station = "부산역"
        weight = stations[depart_station] - stations[arrive_station]

        if weight < 0:
            train = Train("downward")
            train_data = train.get_train_data(depart_station, arrive_station)
            for td in train_data:
                print(td["TRAIN_ID"])
        elif weight > 0:
            train = Train("upward")
        else:
            print("출발역과 도착역이 같습니다.")