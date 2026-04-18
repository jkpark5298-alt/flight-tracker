import os
import sys

# 현재 경로를 시스템 경로에 추가하여 임포트 오류 방지
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request
from FlightRadar24 import FlightRadar24API

# 절대 경로를 사용하여 templates 폴더 지정
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

    return render_template('index.html', flight=flight_data, flight_no=flight_no, gate_info=gate_info, error=error_msg)

# Vercel 배포를 위한 핵심: 'app' 객체를 'app'으로 명시
app = app
