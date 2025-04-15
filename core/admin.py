from model import Train
import os

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

    def validate_train_data(self, data: dict) -> bool:
        """기차 편성 데이터를 검증하는 메서드"""

        fee = data.get("FEE")
        base_fee = data.get("BASE_FEE")

        if not (isinstance(fee, int) and 1 <= fee < 1000000):
            raise ValueError("*FEE는 1000000 미만의 자연수이어야 합니다. 다시 입력해주세요.")
        if not (isinstance(base_fee, int) and base_fee >= 1):
            #변경해야함
            raise ValueError("BASE_FEE must be an integer greater than or equal to 1.")
        if not (fee > base_fee):
            raise ValueError("*BASE_FEE는 FEE보다 작은 값이어야 합니다. 다시 입력해주세요.")

        return True

    def get_input(self, prompt, validation_function=None, *args):
        while True:
            user_input = input(prompt)
            if validation_function:
                try:
                    return validation_function(user_input, *args)
                except ValueError as ve:
                    print(f"❌ 입력 오류: {ve}")
            else:
                return user_input

    def create_train_file(self):
        print("=== 열차 편성 정보 입력 ===")
        try:
            tid = self.get_input("TRAIN_ID: ", self.validate_train_id)
            stations_input = self.get_input("STATION: ", self.validate_stations_input)
            fee = self.get_input("FEE: ", self.validate_fee)
            base_fee = self.get_input("BASE_FEE: ", self.validate_base_fee, fee)

            data = {
                "TRAIN_ID": int(tid),
                "STATION": [s.strip() for s in stations_input.split(",") if s.strip()],
                "BASE_FEE": int(base_fee),
                "FEE": int(fee),
                "BOOKED": []
            }

            self.validate_train_data(data)

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

            print(f"✅ 열차 편성 저장 완료: {file_path}")

        except Exception as e:
            print(f"❌ 예상치 못한 오류 발생: {e}")

    def validate_train_id(self, user_input):
        """TRAIN_ID 검증"""
        tid = int(user_input)
        if not (1 <= tid < 10000):
            raise ValueError("*잘못된 입력 형식입니다. 다시 입력해주세요.")
        return tid

    def validate_stations_input(self, user_input):
        """STATION 입력 검증"""
        stations = [s.strip() for s in user_input.split(",")]
        if any(st not in self.valid_stations for st in stations):
            #변경해야함
            raise ValueError(f"@@Invalid station name in STATION list. Must be in {self.valid_stations}.@@")
        weights = [self.valid_stations.index(st) for st in stations]
        if not (weights == sorted(weights) or weights == sorted(weights, reverse=True)):
            raise ValueError("*입력 순서가 적절하지 않습니다. 다시 입력해주세요.")
        return user_input

    def validate_base_fee(self, user_input, fee):
        base_fee = int(user_input)
        if base_fee < 1:
            raise ValueError("@@BASE_FEE must be greater than or equal to 1.@@")
        if base_fee >= int(fee):
            raise ValueError("*BASE_FEE는 FEE보다 작은 값이어야 합니다. 다시 입력해주세요.")
        return base_fee

    def validate_fee(self, user_input):
        """FEE 검증"""
        fee = int(user_input)
        if not (1 <= fee < 1000000):
            raise ValueError("*FEE는 1000000 미만의 자연수이어야 합니다. 다시 입력해주세요.")
        return fee