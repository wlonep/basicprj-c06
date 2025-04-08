import os


class Station:
    def __init__(self):
        self.__STATION_FILES = "src/stations"
        self.__station_data = {}
        self.__load_station_data()

    def __load_station_data(self):
        """
        역 데이터 로드 함수입니다.
        클래스 선언 시 init 함수에서 함께 실행됩니다.
        __station_data 딕셔너리에 노선 ID와 그 노선의 역, 가중치를 저장합니다.
        :return:
        """
        if not os.path.isdir(self.__STATION_FILES):
            raise FileNotFoundError("src/stations folder is missing.")
        for sf in os.listdir(self.__STATION_FILES):
            self.__station_data[sf.replace(".txt", "")] = {}
            with open(f"{self.__STATION_FILES}/{sf}", 'r', encoding='UTF-8') as file:
                lines = file.readlines()
            for line in lines:
                temp = line.strip('\n').split('=')
                self.__station_data[sf.replace(".txt", "")][temp[0]] = int(temp[1])

    def get_stations(self, route: str) -> dict:
        """
        역 목록을 fetch하는 함수입니다.
        노선 ID가 존재하지 않는 경우 빈 딕셔너리를 반환합니다.
        :param route: 노선 ID(string)
        :return:
        """
        try:
            return self.__station_data[route]
        except KeyError:
            return {}
