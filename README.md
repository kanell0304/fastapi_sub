4팀 FastAPI 과제

주제: 도서관 관리 시스템

테이블 구조:
Users (회원/사서)
Books (도서)
Authors (저자)
Loans (대출 기록)
Reservations (예약)

주요 기능:
회원/사서 권한 분리 (OAuth/JWT)
도서 검색 및 관리
대출/반납 시스템
도서 예약 기능
연체 관리

API 예시:
GET /books?author=홍길동&available=true (쿼리 매개변수)
POST /loans (Request Body로 대출 정보)
PUT /loans/{loan_id}/return (경로 매개변수)

-역할 분담-
- 손연서 - oAuth, jwt
- 함현준 - DB 테이블 작성, Pydantic 모델링
- 차영준 - DB 테이블 작성, Pydantic 모델링
- 이경준 - API작성, api명세서


-2차 역할 분담-
1. Users테이블 + API(CRUD) + JWT토큰인증(oAuth)
2. 테이블 1개 + API(CRUD) + DATABASE Setting(DATABASE 생성 및 연결)
3. 테이블 1개 + API(CRUD) + API명세서 작성
4. 테이블 2개 + API(CRUD)

- CRUD = 생성(추가), 전체조회, 특정ID 조회 수정(특정 ID), 삭제(특정 ID)