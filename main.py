import sys

from core.menu import main_menu
from model import Ticket
from model.train import Train
from model.user import User
from model.station import Station

if __name__ == '__main__':
    try:
        users = User()
        Station()
        Train("downward")
        Train("upward")
    except Exception as e:
        print("\033[31m" + f"파일을 불러오는 데 문제가 발생하였습니다.\n{e}" + "\033[0m")
        sys.exit()

    ticket = Ticket()
    for t in ticket.ticket_data:
        try:
            User(ticket.ticket_data[t]["user_id"])
        except FileNotFoundError:
            print("\033[31m" + "파일을 불러오는 데 문제가 발생하였습니다."
                               "\n데이터 파일 사이에 충돌이 일어났습니다." + "\033[0m")
            sys.exit()

    for uid in users.user_ids:
        booked = User(uid).user_data["booked_list"]
        tickets = ticket.get_ticket_by_user(uid)
        if len(booked) != len(tickets):
            print("\033[31m" + "파일을 불러오는 데 문제가 발생하였습니다."
                               "\n데이터 파일 사이에 충돌이 일어났습니다." + "\033[0m")
            sys.exit()

    main_menu()