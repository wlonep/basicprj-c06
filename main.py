from core.dummy import Dummy
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
        user = User("test")
        print(user.user_id)
