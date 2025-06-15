from model import Train
import os
import re


class Admin:
    def __init__(self):
        # 클래스 인스턴스가 초기화될 때 호출되는 메서드입니다.
        self.valid_station_dict = self.load_all_valid_stations()

    @staticmethod
    def get_train_list():
        print("[열차 목록 조회]")
        train = Train("downward")
        for tid, info in train.train_data.items():
            for key, value in info.items():
                if key == "STATION":
                    value = ",".join([s.replace("역", "") for s in value])
                elif key == "BOOKED":
                    if not value:
                        value = ""
                    else:
                        value = ",".join(value)
                print(f"{key}={value}")
            print("-----------------------------------------------")

        train2 = Train("upward")
        for tid, info in train2.train_data.items():
            for key, value in info.items():
                if key == "STATION":
                    value = ",".join([s.replace("역", "") for s in value])
                elif key == "BOOKED":
                    if not value:
                        value = ""
                    else:
                        value = ",".join(value)
                print(f"{key}={value}")
            print("-----------------------------------------------")

    @staticmethod
    def load_all_valid_stations(directory="src/stations") -> dict:
        """
        src/stations 폴더 내 모든 *.txt 노선 파일을 읽고
        {노선명: [역1, 역2, ...]} 형태로 딕셔너리 반환
        """
        valid_stations = {}
        if not os.path.exists(directory):
            raise FileNotFoundError(f"{directory} 폴더가 존재하지 않습니다.")

        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                route_name = filename.replace(".txt", "")
                filepath = os.path.join(directory, filename)
                stations = []
                with open(filepath, 'r', encoding='UTF-8') as f:
                    for line in f:
                        if '=' in line:
                            name, _ = line.strip().split('=')
                            stations.append(name)
                valid_stations[route_name] = stations

        return valid_stations

    @staticmethod
    def get_existing_train_ids() -> set:
        existing_ids = set()
        for direction in ["upward", "downward"]:
            dir_path = f"src/train/{direction}"
            if not os.path.exists(dir_path):
                continue
            for filename in os.listdir(dir_path):
                if filename.startswith("KTX-") and filename.endswith(".txt"):
                    try:
                        train_id = int(filename.split("-")[1].split(".")[0])
                        existing_ids.add(train_id)
                    except ValueError:
                        continue
        return existing_ids

    @staticmethod
    def get_input(prompt, validation_function=None, *args):
        while True:
            user_input = input(prompt)
            if validation_function:
                try:
                    return validation_function(user_input, *args)
                except ValueError as ve:
                    print("\033[31m" + f"{ve}" + "\033[0m")
            else:
                return user_input

    def create_train_file(self):
        print("[열차 편성 추가]")
        try:
            tid = self.get_input("TRAIN_ID: ", self.validate_train_id)
            stations_input = self.get_input("STATION: ", self.validate_stations_input, tid)
            station_list = [s.strip() for s in stations_input.split(",") if s.strip()]
            way = "upward" if int(tid) % 2 == 0 else "downward"
            stop_times = self.get_input("STOP_TIME: ", self.validate_stop_times_input, station_list, way)
            while True:
                fee = self.get_input("FEE: ", self.validate_fee)
                base_fee = None  # 예외 대비 초기화
                base_fee_input = input("BASE_FEE: ")

                if not base_fee_input or re.search(r"\s", base_fee_input):
                    print("*BASE_FEE는 1 이상 FEE 미만의 자연수여야 합니다.")
                    continue

                if not base_fee_input.isdigit():
                    print("*BASE_FEE는 1 이상 FEE 미만의 자연수여야 합니다.")
                    continue

                base_fee = int(base_fee_input)
                if base_fee < 1 or base_fee >= fee:
                    print("*BASE_FEE는 1 이상 FEE 미만의 자연수여야 합니다.")
                    continue

                break

            data = {
                "TRAIN_ID": int(tid),
                "STATION": [s.strip() for s in stations_input.split(",") if s.strip()],
                "STOP_TIME": stop_times,
                "FEE": int(fee),
                "BASE_FEE": int(base_fee),
                "BOOKED": []
            }

            way = "upward" if int(tid) % 2 == 0 else "downward"
            directory = f"src/train/{way}"
            os.makedirs(directory, exist_ok=True)
            file_path = f"{directory}/KTX-{tid}.txt"

            with open(file_path, 'w', encoding='UTF-8') as file:
                for key, value in data.items():
                    if isinstance(value, list):
                        value = ','.join(value)
                    file.write(f"{key}={value}\n")

            print("열차 편성이 데이터 파일에 추가되었습니다. 메뉴로 돌아갑니다.")
        except Exception as e:
            print(f"❌ 예상치 못한 오류 발생: {e}")

    def validate_train_id(self, user_input):
        """TRAIN_ID 검증"""
        try:
            tid = int(user_input)
        except ValueError:
            raise ValueError("*잘못된 입력 형식입니다. 다시 입력해주세요.")

        if not (1 <= tid < 10000):
            raise ValueError("*잘못된 입력 형식입니다. 다시 입력해주세요.")

        existing_ids = self.get_existing_train_ids()
        if tid in existing_ids:
            raise ValueError("*목록에 이미 존재하는 열차 고유 번호입니다. 다시 입력해주세요.")
        return tid

    def validate_stations_input(self, user_input, tid):
        """STATION 입력 검증"""

        # 1. 공백 문자(스페이스, 탭, 줄바꿈 등)가 포함된 경우
        if any(c.isspace() for c in user_input):
            raise ValueError("*잘못된 입력 형식입니다. 다시 입력해주세요.")

        # 2. 쉼표 이외의 구분자가 있으면 잘못된 형식
        if re.search(r'[^가-힣,역]', user_input):  # 한글과 쉼표 외의 다른 문자
            raise ValueError("*잘못된 입력 형식입니다. 다시 입력해주세요.")

        # 3. 쉼표가 없으면 오류
        if ',' not in user_input:
            raise ValueError("*잘못된 입력 형식입니다. 다시 입력해주세요.")

        # 4. 쉼표로 분할 후 빈 항목이 있거나, 2개 미만이면 오류
        stations = user_input.split(',')
        if '' in stations or len(stations) < 2:
            raise ValueError("*잘못된 입력 형식입니다. 다시 입력해주세요.")

        stripped_stations = [s.strip().removesuffix("역") for s in stations]

        # 5. 존재하지 않는 역 이름이 있는지 확인
        all_valid_stations = set()
        for route_stations in self.valid_station_dict.values():
            all_valid_stations.update(route_stations)

        for st in stripped_stations:
            if st not in all_valid_stations:
                raise ValueError("*존재하지 않는 역 이름이 포함되어있습니다. 다시 입력해주세요.")

        # 6. 모든 역이 동일한 노선에 속하는지 확인
        matched_route = None
        for route_name, route_stations in self.valid_station_dict.items():
            if all(st in route_stations for st in stripped_stations):
                matched_route = route_stations
                break

        if matched_route is None:
            raise ValueError("*입력된 역들이 서로 다른 노선에 속해있습니다. 다시 입력해주세요.")

        # 6. 입력된 역이 노선 내에서 오름차순 또는 내림차순이어야 함
        weights = [matched_route.index(st) for st in stripped_stations]
        ascending = weights == sorted(weights)
        descending = weights == sorted(weights, reverse=True)

        if not (ascending or descending):
            raise ValueError("*입력 순서가 적절하지 않습니다. 다시 입력해주세요.")

        # 7. 열차 번호와 방향 일치 여부 확인
        if ascending and int(tid) % 2 == 0:
            raise ValueError("*입력한 열차 고유 번호는 상행이고 입력한 역 목록은 하행입니다. 다시 입력해주세요.")
        if descending and int(tid) % 2 != 0:
            raise ValueError("*입력한 열차 고유 번호는 하행이고 입력한 역 목록은 상행입니다. 다시 입력해주세요.")

        return ",".join(stripped_stations)

    @staticmethod
    def validate_fee(user_input):
        """FEE 검증"""
        if re.search(r'\s', user_input) or not user_input.isdigit():
            raise ValueError("*FEE는 2 이상 1000000 미만의 자연수이어야 합니다. 다시 입력해주세요.")
        fee = int(user_input)
        if not (2 <= fee < 1000000):
            raise ValueError("*FEE는 2 이상 1000000 미만의 자연수이어야 합니다. 다시 입력해주세요.")
        return fee

    @staticmethod
    def validate_stop_times_input(stop_input, station_list, way):
        import re

        # 1. 문법 규칙 검사
        if re.search(r'\s', stop_input):
            raise ValueError("*잘못된 입력 형식입니다. 다시 입력해주세요.")

        stop_times = stop_input.split(',')
        if len(stop_times) != len(station_list):
            raise ValueError("*잘못된 입력 형식입니다. 다시 입력해주세요.")

        for st in stop_times:
            if not re.fullmatch(r'\d{4}', st):
                raise ValueError("*잘못된 입력 형식입니다. 다시 입력해주세요.")


        # 2. 시간 형식 및 첫 정차 시각 검사
        def to_minutes(tm):
            return int(tm[:2]) * 60 + int(tm[2:])

        # 첫 시간 확인
        first_time = int(stop_times[0])
        if first_time >= 2400:
            raise ValueError("*첫 정차시간은 24:00 미만 이여야 합니다. 다시 입력해주세요.")

        has_crossed_midnight = False
        for i, t in enumerate(stop_times):
            hour = int(t[:2])
            minute = int(t[2:])
            time_int = int(t)

            if not (0 <= minute < 60):
                raise ValueError("*잘못된 시간 입력입니다. 다시 입력해주세요.")

            if 2400 <= time_int <= 2600:
                has_crossed_midnight = True
            elif 0 <= time_int <= 2359:
                if has_crossed_midnight:
                    raise ValueError("*잘못된 시간 입력입니다. 다시 입력해주세요.")
            else:
                raise ValueError("*잘못된 시간 입력입니다. 다시 입력해주세요.")

        # 3. 시간 순서 검사
        for i in range(1, len(stop_times)):
             if int(stop_times[i]) <= int(stop_times[i - 1]):
                 raise ValueError("*잘못된 시간 입력입니다. 다시 입력해주세요.")

        # 4. 정차역 간 최소 5분 이상 차이 검사
        for i in range(1, len(stop_times)):
            prev = to_minutes(stop_times[i - 1])
            curr = to_minutes(stop_times[i])
            if curr - prev < 5:
                raise ValueError("*역 간 이동에는 최소 5분 이상이 걸립니다. 다시 입력해주세요.")

        # 5. ±3분 이내 정차 충돌 검사
        existing_trains = Train(way)
        for station, new_time_str in zip(station_list, stop_times):
            new_time = to_minutes(new_time_str)
            station_name = station if station.endswith("역") else station + "역"

            for tid, info in existing_trains.train_data.items():
                if station_name not in info.get("STATION", []):
                    continue

                index = info["STATION"].index(station_name)

                stop_time_list = info.get("STOP_TIME")
                if not stop_time_list:
                    continue
                if isinstance(stop_time_list, str):
                    stop_time_list = stop_time_list.split(",")
                elif not isinstance(stop_time_list, list):
                    print(f"train {tid}의 STOP_TIME에 잘못된 데이터 형식이 저장되어 있습니다.")
                    continue

                if len(stop_time_list) <= index:
                    continue

                try:
                    existing_time_str = stop_time_list[index]
                    existing_time = to_minutes(existing_time_str)
                except Exception:
                    print(f"train {tid}의 STOP_TIME에 잘못된 데이터 형식이 저장되어 있습니다.")
                    continue

                if abs(existing_time - new_time) <= 3:
                    raise ValueError(f"*3분 이내에 같은 방향의 다른 열차({tid})가 '{station_name}'에 정차합니다. 다시 입력해주세요.")

        return stop_times
