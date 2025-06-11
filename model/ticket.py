import os
import random
from model.train import Train
from model.user import User


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
        if (self.ticket_id is None and t_id not in self.ticket_ids) or \
                (self.ticket_id is not None and self.ticket_id not in self.ticket_ids):
            raise ValueError("존재하지 않는 티켓 ID입니다.")
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
        with open(f"{self.__TICKET_FILES}/{t_id}.txt", 'w', encoding='UTF-8') as file:
            for key, value in self.ticket_data[t_id].items():
                file.write(f"{key.upper()}={','.join(str(v) for v in value) if isinstance(value, list) else value}\n")

        User(user_id).add_ticket(t_id)
        index = 0
        train_up = Train("upward")
        train_down = Train("downward")
        for train_id in data["train_ids"]:
            if train_id % 2 == 0:
                train_up.book_seat(train_id, data["booked_seats"][index])
            else:
                train_down.book_seat(train_id, data["booked_seats"][index])
            index += 1
        return True

    def cancel_ticket(self, t_id: str) -> bool:
        if t_id not in self.ticket_ids:
            return False

        data = self.ticket_data[t_id]
        user_id = data["user_id"]
        User(user_id).remove_ticket(t_id)

        train_up = Train("upward")
        train_down = Train("downward")

        index = 0
        for train_id in data["train_ids"]:
            seat_id = data["booked_seats"][index]
            if train_id % 2 == 0:
                train_up.unbook_seat(train_id, seat_id)
            else:
                train_down.unbook_seat(train_id, seat_id)
            index += 1

        self.ticket_ids.remove(t_id)
        os.remove(f"{self.__TICKET_FILES}/{t_id}.txt")
        del self.ticket_data[t_id]
        return True

    @staticmethod
    def calc_fee(data: dict) -> int:

        stations = data["stations"]
        train_ids = data["train_ids"]
        base_fees = []
        fees = []
        all_sts = []
        stop_sts = []

        for i, tid in enumerate(train_ids):
            t_data1 = Train("downward").train_data
            t_data2 = Train("upward").train_data
            t_data = {**t_data1, **t_data2}[tid]
            base_fees.append(t_data["BASE_FEE"])
            fees.append(t_data["FEE"])
            all_sts.append(len(t_data["STATION"]))
            station_list = t_data["STATION"]
            start_station = stations[i]
            end_station = stations[i + 1]

            counting = False
            count = 0
            for st in station_list:
                if not counting:
                    if st[:-1] == start_station:
                        counting = True
                        count += 1
                else:
                    count += 1
                    if st[:-1] == end_station:
                        break
            stop_sts.append(count)

        base_fee_avg = sum(base_fees) / len(base_fees)
        extra_fee = sum(
            (fees[i] - base_fees[i]) * stop_sts[i] / all_sts[i]
            for i in range(len(train_ids))
        )

        total_fee = base_fee_avg + extra_fee
        return int(round(total_fee, -2))

    @staticmethod
    def print_booked_info(t_num: str):
        """출력하는 함수 구현해주세요!"""
