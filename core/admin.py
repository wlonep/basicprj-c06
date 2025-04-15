from model import Train
import os
import re

class Admin:
    def __init__(self):
        # 클래스 인스턴스가 초기화될 때 호출되는 메서드입니다.
        self.valid_stations = self.load_valid_stations()

    @staticmethod
    def get_train_list():
        print("[열차 목록 조회]")
        train = Train("downward")
        for tid, info in train.train_data.items():
            for key, value in info.items():
                if key == "STATION":
                    value = ",".join([s.replace("역", "") for s in value])
                if key == "BOOKED":
                    if value == []:
                        value = ""
                print(f"{key}={value}")
            print("-----------------------------------------------\n\n\n")
        train2 = Train("upward")
        for tid, info in train2.train_data.items():
            for key, value in info.items():
                if key == "STATION":
                    value = ",".join([s.replace("역", "") for s in value])
                if key == "BOOKED":
                    if value == []:
                        value = ""
                print(f"{key}={value}")
            print("-----------------------------------------------\n\n\n")

    def load_valid_stations(self, filepath="src/stations/gyeongbu.txt") -> list:
        """유효한 역 목록을 파일에서 읽어오는 메서드"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"{filepath} 파일을 찾을 수 없습니다.")
        with open(filepath, 'r', encoding='UTF-8') as f:
            stations = []
            for line in f:
                if '=' in line:
                    name, _ = line.strip().split('=')
                    stations.append(name)
        return stations

    def get_existing_train_ids(self) -> set:
        existing_ids = set()
        for direction in ["upward","downward"]:
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

    def get_input(self, prompt, validation_function=None, *args):
        while True:
            user_input = input(prompt)
            if validation_function:
                try:
                    return validation_function(user_input, *args)
                except ValueError as ve:
                    print(f"{ve}")
            else:
                return user_input

    def create_train_file(self):
        print("[열차 편성 추가]")
        try:
            tid = self.get_input("TRAIN_ID: ", self.validate_train_id)
            stations_input = self.get_input("STATION: ", self.validate_stations_input)

            while True:
                # FEE 입력 받기
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
                "BASE_FEE": int(base_fee),
                "FEE": int(fee),
                "BOOKED": []
            }

            way = "upward" if int(tid) % 2 == 0 else "downward"
            directory = f"src/train/{way}"
            os.makedirs(directory, exist_ok=True)
            file_path = f"{directory}/KTX-{tid}.txt"

            with open(file_path, 'w', encoding='UTF-8') as file:
                file.write(f"TRAIN_ID={tid}\n")
                for key in ["STATION", "BASE_FEE", "FEE", "BOOKED"]:
                    val = data[key]
                    if isinstance(val, list):
                        val = ','.join(val)
                    file.write(f"{key}={val}\n")

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

    def validate_stations_input(self, user_input):
        """STATION 입력 검증"""

        # 1. 공백 문자(스페이스, 탭, 줄바꿈 등)가 포함된 경우
        if any(c.isspace() for c in user_input):
            raise ValueError("*잘못된 입력 형식입니다. 다시 입력해주세요.")

        # 2. 쉼표 이외의 구분자가 있으면 잘못된 형식
        if re.search(r'[^가-힣,]', user_input):  # 한글과 쉼표 외의 다른 문자
            raise ValueError("*잘못된 입력 형식입니다. 다시 입력해주세요.")

        # 3. 쉼표가 없으면 오류
        if ',' not in user_input:
            raise ValueError("*잘못된 입력 형식입니다. 다시 입력해주세요.")

        # 4. 쉼표로 분할 후 빈 항목이 있거나, 2개 미만이면 오류
        stations = user_input.split(',')
        if '' in stations or len(stations) < 2:
            raise ValueError("*잘못된 입력 형식입니다. 다시 입력해주세요.")

        # 5. 존재하지 않는 역이 포함되어 있으면 오류
        if any(st not in self.valid_stations for st in stations):
            raise ValueError("*잘못된 입력 형식입니다. 다시 입력해주세요.")

        # 6. 역 순서가 오름차순 또는 내림차순이어야 함
        weights = [self.valid_stations.index(st) for st in stations]
        if not (weights == sorted(weights) or weights == sorted(weights, reverse=True)):
            raise ValueError("*입력 순서가 적절하지 않습니다. 다시 입력해주세요.")
        return user_input

    def validate_fee(self, user_input):
        """FEE 검증"""
        if re.search(r'\s', user_input) or not user_input.isdigit():
            raise ValueError("*FEE는 1 이상 1000000 미만의 자연수이어야 합니다. 다시 입력해주세요.")
        fee = int(user_input)
        if not (1 <= fee < 1000000):
            raise ValueError("*FEE는 1 이상 1000000 미만의 자연수이어야 합니다. 다시 입력해주세요.")
        return fee
