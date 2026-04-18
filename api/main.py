import os
from flask import Flask, render_template, request
from FlightRadar24 import FlightRadar24API

# api 폴더 외부에 있는 templates 폴더를 인식하도록 설정
app = Flask(__name__, template_folder="../templates")
fr_api = FlightRadar24API()

@app.route('/', methods=['GET', 'POST'])
def index():
    flight_data = None
    flight_no = request.form.get('flight_number', '').upper()
    gate_info = request.form.get('gate_info', '')
    error_msg = None

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'search' and flight_no:
            try:
                # 실시간 항공기 목록 가져오기
                flights = fr_api.get_flights()
                for f in flights:
                    if f.number == flight_no:
                        details = fr_api.get_flight_details(f)
                        f.set_flight_details(details)
                        flight_data = f
                        break
                if not flight_data:
                    error_msg = f"{flight_no} 편의 실시간 정보를 찾을 수 없습니다."
            except Exception:
                error_msg = "데이터 조회 중 오류가 발생했습니다."

    return render_template('index.html', flight=flight_data, flight_no=flight_no, gate_info=gate_info, error=error_msg)

# Vercel이 파이썬 앱을 실행하기 위한 핸들러
def handler(request):
    return app(request)
