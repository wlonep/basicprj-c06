import os
import random


class Ticket:
    def __init__(self, ticket_id: str = None):
        self.__TICKET_FILES = "src/tickets"
        self.ticket_data = {}
        self.ticket_id = ticket_id
        self.ticket_ids = []
        self.__load_ticket_data()

    def __load_ticket_data(self):
        def parse_value(k, v):
            if k == "USER_ID":
                return v
            split_vals = v.split(",")
            parsed = []
            for sv in split_vals:
                try:
                    parsed.append(int(sv))
                except ValueError:
                    parsed.append(sv)
            return parsed

        if self.ticket_id is None:
            if not os.path.isdir(self.__TICKET_FILES):
                os.makedirs(self.__TICKET_FILES)
            for ticket_file in os.listdir(self.__TICKET_FILES):
                with open(f"{self.__TICKET_FILES}/{ticket_file}", 'r', encoding='UTF-8') as file:
                    lines = file.readlines()
                ticket_id = ticket_file.replace(".txt", "")
                self.ticket_ids.append(ticket_id)
                self.ticket_data[ticket_id] = {}
                for line in lines:
                    key, value = line.strip().split('=', 1)
                    self.ticket_data[ticket_id][key.lower()] = parse_value(key.upper(), value)
        else:
            ticket_file = f"{self.__TICKET_FILES}/{self.ticket_id}.txt"
            if not os.path.isfile(ticket_file):
                raise FileNotFoundError(f"{ticket_file} 파일을 찾을 수 없습니다.")
            with open(ticket_file, 'r', encoding='UTF-8') as file:
                lines = file.readlines()
            self.ticket_ids.append(self.ticket_id)
            self.ticket_data[self.ticket_id] = {}
            for line in lines:
                key, value = line.strip().split('=', 1)
                self.ticket_data[self.ticket_id][key.lower()] = parse_value(key.upper(), value)

    def create_ticket_id(self) -> str:
        if len(self.ticket_ids) >= 100000:
            raise OverflowError("티켓 아이디의 최대 개수에 도달했습니다.")
        while True:
            ticket_id = ''.join(random.choices('0123456789', k=5))
            if ticket_id not in self.ticket_ids:
                return ticket_id

    def get_ticket(self, t_id: str = None) -> dict:
        if self.ticket_id is None:
            return {t_id: self.ticket_data.get(t_id, {})}
        return {self.ticket_id: self.ticket_data.get(self.ticket_id, {})}

    def get_ticket_by_user(self, user_id: str) -> dict:
        if self.ticket_id is None:
            return {t_id: data for t_id, data in self.ticket_data.items() if data.get("user_id") == user_id}
        raise TypeError("특정 티켓 ID가 고정된 상태로 이 메소드를 호출할 수 없습니다.")

    def book_ticket(self, user_id: str, t_id: str, data: dict) -> bool:
        if t_id in self.ticket_ids:
            return False
        if "stations" not in data or "train_ids" not in data or "booked_seats" not in data:
            return False
        self.ticket_ids.append(t_id)
        self.ticket_data[t_id] = {
            "user_id": user_id,
            "stations": data["stations"],
            "train_ids": data["train_ids"],
            "booked_seats": data["booked_seats"]
        }
        print(self.ticket_data[t_id])
        with open(f"{self.__TICKET_FILES}/{t_id}.txt", 'w', encoding='UTF-8') as file:
            for key, value in self.ticket_data[t_id].items():
                file.write(f"{key.upper()}={','.join(str(v) for v in value) if isinstance(value, list) else value}\n")
        return True

    def cancel_ticket(self, t_id: str) -> bool:
        if t_id not in self.ticket_ids:
            return False
        del self.ticket_data[t_id]
        self.ticket_ids.remove(t_id)
        os.remove(f"{self.__TICKET_FILES}/{t_id}.txt")
        return True
