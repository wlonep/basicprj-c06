from model.user import User
from model.ticket import Ticket

from .check_booked import CheckBooked
from .book_train import BookTrain
from .admin import Admin


def admin_menu():
    admin = Admin()

    while True:
        print("[관리자 메뉴]")
        print("1. 목록조회")
        print("2. 편성추가")
        print("3. 로그아웃")
        sel = input("원하는 메뉴를 입력하세요: ")

        if sel == "1" or sel == "목록조회":
            admin.get_train_list()
        elif sel == "2" or sel == "편성추가":
            admin.create_train_file()
        elif sel == "3" or sel == "로그아웃":
            print("로그아웃합니다. 이용해주셔서 감사합니다.")
            return
        else:
            print("\033[31m" + "* 잘못된 입력입니다. 올바른 메뉴의 숫자 또는 단어를 입력하세요." + "\033[0m")


def user_menu(user_id: str):
    while True:
        print("[사용자 메뉴]")
        print("1. 열차예매")
        print("2. 예매정보")
        print("3. 로그아웃")
        sel = input("원하는 메뉴를 입력하세요: ")

        if sel == "1" or sel == "열차예매":
            book = BookTrain(user_id)
            book.print_menu()
        elif sel == "2" or sel == "예매정보":
            CheckBooked(user_id).menu()
        elif sel == "3" or sel == "로그아웃":
            print("로그아웃합니다. 이용해주셔서 감사합니다.")
            return
        else:
            print("\033[31m" + "* 잘못된 입력입니다. 올바른 메뉴의 숫자 또는 단어를 입력하세요." + "\033[0m")


def main_menu():
    user = User()
    while True:
        print("[KTX 예매 프로그램]")
        print("1. 로그인")
        print("2. 회원가입")
        print("3. 비회원 조회")
        print("4. 종료")
        sel = input("원하는 메뉴를 입력해 주세요: ")

        # 로그인
        if sel in ["1", "로그인"]:
            while True:
                print("[로그인]")
                uid = input("아이디: ")

                if uid == "admin":
                    pw = input("비밀번호: ")
                    if pw == "1234":
                        print("관리자모드로 로그인합니다")
                        admin_menu()
                        break
                    else:
                        print("\033[31m" + "*로그인 정보가 틀렸습니다. 처음부터 다시 입력하세요." + "\033[0m")
                        continue

                if user.is_user_exist(uid):  # 아이디 확인
                    pw = input("비밀번호: ")

                    if user.login(uid, pw):  # 비밀번호 확인 절차 포함
                        print(f"*{uid}님 환영합니다.")
                        user_menu(uid)
                        break
                    else:
                        print("\033[31m" + "*로그인 정보가 틀렸습니다. 처음부터 다시 입력하세요." + "\033[0m")
                else:
                    print("\033[31m" + "*로그인 정보가 틀렸습니다. 처음부터 다시 입력하세요." + "\033[0m")

        elif sel in ["2", "회원가입"]:
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
                    break  # 비밀번호 루프 탈출
                break  # 아이디 루프 탈출

        elif sel in ["3", "비회원조회", "비회원 조회"]:

            print("[비회원 조회]")
            while True:
                t_id = input("티켓 번호를 입력하세요: ")
                if check_by_ticket(t_id):
                    break  # 조회 성공했을 때만 종료

        elif sel in ["4", "종료"]:
            print("[프로그램 종료]")
            print("이용해주셔서 감사합니다.")
            break

        else:
            print("*잘못된 입력입니다. 올바른 메뉴의 숫자 또는 단어를 입력하세요.")


def check_by_ticket(t_id: str):
    try:
        Ticket(t_id).print_booked_info(t_id)
        return True
    except FileNotFoundError:
        print("\033[31m*티켓 번호가 존재하지 않습니다. 다시 입력해주세요.\033[0m")
        return False
