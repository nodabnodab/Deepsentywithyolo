import os
import firebase_admin
from firebase_admin import credentials, firestore
import requests  # 영상 다운로드를 위한 라이브러리

# --- 설정 ---
# 기존 업로드 스크립트와 동일한 키 파일 경로를 사용합니다.
FIREBASE_CREDENTIAL_PATH = r'C:\Users\AREU\Desktop\PolyProject\databaseuploading\fkey\animaldetection-b3cc8-firebase-adminsdk-fbsvc-09d686d3fd.json'

# 다운로드한 영상을 저장할 폴더 이름
DOWNLOAD_DIR = "firebase_downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# 가져올 최근 기록의 개수
LIMIT = 3

# --- Firebase Admin 초기화 ---
# 스크립트가 여러 개이므로, 고유한 앱 이름으로 초기화하는 것이 좋습니다.
APP_NAME_DOWNLOADER = 'FirebaseDownloader'
try:
    try:
        firebase_admin.get_app(name=APP_NAME_DOWNLOADER)
    except ValueError:
        cred = credentials.Certificate(FIREBASE_CREDENTIAL_PATH)
        firebase_admin.initialize_app(cred, name=APP_NAME_DOWNLOADER)
    
    db = firestore.client(app=firebase_admin.get_app(name=APP_NAME_DOWNLOADER))
    print("✅ Firebase에 성공적으로 연결되었습니다.")

except Exception as e:
    print(f"❌ Firebase 초기화 실패: {e}")
    exit()

# --- 메인 로직 ---
print(f"\n▶️ Firestore에서 가장 최근 탐지 기록 {LIMIT}개를 가져옵니다...")
print("-" * 50)

try:
    # 'LogRecord' 컬렉션에서 날짜(DetDate)와 시간(DetTime)을 기준으로 내림차순 정렬하여 최신순으로 만듭니다.
    query = db.collection("LogRecord") \
              .order_by("DetDate", direction=firestore.Query.DESCENDING) \
              .order_by("DetTime", direction=firestore.Query.DESCENDING) \
              .limit(LIMIT)

    docs = query.stream()

    count = 0
    for doc in docs:
        count += 1
        log_data = doc.to_dict()
        
        # --- 1. Firestore에서 가져온 메타데이터 출력 ---
        print(f"📄 기록 #{count} (ID: {doc.id})")
        print(f"  - 동물: {log_data.get('DetAnimal', 'N/A')}")
        print(f"  - 날짜/시간: {log_data.get('DetDate', '')} {log_data.get('DetTime', '')}")
        print(f"  - 위치: {log_data.get('DetLocation', 'N/A')}")
        
        video_url = log_data.get("VideoUrl")
        if not video_url:
            print("  - 영상 URL 없음. 건너뜁니다.")
            print("-" * 50)
            continue
            
        # --- 2. VideoUrl을 사용해 영상 다운로드 ---
        print("  - 영상 다운로드 중...")
        try:
            response = requests.get(video_url, stream=True)
            
            # 응답이 정상적인지 확인 (200 OK)
            if response.status_code == 200:
                # 파일 이름 만들기 (예: 2025-06-10_163057_human.mp4)
                # 파일명에 ':' 문자는 사용할 수 없으므로 제거합니다.
                time_str_for_file = log_data.get('DetTime', '').replace(':', '')
                filename = f"{log_data.get('DetDate')}_{time_str_for_file}_{log_data.get('DetAnimal')}.mp4"
                filepath = os.path.join(DOWNLOAD_DIR, filename)

                # 파일 저장
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"  ✅ 다운로드 성공! -> '{filepath}'")

            else:
                print(f"  ❌ 다운로드 실패. HTTP 상태 코드: {response.status_code}")

        except Exception as e:
            print(f"  ❌ 영상 다운로드 중 오류 발생: {e}")

        print("-" * 50)

    if count == 0:
        print("Firestore 'LogRecord' 컬렉션에서 탐지 기록을 찾을 수 없습니다.")

except Exception as e:
    print(f"Firestore 쿼리 중 오류 발생: {e}")