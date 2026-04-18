import os
from flask import Flask, render_template, request
from FlightRadar24 import FlightRadar24API

# Vercel 서버리스 환경에서 templates 폴더 위치를 절대 경로로 추적합니다.
# 현재 파일(main.py) 위치에서 한 단계 위로 올라가 templates 폴더를 찾습니다.
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, "..", "templates")

app = Flask(__name__, template_folder=template_path)
fr_api = FlightRadar24API()

@app.route('/', methods=['GET', 'POST'])
def index():
    flight_data = None
    flight_no = request.form.get('flight_number', '').upper().strip()
    gate_info = request.form.get('gate_info', '')
    error_msg = None

    if request.method == 'POST':
        if flight_no:
            try:
                # 실시간 항공 데이터 조회
                flights = fr_api.get_flights()
                for f in flights:
                    if f.number == flight_no:
                        details = fr_api.get_flight_details(f)
                        f.set_flight_details(details)
                        flight_data = f
                        break
                
                if not flight_data:
                    error_msg = f"{flight_no} 정보를 찾을 수 없습니다."
            except Exception as e:
                # 에러 발생 시 상세 메시지 출력 (디버깅용)
                error_msg = "데이터 조회 중 오류가 발생했습니다."

    return render_template('index.html', 
                           flight=flight_data, 
                           flight_no=flight_no, 
                           gate_info=gate_info, 
                           error=error_msg)

# Vercel이 Flask 앱을 인식하도록 설정
app = app
