import os


class User:
    def __init__(self):
        self.__USER_FILES = "src/user"
        self.user_ids = []
        self.user_data = {}
        self.__load_user_data()

    def __load_user_data(self):
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
        for line in lines[1:]:
            temp = line.split('-')

        return True

