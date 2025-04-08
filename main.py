from model.Train import Train
from model.Station import Station
from model.User import User

"""
임의로 구현한 초기 화면입니다. 실제 초기 화면은 while문을 사용하여
사용자가 종료하기 전까지 무한으로 반복되고, 로그인 된 상태인 경우
초기화면이 아닌 사용자 메뉴 화면에서 무한 루프되므로 해당 부분 처리가 필요합니다.
"""
if __name__ == '__main__':
    print("[KTX 예매 프로그램]")
    print("1. 로그인")
    print("2. 회원가입")
    print("3. 종료")
    sel = input("원하는 메뉴를 입력해 주세요: ")

    # 각 클래스 호출 예시입니다. 실제 구동 시에는 삭제해 주세요.
    if sel == "2":
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
