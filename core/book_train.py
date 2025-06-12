import re
from contextlib import nullcontext

from model import Station, Train, User, Ticket


class BookTrain:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.user = User(user_id)
        self.train_data = []
        self.depart = ""
        self.arrive = ""
        self.train = None
        self.index = 1
        self.transfer_stations = []
        self.transfers = []
        self.seat = []
        self.flag = 1
        self.count = 1
        self.select_train = dict()
        self.book_seats = []
        self.isReserved = False

        if not self.train:
            self.__get_train_list()

    def reserve_ticket(self, t: dict):
        if len(self.transfers) == 0:
            """
                환승 아닐 경우
            """
            if re.fullmatch(r"[1-9][0-9]*", str(self.book_seats[0])):
                if int(self.book_seats[0]) > 20:
                    print("\033[31m" + "*잘못된 입력입니다. 올바른 좌석을 선택해주세요." + "\033[0m")
                    self.print_seats(self.select_train)
                else:
                    if self.book_seats[0] in self.select_train['BOOKED']:
                        print("\033[31m" + "*이미 예약된 좌석입니다. 다른 좌석을 선택해주세요." + "\033[0m")
                        self.print_seats(self.select_train)
                    else:
                        ticket = Ticket()
                        ticket_id = ticket.create_ticket_id()

                        ticket_dict = {
                            "stations": [self.depart[:-1], self.arrive[:-1]],
                            "train_ids": [self.select_train['TRAIN_ID']],
                            "booked_seats": [self.book_seats[0]]
                        }

                        is_ticketed = ticket.book_ticket(self.user_id, ticket_id, ticket_dict)

                        print(f"[KTX-{self.select_train['TRAIN_ID']}] {self.book_seats[0]}번 자리 예약이 완료되었습니다.")
                        self.isReserved = True

                        print("모든 좌석 선택이 끝났으므로 예매가 종료됩니다.")
                        print(is_ticketed)
                        if is_ticketed:
                            ticket.get_ticket(ticket_id)
                            ticket_data = ticket.get_ticket(ticket_id)
                            print(ticket_data)
                            print(f"[KTX-{ticket_data[ticket_id]['train_ids'][0]}]")
                            print(f"{self.depart[:-1]} -> {self.arrive[:-1]}")
                            dt_index = self.select_train['STATION'].index(self.depart)
                            at_index = self.select_train['STATION'].index(self.arrive)
                            dep_time = self.select_train['STOP_TIME'][dt_index]
                            arr_time = self.select_train['STOP_TIME'][at_index]
                            print(f"{dep_time[:2]}:{dep_time[2:]} -> {arr_time[:2]}:{arr_time[2:]}")
                            print(f"좌석번호 : {ticket_data[ticket_id]['booked_seats'][0]}번")
                            stationgn = Station().get_stations("gangneung")
                            stationja = Station().get_stations("jungang")

                            formatgn = list(stationgn.keys())
                            formatja = list(stationja.keys())

                            gn = all(item in formatgn for item in self.select_train['STATION'])
                            ja = all(item in formatja for item in self.select_train['STATION'])

                            if gn:
                                route = 14
                            if ja:
                                route = 15
                            else:
                                route = 17

                            total_fee = f"비용 : {int(self.select_train['BASE_FEE'] + (self.select_train['FEE'] - self.select_train['BASE_FEE']) * (at_index - dt_index) / route)}원"
                            hour = int(arr_time[:2]) - int(dep_time[:2])
                            minute = int(arr_time[2:]) - int(dep_time[2:])
                            if minute < 0:
                                minute += 60
                                hour -= 1
                            print(f"{total_fee} / 소요시간 : {hour}시간 {minute}분")
                            print(f"티켓 번호 : {ticket_id}")
                        print("------------------------------------")
            else:
                print("\033[31m" + "*잘못된 입력입니다. 올바른 좌석을 선택해주세요." + "\033[0m")
                self.print_seats(self.select_train)
        else:
            """
                환승일 경우
            """
            if re.fullmatch(r"[1-9][0-9]*", str(self.book_seats[self.count - 1])):
                if int(self.book_seats[self.count - 1]) > 20:
                    print("\033[31m" + "*잘못된 입력입니다. 올바른 좌석을 선택해주세요." + "\033[0m")
                    self.print_seats(self.select_train)
                else:
                    if self.book_seats[self.count - 1] in self.select_train[self.count - 1]['BOOKED']:
                        print("\033[31m" + "*이미 예약된 좌석입니다. 다른 좌석을 선택해주세요." + "\033[0m")
                        self.print_seats(self.select_train)
                    else:
                        print(
                            f"[KTX-{self.select_train[self.count - 1]['TRAIN_ID']}] {self.book_seats[self.count - 1]}번 자리 예약이 완료되었습니다.")
                        self.isReserved = True
                        if self.count == 2:
                            print("모든 좌석 선택이 끝났으므로 예매가 종료됩니다.")
                            ticket = Ticket()
                            ticket_id = ticket.create_ticket_id()

                            ticket_dict = {
                                "stations": [self.depart, self.transfers[self.index - 2], self.arrive],
                                "train_ids": [int(self.select_train[0]['TRAIN_ID']),
                                              int(self.select_train[1]['TRAIN_ID'])],
                                "booked_seats": [int(self.book_seats[0]), int(self.book_seats[1])]
                            }

                            is_ticketed = ticket.book_ticket("test", ticket_id, ticket_dict)
                            if is_ticketed:
                                ticket_data = ticket.get_ticket(ticket_id)
                                print(ticket_data)
                                trans = ticket_data[ticket_id]['stations'][1]
                                print(
                                    f"[KTX-{ticket_data[ticket_id]['train_ids'][0]} -> KTX-{ticket_data[ticket_id]['train_ids'][1]}]")
                                print(f"{self.depart[:-1]} -> {trans[:-1]} -> {self.arrive[:-1]}")
                                dt_index = self.select_train[0]['STATION'].index(self.depart)
                                trb_idx = self.select_train[0]['STATION'].index(trans)
                                tra_idx = self.select_train[1]['STATION'].index(trans)
                                at_index = self.select_train[1]['STATION'].index(self.arrive)
                                dep_time = self.select_train[0]['STOP_TIME'][dt_index]
                                tr_off_time = self.select_train[0]['STOP_TIME'][trb_idx]
                                tr_on_time = self.select_train[1]['STOP_TIME'][tra_idx]
                                arr_time = self.select_train[1]['STOP_TIME'][at_index]
                                print(f"{dep_time[:2]}:{dep_time[2:]} -> {tr_off_time[:2]}:{tr_off_time[2:]} "
                                      f"/ {tr_on_time[:2]}:{tr_on_time[2:]} -> {arr_time[:2]}:{arr_time[2:]}")
                                print(
                                    f"좌석번호 : {ticket_data[ticket_id]['booked_seats'][0]}번 -> {ticket_data[ticket_id]['booked_seats'][1]}번")
                                stationgn = Station().get_stations("gangneung")
                                stationja = Station().get_stations("jungang")

                                formatgn = list(stationgn.keys())
                                formatja = list(stationja.keys())

                                gn = all(item in formatgn for item in self.select_train[0]['STATION'])
                                ja = all(item in formatja for item in self.select_train[0]['STATION'])

                                if gn:
                                    route1 = 14
                                elif ja:
                                    route1 = 15
                                else:
                                    route1 = 17

                                gn1 = all(item in formatgn for item in self.select_train[1]['STATION'])
                                ja1 = all(item in formatja for item in self.select_train[1]['STATION'])

                                if gn1:
                                    route2 = 14
                                elif ja1:
                                    route2 = 15
                                else:
                                    route2 = 17

                                base_fee1 = self.select_train[0]['BASE_FEE']
                                base_fee2 = self.select_train[1]['BASE_FEE']
                                fee1 = self.select_train[0]['FEE']
                                fee2 = self.select_train[1]['FEE']
                                calc_fee = (base_fee1 + base_fee2) / 2 + (fee1 - base_fee1) * (
                                        trb_idx - dt_index) / route1 + (fee2 - base_fee2) * (
                                                   at_index - tra_idx) / route2

                                hour = int(arr_time[:2]) - int(dep_time[:2])
                                minute = int(arr_time[2:]) - int(dep_time[2:])
                                if minute < 0:
                                    minute += 60
                                    hour -= 1
                                print(f"{int(calc_fee)}원 / 소요시간 : {hour}시간 {minute}분")
                                print(f"티켓 번호: {ticket_id}")
                        print("------------------------------------")
                        self.count += 1
            else:
                print("\033[31m" + "*잘못된 입력입니다. 올바른 좌석을 선택해주세요." + "\033[0m")
                self.print_seats(self.select_train)

        # while True:
        #     tn = input("선택하실 열차 번호를 입력해주세요: ")
        #
        #     if re.fullmatch(r"[1-9][0-9]*", tn):
        #         pass
        #     else:
        #         print("\033[31m" + "*잘못된 입력 형식입니다. 다시 입력해 주세요." + "\033[0m")
        #         continue
        #     fl = False
        #
        #     if int(tn) in list(self.user.user_data["booked_list"].keys()):
        #         print("\033[31m" + "* 이미 동일한 열차의 좌석을 예매하였습니다. 다시 입력해주세요." + "\033[0m")
        #         continue
        #
        #     for t in self.train_data:
        #         if int(tn) == t["TRAIN_ID"]:
        #             fl = True
        #     if fl:
        #         break
        #     else:
        #         print("\033[31m" + "*예매 가능한 열차가 아닙니다. 다시 입력해주세요." + "\033[0m")
        #
        # while True:
        #     seat = 1
        #     for t in self.train_data:
        #         if int(tn) == t["TRAIN_ID"]:
        #             print("====================")
        #             self.print_train(t)
        #             print("====================")
        #             idx = 1
        #             for s in t["BOOKED"]:
        #                 if int(s) != idx:
        #                     seat = idx
        #                     break
        #                 else:
        #                     idx += 1
        #             else:
        #                 seat = idx
        #
        #     choose = input("해당 열차로 예매를 진행하시겠습니까? ( 예 y / 아니오 n): ")
        #     if choose == 'y':
        #         self.train.book_seats(int(tn), seat)
        #         self.user.add_booking(int(tn), self.depart[:-1], self.arrive[:-1], seat)
        #         print("예매가 완료되었습니다. 메뉴로 돌아갑니다.")
        #         return
        #     elif choose == 'n':
        #         print("에매가 취소되었습니다. 메뉴로 돌아갑니다.")
        #         return
        #     else:
        #         print("\033[31m" + "*잘못된 입력 형식입니다. 다시 입력해 주세요." + "\033[0m")

    def __get_train_list(self):
        print("[열차 예매]")
        stationgn = Station().get_stations("gangneung")
        stationja = Station().get_stations("jungang")
        stationgb = Station().get_stations("gyeongbu")
        station_list = [stationgb, stationgn, stationja]

        route_dp = []
        route_av = []

        while True:
            self.depart = input("출발지: ")
            if self.depart[-1] != "역":
                self.depart += "역"

            found = False
            for st in station_list:
                if self.depart in st:
                    route_dp.append(st)
                    found = True

            if found:
                break
            print("\033[31m" + "* 일치하는 역이 존재하지 않습니다. 다시 입력해주세요." + "\033[0m")

        while True:
            self.arrive = input("도착지: ")
            if self.arrive[-1] != "역":
                self.arrive += "역"

            found = False
            for st in station_list:
                if self.arrive in st:
                    route_av.append(st)
                    found = True

            if found:
                break
            print("\033[31m" + "* 일치하는 역이 존재하지 않습니다. 다시 입력해주세요." + "\033[0m")

        route_equal = False
        for dp in route_dp:
            for av in route_av:
                if dp in route_av or av in route_dp:
                    weight = dp[self.depart] - dp[self.arrive]
                    route_equal = True
                    break
            if route_equal:
                break

        dtt_list = []
        tta_list = []

        if not route_equal:
            for dp in route_dp:
                for av in route_av:
                    common = [station for station in dp if station in av]
                    self.transfer_stations.extend(common)

            for ts in self.transfer_stations:
                for pr in route_dp:
                    if ts in pr:
                        weight = pr[self.depart] - pr[ts]
                        if weight < 0:
                            way = "downward"
                        elif weight > 0:
                            way = "upward"

                        train_prev = Train(way)
                        dtt_list = train_prev.get_train_data(self.depart, ts)

                for ar in route_av:
                    if ts in ar:
                        weight = ar[ts] - ar[self.arrive]
                        if weight < 0:
                            way = "downward"
                        elif weight > 0:
                            way = "upward"

                        train_after = Train(way)
                        tta_list = train_after.get_train_data(ts, self.arrive)

        if self.transfer_stations:
            self.train_data = self.transfer_train_list(dtt_list, tta_list)

        if not self.transfer_stations:
            if weight < 0:
                way = "downward"
            elif weight > 0:
                way = "upward"
            else:
                print("\033[31m" + "* 출발지와 도착지가 같습니다. 다시 입력해주세요." + "\033[0m")

            self.train = Train(way)
            self.train_data = self.train.get_train_data(self.depart, self.arrive)

    def transfer_train_list(self, dtt_list: list, tta_list: list) -> list:
        dta_list = []
        for ts in self.transfer_stations:
            for dtt in dtt_list:
                if ts not in dtt["STATION"]:
                    continue
                ts_idx_dtt = dtt["STATION"].index(ts)
                dtt_arrival_str = dtt["STOP_TIME"][ts_idx_dtt]
                dtt_arrival_time = int(dtt_arrival_str[:2]) * 60 + int(dtt_arrival_str[2:])

                for tta in tta_list:
                    if ts not in tta["STATION"]:
                        continue
                    ts_idx_tta = tta["STATION"].index(ts)
                    tta_departure_str = tta["STOP_TIME"][ts_idx_tta]
                    tta_departure_time = int(tta_departure_str[:2]) * 60 + int(tta_departure_str[2:])

                    diff = tta_departure_time - dtt_arrival_time
                    if 10 <= diff <= 30:
                        dta_list.append({self.index: [dtt, tta]})
                        self.transfers.append(ts)
                        self.index += 1

        return dta_list

    def print_train(self, t: list):
        if not self.transfer_stations:
            """
            환승이 없을 경우
            """
            idx = 0
            for tr in t:

                idx += 1
                tid = f"[KTX-{tr['TRAIN_ID']}]"

                station = f"{self.depart[:-1]} → {self.arrive[:-1]}"

                dep_index = tr['STATION'].index(self.depart)
                arr_index = tr['STATION'].index(self.arrive)

                dep_time = tr['STOP_TIME'][dep_index]
                format_dep = f"{dep_time[:2]}:{dep_time[2:]}"
                arr_time = tr['STOP_TIME'][arr_index]
                format_arr = f"{arr_time[:2]}:{arr_time[2:]}"
                time = f"{format_dep} → {format_arr}"

                seat = f"남은좌석 : {20 - len(tr['BOOKED'])}석"

                stations = tr['STATION']  # 예: ['부산역', '울산역', ...]

                stationgn = Station().get_stations("gangneung")
                stationja = Station().get_stations("jungang")
                stationgb = Station().get_stations("gyeongbu")

                formatgn = list(stationgn.keys())
                formatja = list(stationja.keys())
                formatgb = list(stationgb.keys())

                is_gangneung = all(item in formatgn for item in stations)
                is_jungang = all(item in formatja for item in stations)
                is_gyeongbu = all(item in formatgb for item in stations)

                route = 0
                if is_gangneung:
                    route = 14
                elif is_jungang:
                    route = 15
                else:
                    route = 17

                fee = tr['FEE']
                base_fee = tr['BASE_FEE']

                total_fee = f"비용 : {int(base_fee + (fee - base_fee) * (arr_index - dep_index) / route)}원"

                hour = int(dep_time[:2])
                minute = int(dep_time[2:])
                taken_dep = hour * 60 + minute

                hour = int(arr_time[:2])
                minute = int(arr_time[2:])
                taken_arr = hour * 60 + minute

                time_taken = taken_arr - taken_dep

                hours = time_taken // 60
                minutes = time_taken % 60

                print(f"─────────────────\n{idx}) {tid}")
                print(station)
                print(time)
                print(seat)
                print(f"{total_fee} / 소요시간: {hours}시간 {minutes}분")

        else:
            """
                환승이 있을 경우
            """

            keys = []
            values = []

            for item in t:
                for key, value in item.items():
                    keys.append(key)
                    values.append(value)

            idx = 0
            for route in values:
                idx += 1
                dep_id = route[0]['TRAIN_ID']  # 각 리스트의 첫 번째 딕셔너리에서 TRAIN_ID 가져오기
                arr_id = route[1]['TRAIN_ID']
                tid = f"{idx}) [KTX-{dep_id}] -> [KTX-{arr_id}]"

                station = f"{self.depart[:-1]} -> {self.transfers[idx - 1][:-1]} -> {self.arrive[:-1]}"

                dep_index = route[0]['STATION'].index(self.depart)
                tr_index1 = route[0]['STATION'].index(self.transfers[idx - 1])
                arr_index = route[1]['STATION'].index(self.arrive)
                tr_index2 = route[1]['STATION'].index(self.transfers[idx - 1])

                dep_time = route[0]['STOP_TIME'][dep_index]
                format_dep = f"{dep_time[:2]}:{dep_time[2:]}"
                tr1_time = route[0]['STOP_TIME'][tr_index1]
                format_tr1 = f"{tr1_time[:2]}:{tr1_time[2:]}"
                arr_time = route[1]['STOP_TIME'][arr_index]
                format_arr = f"{arr_time[:2]}:{arr_time[2:]}"
                tr2_time = route[1]['STOP_TIME'][tr_index2]
                format_tr2 = f"{tr2_time[:2]}:{tr2_time[2:]}"
                time = f"{format_dep} → {format_tr1} / {format_tr2} → {format_arr}"

                seat = f"남은좌석 : {20 - len(route[0]['BOOKED'])}석 / {20 - len(route[1]['BOOKED'])}석"

                stations = route[0]['STATION']  # 예: ['부산역', '울산역', ...]
                stations2 = route[1]['STATION']  # 예: ['부산역', '울산역', ...]

                stationgn = Station().get_stations("gangneung")
                stationja = Station().get_stations("jungang")
                stationgb = Station().get_stations("gyeongbu")

                formatgn = list(stationgn.keys())
                formatja = list(stationja.keys())
                formatgb = list(stationgb.keys())

                is_gangneung = all(item in formatgn for item in stations)
                is_jungang = all(item in formatja for item in stations)
                is_gyeongbu = all(item in formatgb for item in stations)

                route1 = 0
                if is_gangneung:
                    route1 = 14
                elif is_jungang:
                    route1 = 15
                else:
                    route1 = 17

                is_gangneung1 = all(item in formatgn for item in stations2)
                is_jungang1 = all(item in formatja for item in stations2)
                is_gyeongbu1 = all(item in formatgb for item in stations2)

                route2 = 0
                if is_gangneung1:
                    route2 = 14
                elif is_jungang1:
                    route2 = 15
                else:  # elif is_gyeongbu
                    route2 = 17

                fee1 = route[0]['FEE']
                base_fee1 = route[0]['BASE_FEE']
                fee2 = route[1]['FEE']
                base_fee2 = route[1]['BASE_FEE']
                calc_fee = (base_fee1 + base_fee2) / 2 + (fee1 - base_fee1) * (tr_index1 - dep_index) / route1 + (
                        fee2 - base_fee2) * (arr_index - tr_index2) / route2

                total_fee = f"비용 : {int(calc_fee)}원"

                hour = int(dep_time[:2])
                minute = int(dep_time[2:])
                taken_dep = hour * 60 + minute

                hour = int(arr_time[:2])
                minute = int(arr_time[2:])
                taken_arr = hour * 60 + minute

                time_taken = taken_arr - taken_dep

                hours = time_taken // 60
                minutes = time_taken % 60

                print("--------------------------------")
                print(tid)
                print(station)
                print(time)
                print(seat)
                print(f"{total_fee} / 소요시간: {hours}시간 {minutes}분")

        print("--------------------------------")

        number = 0
        while True:
            sta_num = input("열차 목록 중 선택할 번호를 입력해주세요: ")
            if re.fullmatch(r"[1-9][0-9]*", sta_num):
                pass
            else:
                print("\033[31m" + "*잘못된 입력 형식입니다. 다시 입력해 주세요." + "\033[0m")
                continue

            number = int(sta_num)
            if number > idx or number == 0:
                print("*잘못된 입력 형식입니다. 다시 입력해주세요.")
                continue
            break

        if len(self.transfers) == 0:
            print(t[number - 1])
            self.select_train = t[number - 1]
            self.print_seats(self.select_train)
        else:
            for item in t:
                if number in item:
                    print(item[number])
                    self.select_train = item[number]
                    self.print_seats(self.select_train)
        return

    def print_seats(self, t: dict):
        if len(t) == 2:
            """
            환승
            """
            if self.flag == 1:
                print("*좌석을 선택합니다.")
                print(f"[KTX-{t[self.count - 1]['TRAIN_ID']} 자리 현황]")
                number = 1
                for r in range(5):
                    # 상단 선
                    print("+----" * 4 + "+")

                    # 숫자 라인
                    for c in range(4):
                        if number <= 20:
                            if number in t[self.count - 1]['BOOKED']:
                                print("|  X ", end="")  # 예약된 좌석 → X 표시
                            else:
                                print(f"| {number:2} ", end="")  # 예약 안 된 좌석
                            number += 1
                        else:
                            print("|    ", end="")  # 빈 자리
                    print("|")

                    # 마지막 하단 선
                print("+----" * 4 + "+")
                self.flag += 1
            self.book_seats.append(input("좌석을 선택해 주세요: "))
        else:
            """
            환승 x
            """
            if self.flag == 1:
                print("*좌석을 선택합니다.")
                print(f"[KTX-{t['TRAIN_ID']} 자리 현황]")
                number = 1
                for r in range(5):
                    # 상단 선
                    print("+----" * 4 + "+")

                    # 숫자 라인
                    for c in range(4):
                        if number <= 20:
                            if number in t['BOOKED']:
                                print("|  X ", end="")  # 예약된 좌석 → X 표시
                            else:
                                print(f"| {number:2} ", end="")  # 예약 안 된 좌석
                            number += 1
                        else:
                            print("|    ", end="")  # 빈 자리
                    print("|")

                    # 마지막 하단 선
                print("+----" * 4 + "+")
                self.flag += 1
            self.book_seats.append(input("좌석을 선택해 주세요: "))

    def print_menu(self):
        print(self.train_data)
        if len(self.train_data) == 0:
            print("\033[31m" + "* 해당 출발지에서 도착지로 가는 모든 열차의 좌석이 매진되었습니다. 메뉴로 돌아갑니다." + "\033[0m")
            return

        # for t in self.train_data:
        #     self.print_train(t)
        #     print("-----------------------")
        # self.reserve_ticket()

        self.print_train(self.train_data)
        while True:
            self.reserve_ticket(self.select_train)
            if self.isReserved:
                break
        if len(self.transfers) != 0:
            while True:
                self.flag = 1
                self.print_seats(self.select_train)
                self.reserve_ticket(self.select_train)
                if self.isReserved:
                    break

        return
