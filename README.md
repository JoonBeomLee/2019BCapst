# 2019BCapst

      2019년도 빅데이터 캡스톤 프로젝트 _ 모션인식 기반 헬스케어 프로젝트

      주제 : 영상 분석 기반 Health care 보조 프로그램

      기간 : 2019/08/28 ~ 2019/12/05
      
# 주제 선정 배경
      - 폭발적으로 늘어 나고 있는 '건강한 삶' 에 대한 관심
      
      - 정기적으로 체육관에 다니기 힘든 사람들의 '홈 트레이닝' 에 대한 관심 증가
      
      - 증가한 관심도에 비해 낮은 동기 부여
      
# 프로젝트 목표
      - 모션 인식 홈 트레이닝 프로그램
      
      - 홈 트레이닝 자세 교정, 횟수 카운트 등을 활용한
        동기 부여 및 보조 역할
        
      - 영상 촬영을 통한 횟수 정보 저장 / 데이터 열람을 
        활용한 운동 기록 확인
        
      - 노력의 시각화를 통해 지속적인 동기 부여 효과

# 프로젝트 개요 

      1. 주제 조사 및 선정

      2. 사용될 모듈 검사 및 자료 조사

      3. 개발 환경 조성 및 git_hub 구성

      4. 모듈 적용 및 서버 구축
      
      5. 윈도우 프로그램 

      6. 프로토 타입 생성

      7. 개선 내용 조사 및 버그 체크

      8. 배포 초기판 생성
      
# 프로젝트 진행
      
      1. 프로젝트 초안 발표     (2019-09-04)
      2. 기술 발표             (2019-09-20)
      3. 중간 발표             (2019-10-24)
      4. 진행 발표             (2019-11-20)
      5. 최종 발표             (2019-11-27)
      
# 주제 조사 및 선정 (주제 변경 기간 : 시작 ~ 09/14)
      
      1-1. 운동 영상 분석통한 사용자 Health Care 보조 프로그램


# 사용될 모듈 검사 및 자료 조사

      영상 분석 모듈 조사

            참조 주소 : https://github.com/michalfaber/keras_Realtime_Multi-Person_Pose_Estimation

            a. 모듈 구동 개념 확인

            b. 프로젝트에 적용 방법 확인

            c. 모듈에 사용될 데이터 분석

            d. 적용
                  
 # 시스템 파이프 라인
 ![image](https://user-images.githubusercontent.com/43035696/70235190-c3308100-17a5-11ea-936d-63138c77dc29.png)
 
 # 모듈 설명
 프레임 단위로 모듈을 통한 동작 추출 과정
 ![image](https://user-images.githubusercontent.com/43035696/70235862-22db5c00-17a7-11ea-8bf6-c0dbde6b7560.png)
 
 추출된 동작을 분류 하는 과정
 ![image](https://user-images.githubusercontent.com/43035696/70235970-561deb00-17a7-11ea-821d-7e523fc92e32.png)
 
 누적된 데이터를 시각화 하는 과정
 ![image](https://user-images.githubusercontent.com/43035696/70236018-6fbf3280-17a7-11ea-9dd4-046003657437.png)
 
 # 실제 프로그램 실행 화면
 메인 페이지
 ![image](https://user-images.githubusercontent.com/43035696/71675514-405d0f00-2dc1-11ea-93f9-ff53ae3a0cf9.png)
 로그인을 통해 입장 할 수 있는 화면이며, 프로필 관리, 상단 메뉴 이동, 동영상 시청 등을 할 수 있다.
 
 운동 선택 페이지
 ![image](https://user-images.githubusercontent.com/43035696/71675604-79957f00-2dc1-11ea-8adf-e06c275efc02.png)
 운동 부위에 따른 다양한 운동을 조회 할 수 있고, 수행할 운동을 선택 할 수 있다.
 
 실제 운동 페이지
 ![image](https://user-images.githubusercontent.com/43035696/71675671-a0ec4c00-2dc1-11ea-8156-6de6948cad89.png)
 왼쪽은 연결된 카메라를 통해 운동 동작을 추적 하는 모습.
 오른쪽은 운동 설명 및 모범 영상 그리고 왼쪽에서 추적한 운동 결과에 따른 진행 사항을 보이는 화면 이다.
 
 기록 열람 페이지
 ![image](https://user-images.githubusercontent.com/43035696/71675772-e0b33380-2dc1-11ea-92db-27793d560e4c.png)
 누적된 운동 기록을 시각화 하여 제공하는 화면이다. 
 시각화된 자료를 통해 사용자는 지속적인 운동 동기부여를 다질 수 있다.
 
 게시판 페이지
 ![image](https://user-images.githubusercontent.com/43035696/71675826-06403d00-2dc2-11ea-9fb6-2f00869d290e.png)
 부족한 정보 공유를 위해 게시판을 연결.
 프로그램 내부에서 별도의 익스플로어 없이 실제 사이트를 열람 및 사용 할 수 있다.
