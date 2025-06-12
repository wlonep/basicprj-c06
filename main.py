import sys
import os
from core.menu import main_menu
from model import Ticket
from model.train import Train
from model.user import User
from model.station import Station


def parse_train_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        data = {}
        for line in f:
            if '=' not in line:
                continue
            key, val = line.strip().split('=', 1)
            data[key.strip()] = val.strip()
    stations = data.get("STATION", "").split(",")
    stop_times = [int(s) for s in data.get("STOP_TIME", "").split(",") if s]
    train_id = data.get("TRAIN_ID", os.path.basename(filepath))
    if len(stations) != len(stop_times):
        raise ValueError()
    return train_id, stations, stop_times


def convert_times_to_monotonic(stop_times):
    mono_times = []
    prev = None
    day_offset = 0
    for idx, t in enumerate(stop_times):
        t_min = (t // 100) * 60 + (t % 100) + day_offset
        if prev is not None:
            if t_min < prev:
                if 0 <= t < 100:
                    day_offset += 24 * 60
                    t_min = (t // 100) * 60 + (t % 100) + day_offset
                else:
                    raise ValueError()
        prev = t_min
        mono_times.append(t_min)
    return mono_times


def check_train_data_validity(train_dirs):
    for train_dir in train_dirs:
        station_time_dict = dict()  # {역이름: [(train_id, stop_time)], ...}
        train_time_dict = dict()  # 열차번호별 monotonic time list 저장
        for fname in os.listdir(train_dir):
            if not fname.endswith(".txt"):
                continue
            path = os.path.join(train_dir, fname)
            train_id, stations, stop_times = parse_train_file(path)
            mono_times = convert_times_to_monotonic(stop_times)
            train_time_dict[train_id] = mono_times
            # 1. stop_time 오름차순 확인
            if mono_times != sorted(mono_times):
                raise ValueError()
            # 3. 연속된 stop_time 간격이 5분 미만일 때 에러
            for idx, (t1, t2) in enumerate(zip(mono_times, mono_times[1:])):
                if t2 - t1 <= 5:
                    st_name1 = stations[idx]
                    st_name2 = stations[idx + 1]
                    raise ValueError()
            # 2. 역별로 stop_time 모으기 (방향별로만 검사)
            for name, t_mono, t_raw in zip(stations, mono_times, stop_times):
                station_time_dict.setdefault(name, []).append((train_id, t_mono, t_raw))
        # 2. 모든 열차의 같은 역 stop_time이 3분 이상 겹치지 않는지 (방향별로만 검사)
        for station, arr in station_time_dict.items():
            arr_sorted = sorted(arr, key=lambda x: x[1])  # x[1] = t_mono
            for (tid1, t1, t_raw1), (tid2, t2, t_raw2) in zip(arr_sorted, arr_sorted[1:]):
                if t2 - t1 < 3:
                    raise ValueError()


if __name__ == '__main__':
    try:
        users = User()
        Station()
        Train("downward")
        Train("upward")
    except Exception as e:
        print("\033[31m" + f"파일을 불러오는 데 문제가 발생하였습니다.\n{e}" + "\033[0m")
        sys.exit()

    ticket = Ticket()
    for t in ticket.ticket_data:
        try:
            User(ticket.ticket_data[t]["user_id"])
        except FileNotFoundError:
            print("\033[31m" + "파일을 불러오는 데 문제가 발생하였습니다."
                               "\n데이터 파일 사이에 충돌이 일어났습니다." + "\033[0m")
            sys.exit()

    for uid in users.user_ids:
        booked = User(uid).user_data["booked_list"]
        tickets = ticket.get_ticket_by_user(uid)
        if len(booked) != len(tickets):
            print("\033[31m" + "파일을 불러오는 데 문제가 발생하였습니다."
                               "\n데이터 파일 사이에 충돌이 일어났습니다." + "\033[0m")
            sys.exit()

    try:
        check_train_data_validity(["src/train/downward", "src/train/upward"])
    except Exception as e:
        print("\033[31m" + "파일을 불러오는 데 문제가 발생하였습니다."
                           "\n데이터 파일 사이에 충돌이 일어났습니다." + "\033[0m")
        sys.exit()

    main_menu()
