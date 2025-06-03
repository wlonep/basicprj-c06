from model import Ticket

ticket = Ticket()
# num = ticket.create_ticket_id()
# ticket.book_ticket("test1", num, {"stations": ["광명", "경주", "태화강"], "train_ids": [2, 4, 8], "booked_seats": [20, 15, 10]})
# t = ticket.get_ticket_by_user("test1")
# t = ticket.get_ticket("21212")
ticket.cancel_ticket("11212")

