import re
from model import User, Train, Ticket


class CheckBooked:
    def __init__(self, user_id: str):
        self.user = User(user_id)

    def __get_info(self) -> dict:  # 사용자의 모든 예약된 열차 데이터 반환
        return self.user.user_data["booked_list"]

    def print_booked_lists(self) -> bool:
        try:
            tickets = self.__get_info()
        except NotADirectoryError:
            print("\033[31m" + "*예매된 기차가 없습니다." + "\033[0m")
            return False
        print("─────────────────")
        for t_num in tickets:
            """
            Ticket.print_booked_info(t_num)
            """
            print("출력함수 미완성!")
            print("─────────────────")
        return True

    def cancel_booked(self):
        print("[예매 취소]")
        self.print_booked_lists()
        tickets = self.__get_info()

        while True:
            cancel = input("예매 취소를 원하는 티켓 번호를 입력해 주세요: ")

            if re.fullmatch(r"\d{5}", cancel):
                if cancel not in tickets:
                    print("\033[31m" + "*일치하는 예매 정보가 없습니다. 다시 입력해주세요." + "\033[0m")
                    continue
                else:
                    break
            else:
                print("\033[31m" + "*잘못된 입력 형식입니다. 다시 입력해주세요." + "\033[0m")

        ticket = Ticket(cancel)
        t_data = ticket.ticket_data[cancel]
        t_ids = t_data["train_ids"]
        seats = t_data["booked_seats"]

        print("─────────────────")
        """
        Ticket.print_booked_info(cancel)
        """
        print("출력함수 미완성!")
        print("─────────────────")
        while True:
            yn = input("해당 열차 예매 취소를 진행하시겠습니까? ( 예 y / 아니오 n ): ")
            if yn == "y":
                ticket.cancel_ticket(cancel)

                for i in range(len(t_ids)):
                    if t_ids[i] % 2 == 1:
                        t = Train("downward")
                    else:
                        t = Train("upward")
                    t.unbook_seat(int(t_ids[i]), int(seats[i]))

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
