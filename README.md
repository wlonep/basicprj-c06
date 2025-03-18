# KTX 예매 프로그램
2025년 1학기 전공기초프로젝트 C06팀

## 환경 셋업
### Python 설치
![image](https://github.com/user-attachments/assets/8370d332-fcf3-4ba0-850d-f393e86de095)

[이 링크](https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe)에서 파이썬을 설치합니다.

설치 중, `Add python.exe to PATH` 부분에 반드시 체크해 주세요.


### PyCharm 설치
[이 링크](https://www.jetbrains.com/pycharm/download/?section=windows)에서 PyCharm Community Edition을 설치합니다.

Community Edition은 스크롤해서 페이지 밑으로 내리면 있습니다.


### GitHub 레포지토리 빌드
![image](https://github.com/user-attachments/assets/e990a0ff-db62-44b4-b851-3e1651328375)

PyCharm 설치 후 프로젝트 선택 화면에서 Get from VCS 버튼을 클릭하고

![image](https://github.com/user-attachments/assets/955396ce-5a43-47ba-8d87-eb42cdd48ca0)
URL 부분에 `https://github.com/wlonep/basicprj-c06.git`을 붙여넣고 프로젝트를 생성합니다.


### 용어의 정의
- 정상적으로 빌드가 된 상태라면 PyCharm 우상단에 사진과 같이 아이콘이 떠 있습니다.
- 좌측부터 각각 fetch, commit, push 역할을 수행합니다.
![image](https://github.com/user-attachments/assets/7f825393-71be-475a-971f-c180559ce8fc)

- Fetch: 여기선 쓸 일이 없습니다.
- Commit(커밋): 파일의 변경사항을 기록합니다.
- Push: 커밋된 변경점을 git 저장소로 업로드합니다.
- Pull: git 저장소에서 변경된 내용을 내 로컬 프로젝트로 받아옵니다.
- Branch: 변경점을 push한 내용을 바탕으로 PR을 작성할 때 사용합니다.
- PR(Pull Request): main branch(코드 원본)와 내 branch(내가 작성한 코드)를 합칠 때 사용합니다.
- Merge: PR이 승인되면 merged 상태가 되고, 내가 작성한 코드가 main branch와 합쳐짐을 의미합니다.

## 주의사항

### 개발 시작 전
![image](https://github.com/user-attachments/assets/232d488c-20cb-4c5c-951c-f4de0622eb5e)

개발 시작 전, **반드시** `Git > Pull`을 클릭해 프로젝트를 Pull해 주세요.

Pull하지 않고 개발을 하면 Merge 시 conflict(한 파일을 각기 다른 사람이 수정하여 충돌이 일어나는 것)가 발생할 수 있습니다.

### 개발 후
![image](https://github.com/user-attachments/assets/7bc06bee-7915-4e70-95ab-269487e21eb3)

파란색 표시한 부분이 main이 아닌지 확인하고, main이라면 branch 이름(아무거나 상관없음)을 입력한 뒤 Push하세요.

# 기능 개발
## 1. FileReader
- 역 정보
- 열차 정보
- 사용자 정보
## 2. 사용자 관리
- 회원가입
- 로그인
- 로그아웃
- 내 예매 정보
- 잔액 충전
## 3. 기차 예매
- 출발지/행선지/날짜/시간 입력
- 조건에 맞는 열차 목록 fetch
- 열차 선택 후 좌석 배치도 표시
- 예매 시 열차 정보와 사용자 정보 파일에 각각 변경점 표시
- 예매 취소
## 4. 관리자 기능
- 열차 편성 추가
- 열차 목록 조회
- 유저 잔액 충전
