import os
from flask import Flask, render_template, request
from FlightRadar24 import FlightRadar24API

# 이 코드가 박종규님의 현재 GitHub 구조(api와 templates가 나란히 있는 구조)에 딱 맞습니다.
app = Flask(__name__, template_folder='../templates')
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
                # 실시간 항공기 데이터 조회
                flights = fr_api.get_flights()
                for f in flights:
                    if f.number == flight_no:
                        details = fr_api.get_flight_details(f)
                        f.set_flight_details(details)
                        flight_data = f
                        break
                if not flight_data:
                    error_msg = f"{flight_no} 편의 정보를 찾을 수 없습니다."
            except Exception as e:
                error_msg = f"조회 중 오류 발생: {str(e)}"

    return render_template('index.html', flight=flight_data, flight_no=flight_no, gate_info=gate_info, error=error_msg)

# Vercel은 이 변수를 찾아 서버를 실행합니다.
app = app
