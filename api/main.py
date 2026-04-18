import os
from flask import Flask, render_template, request
from FlightRadar24 import FlightRadar24API

# templates 폴더 위치를 Flask에게 명확히 알려줍니다.
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
                # 전체 항공기 목록 중 해당 편명 검색
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
                error_msg = "조회 중 오류가 발생했습니다."

    return render_template('index.html', 
                           flight=flight_data, 
                           flight_no=flight_no, 
                           gate_info=gate_info, 
                           error=error_msg)

# Vercel 실행을 위한 필수 핸들러 설정
app = app
