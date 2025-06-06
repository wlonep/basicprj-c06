from.check_booked import CheckBooked
from.book_train import BookTrain
from.admin import Admin


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
