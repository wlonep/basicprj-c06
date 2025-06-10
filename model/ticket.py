import os
import random
from model.train import Train

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
        return True

    def cancel_ticket(self, t_id: str) -> bool:
        if t_id not in self.ticket_ids:
            return False
        del self.ticket_data[t_id]
        self.ticket_ids.remove(t_id)
        os.remove(f"{self.__TICKET_FILES}/{t_id}.txt")
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
        return int(round(total_fee , -2))

    @staticmethod
    def print_booked_info(t_num):
        # 1. 티켓 정보 불러오기
        data = Ticket.get_ticket(t_num)

        # 2. 필요한 데이터 꺼내기
        train_ids = data["train_ids"]          # 탑승 열차 번호 리스트
        stations = data["stations"]            # 거치는 역 리스트
        seats = data["booked_seats"]           # 좌석 번호 리스트

        # 3. 운임 계산
        fee = Ticket.calc_fee(data)

        # 4. 각 열차의 정차 시간 불러오기
        times = []
        for idx, train_id in enumerate(train_ids):
            file_loaded = False
            # 상행/하행 구분해서 둘 다 시도
            for direction in ["upward", "downward"]:
                train_file_path = f"src/train/{direction}/KTX-{train_id}.txt"
                try:
                    with open(train_file_path, encoding="utf-8") as f:
                        lines = f.readlines()
                    # 역 리스트와 시간 리스트 읽기
                    station_list = None
                    stop_times = None
                    for line in lines:
                        if line.startswith("STATION="):
                            station_list = line.strip().split("=")[1].split(",")
                        if line.startswith("STOP_TIME="):
                            stop_times = line.strip().split("=")[1].split(",")
                    # 현재 열차 구간에 해당하는 역들의 시간만 추가
                    if station_list is None or stop_times is None:
                        print("열차 데이터 파일이 잘못되었습니다.")
                        return
                    user_stations = [stations[idx], stations[idx+1]]
                    for us in user_stations:
                        idx_in_file = station_list.index(us)
                        times.append(stop_times[idx_in_file])
                    file_loaded = True
                    break
                except FileNotFoundError:
                    continue
            if not file_loaded:
                print(f"KTX-{train_id} 데이터 파일을 찾을 수 없습니다.")
                return

        # 5. 소요시간 계산 (여기선 그냥 단순히 첫 출발~마지막 도착 차이)
        def hhmm_to_min(hhmm):
            h, m = int(hhmm[:2]), int(hhmm[2:])
            return h * 60 + m
        start_min = hhmm_to_min(times[0])
        end_min = hhmm_to_min(times[-1])
        dur_h = (end_min - start_min) // 60
        dur_m = (end_min - start_min) % 60

        # 6. 출력
        print("─────────────────")
        # 열차번호 출력
        print(f"[KTX-{train_ids[0]}", end="")
        if len(train_ids) > 1:
            for t in train_ids[1:]:
                print(f"  →  KTX-{t}", end="")
        print("]")

        # 역 출력
        print("  →  ".join(stations))
        # 시간 출력
        if len(train_ids) == 1:
            print(f"{times[0][:2]}:{times[0][2:]}  →  {times[1][:2]}:{times[1][2:]}")
        else:
            # 환승의 경우 (두 열차)
            print(f"{times[0][:2]}:{times[0][2:]}  →  {times[1][:2]}:{times[1][2:]} / "
                  f"{times[2][:2]}:{times[2][2:]}  →  {times[3][:2]}:{times[3][2:]}")
        # 좌석 출력
        print("좌석번호: ", end="")
        print("  →  ".join([str(s) + "번" for s in seats]))
        # 비용, 소요시간, 티켓번호
        print(f"비용: {fee}원 / 소요시간: {dur_h}시간 {dur_m}분")
        print(f"티켓번호: {t_num}")
        print("─────────────────")
