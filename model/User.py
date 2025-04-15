import os
import re


class User:
    def __init__(self, user_id: str = None):
        """
        User 클래스 선언 시 user_id를 인자로 넣었다면
        해당 user_id를 가진 파일 하나만 불러오기 때문에 user_ids는 빈 배열이 됩니다.
        user_ids를 사용하는 load_user_data와 is_user_exist 함수 모두
        user_id가 지정되지 않은 로그인이나 회원가입 시에만 사용되고,
        User 클래스는 예약 시에도 사용되기 때문에 이와 같이 설계하였습니다.
        """

        # 사용자 데이터 파일이 저장될 디렉토리 경로
        self.__USER_FILES = "src/user"
        # 모든 사용자 아이디를 저장할 배열
        self.user_ids = []
        # 특정 사용자와 관련된 데이터를 저장하는 딕셔너리
        self.user_data = {}

        self.user_id = user_id
        if not user_id:
            self.__load_user_ids()
        else:
            self.__load_user_data()

    def __load_user_ids(self):
        """
        사용자 데이터 로드 함수입니다.
        클래스 선언 시 init 함수에서 함께 실행됩니다.
        user_ids 배열에 사용자 아이디 집합을 저장합니다.
        :return:
        """
        if not os.path.isdir(self.__USER_FILES):
            os.makedirs(self.__USER_FILES)
        user_files = os.listdir(self.__USER_FILES)
        self.user_ids = [uf.replace('.txt', '') for uf in user_files]

    def is_user_exist(self, uid: str) -> bool:
        """
        사용자 아이디를 받고 그 아이디의 존재 여부를 반환합니다.
        :param uid: 사용자 아이디(string)
        :return: 아이디가 존재한다면 True, 존재하지 않는다면 False를 반환합니다.
        """
        if uid.lower() in self.user_ids:
            return True
        return False

    def register(self, uid: str, password: str) -> bool:
        """
        회원가입 함수입니다. 본 함수 사용 전 **반드시** is_user_exist() 함수를
        먼저 사용해 중복 계정이 있는지를 확인해야 합니다.
        사용하지 않는다면 아이디를 중복으로 입력했을 때 사용자 데이터 파일이 덮어씌워집니다.
        :param uid: 입력받은 사용자 아이디(string)
        :param password: 입력받은 비밀번호(string)
        :return: 회원가입이 정상적으로 처리되었다면 True를 반환합니다.
        """
        if not os.path.isdir(self.__USER_FILES):
            os.makedirs(self.__USER_FILES)
        with open(f"{self.__USER_FILES}/{uid.lower()}.txt", "w", encoding='UTF-8') as file:
            file.write(password)
        self.user_ids.append(uid.lower())
        return True

    def login(self, uid: str, password: str) -> bool:
        """
        로그인 함수입니다. 프로그램 실행 중간에 src/user 폴더가 삭제되었다면 FileNotFoundError가 발생합니다.
        :param uid: 입력받은 사용자 아이디(string)
        :param password: 입력받은 비밀번호(string)
        :return: 입력받은 아이디와 비밀번호가 일치한다면 True를 반환합니다.
        """
        if not os.path.isdir(self.__USER_FILES):
            raise FileNotFoundError("User data files are missing.")
        with open(f"{self.__USER_FILES}/{uid.lower()}.txt", "r", encoding='UTF-8') as file:
            lines = file.readlines()
        correct = lines[0].strip()
        if password != correct:
            return False
        self.__load_user_data(uid)
        return True

    @staticmethod
    def is_valid_username(username):
        if re.fullmatch(r'(?=.*[a-z])(?=.*\d)[a-z\d]{4,12}', username):
            return True
        return False

    @staticmethod
    def is_valid_password(password):
        if re.fullmatch(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,16}', password):
            return True
        return False

    def logout(self):
        """
        현재 로그인된 사용자 정보를 초기화하여 로그아웃 처리합니다.
        :return: None
        """
        print("로그아웃합니다. 이용해주셔서 감사합니다.")
        self.user_id = None
        self.user_data = {}


    # 특정 사용자 아이디 파일의 데이터 호출
    def __load_user_data(self, uid: str = None):
        if not self.user_id:
            self.user_id = uid
        with open(f"{self.__USER_FILES}/{self.user_id}.txt", "r", encoding='UTF-8') as file:
            lines = file.readlines()
        self.user_data["password"] = lines[0].strip()
        self.user_data["booked_list"] = {}
        for line in lines[1:]:
            # temp[0] = train_id인데, 이 값이 정수형이 아닌 경우 오류 발생함
            temp = line.strip().split('-')
            self.user_data["booked_list"][int(temp[0])] = {
                "depart": temp[1],
                "arrive": temp[2],
            }

    def add_booking(self, train_id: int, depart: str, arrive: str) -> bool:
        """
        사용자 계정에 예매 정보를 추가하는 함수입니다.
        모든 예매는 로그인 후 이루어진다고 가정하여 User 클래스 선언 시
        user_id를 인자로 받은 경우에만 호출이 가능합니다.
        :param train_id: 기차 번호(int)
        :param depart: 출발지(string)
        :param arrive: 도착지(string)
        :return: 예약이 정상적으로 처리되었다면 True를 반환합니다.
        """
        self.user_data[train_id] = {
            "depart": depart,
            "arrive": arrive,
        }
        with open(f"{self.__USER_FILES}/{self.user_id}.txt", "a", encoding='UTF-8') as file:
            file.write(f"\n{train_id}-{depart}-{arrive}")
        return True

    def cancel_booked(self, cancel: int):
        with open(f"{self.__USER_FILES}/{self.user_id}.txt", "w", encoding='UTF-8') as file:
            data = self.user_data
            password = data["password"]
            file.write(f"{password}")
            for key in data["booked_list"]:
                if key == cancel:
                    continue
                file.write(f"\n{key}-{data['booked_list'][key]['depart']}-{data['booked_list'][key]['arrive']}")
