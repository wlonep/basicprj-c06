import os
import openpyxl
from datetime import datetime


def calculate_fee(start_time, end_time):
    """
    기본 운임 계산 함수
    수식: 운행시간(분) * 250
    """
    try:
        start = datetime.strptime(start_time, "%H%M")
        end = datetime.strptime(end_time, "%H%M")
        duration = (end - start).seconds / 60  # 분 단위 변환
        return int(duration * 250)
    except:
        return 10000  # 기본값


def main(sheet_data, header, dir_path):
    for row in sheet_data:
        train_id = row[0].value
        # train_type = row[1].value.replace('KTX-', '')
        # if train_type == "산천":
        #     car_count = 8
        #     seat_count = 363
        # elif train_type == "청룡":
        #     car_count = 8
        #     seat_count = 515
        # else:
        #     train_type = 'A'
        #     car_count = 18
        #     seat_count = 935

        stations = []
        stop_time = []
        cell_count = 0
        # if row[20].value == "매일":
        #     operation = "월,화,수,목,금,토,일"
        # else:
        #     operation = ','.join(list(row[20].value))
        for cell in row[2:]:
            if cell.value.strftime("%H%M") == "0000":
                pass
            else:
                stations.append(header[0][cell_count].value.replace('(오대산)', ''))
                stop_time.append(cell.value.strftime("%H%M"))
            cell_count += 1

        train_data = f"""TRAIN_ID={train_id}
STATION={','.join(stations)}
STOP_TIME={','.join(stop_time)}
FEE={calculate_fee(stop_time[0], stop_time[-1])}
BASE_FEE=7000
BOOKED="""
        file_path = os.path.join(dir_path, f"KTX-{train_id}.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(train_data)


wb = openpyxl.load_workbook("train_data.xlsx")

# 경부선
# sheet = wb["경부선"]
# downward_sheet = sheet['B11':'U82']
# downward_header = sheet['D8':'U8']
# downward_dir = './train/downward'
# upward_sheet = sheet['X11':'AQ86']
# upward_header = sheet['Z8':'AQ8']
# upward_dir = './train/upward'

# 강릉선
# sheet = wb["강릉선"]
# downward_sheet = sheet['B11':'S41']
# downward_header = sheet['D8':'S8']
# downward_dir = './train/downward'
# upward_sheet = sheet['V11':'AM41']
# upward_header = sheet['X8':'AM8']
# upward_dir = './train/upward'

# 중앙선
sheet = wb["중앙선"]
downward_sheet = sheet['B11':'S19']
downward_header = sheet['D8':'S8']
downward_dir = './train/downward'
upward_sheet = sheet['V11':'AM19']
upward_header = sheet['X8':'AM8']
upward_dir = './train/upward'

if not os.path.exists(upward_dir):
    os.makedirs(upward_dir)
if not os.path.exists(downward_dir):
    os.makedirs(downward_dir)

main(upward_sheet, upward_header, upward_dir)
main(downward_sheet, downward_header, downward_dir)
