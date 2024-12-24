# Youtube_restapi

## (1) Project Settings

- Github

## Model 구조 => ORM

(1) User => users
- email
- password
- nickname
- is_business

(2) Video => videos
- title
- description
- link
- views_count
- thumbnail
- video_file

ex) 파일 (이미지, 동영상)
=> 장고에 부하가 걸림
=> S3 Bucket (저렴, 속도가 빠름) -> 결과물: 링크

(3) Reaction => reactions
- User: FK
- Video: FK
- reaction (like, dislike, cancel) => 실제 youtube rest api

(4) Comment => comments
- User: FK
- Video: FK
- content
- like
- dislike

(5) Subscription => subscriptions
- User: FK => subscriber (내가 구독한 사람)
- User: FK => subscribed_to (나를 구독한 사람)

(6) Common => common
- created_at
- updated_at

-----------------

### Docker 란??
애플리케이션을 신속하게 구축, 테스트 및 배포 할 수 있는 소프트웨어 플랫폼
### Docker 구성요소
- 도커 이미지
- 도커 컨테이너
- 도커 엔진 : 호스트 OS 위에 설치되며, 도커 CLI를 통해 명령을 받아서 실행
- 도커 허브 : 도커 이미지를 저장하고 공유하는 레지스트리, 도커 허브를 통해 공개된 이미지를 다른사람과 공유할 수 있음

### Docker Image 와 Docker Container
- 도커 이미지 : 컨테이너를 생성하기 위한 템플릿이고, 도커 파일을 통해 생성할 수 있음
    애플리케이션과 그 종속성을 포함하고 있으며, 여러 레이어로 구성되어 있음

- 도커 컨테이너 : 도커 이미지를 실행한 상태로 독립된 환경에서 애플리케이션을 실행하며, 필요한 자원은 호스트 OS 와 공유
    일관된 실행 환경을 제공하여 개발과 운영 간의 차이를 줄여줌

### CI / CD
- CI (Continuous Integration)
    빌드와 테스트 자동화

- CD (Continuous Delivery)
    배포 자동화, CI 과정 이후 -> 버그테스트 -> staging 릴리즈 -> production 배포 하는 과정

### Github Actions
    빌드, 테스트 및 배포 파이프라인을 자동화할 수 있는 지속적인 통합 및 지속적인 배포(CI/CD) 플랫폼
    레포지토리에 대한 모든 풀 리퀘스트를 빌드하고 테스트하거나, 병합된 풀 리퀘스트를 프로덕션에 배포하는 워크플로를 만들 수 있음

### PostgreSQL 의 장점
1) 관계형 DB 중에서 최다 SQL 기능을 지원
2) 다양한 데이터 유형 지원
3) 프로그래밍 언어 지원
4) 대량 데이터 처리