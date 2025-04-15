from core.booktrain import BookTrain
from core.dummy import Dummy
from model.User import User
import re

"""
임의로 구현한 초기 화면입니다. 실제 초기 화면은 while문을 사용하여
사용자가 종료하기 전까지 무한으로 반복되고, 로그인 된 상태인 경우
초기화면이 아닌 사용자 메뉴 화면에서 무한 루프되므로 해당 부분 처리가 필요합니다.
"""
if __name__ == '__main__':
    """
    print("[KTX 예매 프로그램]")
    print("1. 로그인")
    print("2. 회원가입")
    print("3. 종료")
    sel = input("원하는 메뉴를 입력해 주세요: ")

    # 각 클래스 호출 예시입니다. 실제 구동 시에는 삭제해 주세요.
    if sel == "2":
        user = User("test")
        print(user.user_id)
    """

    i = BookTrain()
    i.print_menu()
    user = User()

    while True:
        print("[KTX 예매 프로그램]")
        print("1. 로그인")
        print("2. 회원가입")
        print("3. 종료")
        sel = input("원하는 메뉴를 입력해 주세요: ")

        # 로그인
        if sel == "1" or "로그인":
            while True:
                print("[로그인]")
                uid = input("아이디: ")

                if user.is_user_exist(uid):     # 아이디 확인
                    pw = input("비밀번호: ")

                    if user.login(uid, pw):     # 비밀번호 확인 절차 포함
                        print(f"*{uid}님 환영합니다.")
                        break
                    else:
                        print("*비밀번호가 일치하지 않습니다. 다시 입력해주세요.")
                else:
                    print("*존재하지 않는 아이디입니다. 다시 입력해주세요.")

        elif sel == "2" or "회원가입":
            print("[회원가입]")
            print("※아이디는 알파벳 소문자와 숫자의 조합으로, 각각 최소 하나 이상 포함하여 4자 이상 12자 이하로 구성해야 합니다.")

            # 아이디 입력 루프
            # 아이디 입력 및 검증
            while True:
                uid = input("아이디: ")

                if not user.is_valid_username(uid):
                    print("*잘못된 입력 형식입니다. 다시 입력해주세요.")
                    continue
                if user.is_user_exist(uid):
                    print("*이미 존재하는 아이디입니다. 다시 입력해주세요.")
                    continue
                    
                # 비밀번호 입력 루프
                # 비밀번호 입력 및 검증
                print("※비밀번호는 알파벳 대문자와 소문자, 숫자, 특수문자의 조합으로, 각각 최소 하나 이상 포함하여 8자 이상 16자 이하로 구성해야 합니다.")
                while True:
                    pw = input("비밀번호: ")

                    if not user.is_valid_password(pw):
                        print("*잘못된 입력 형식입니다. 다시 입력해주세요.")
                        continue

                    # 회원가입 처리 완료

                    user.register(uid, pw)
                    print("*회원가입이 완료되었습니다. 시작화면으로 돌아갑니다.")
                    break # 비밀번호 루프 탈출
                break # 아이디 루프 탈출

        elif sel == "3" or "종료":
            print("[프로그램 종료]")
            print("이용해주셔서 감사합니다.")
            break

        else:
            print("*잘못된 입력입니다. 올바른 메뉴의 숫자 또는 단어를 입력하세요.")


    # 각 클래스 호출 예시입니다. 실제 구동 시에는 삭제해 주세요.
    # if sel == "2":
    #     user = User("test")
    #     print(user.user_id)

