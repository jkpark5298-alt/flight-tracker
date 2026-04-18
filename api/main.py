import os
from flask import Flask, render_template, request
from FlightRadar24 import FlightRadar24API

# 경로 설정
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
            except Exception:
                error_msg = "조회 중 오류가 발생했습니다."

    return render_template('index.html', flight=flight_data, flight_no=flight_no, gate_info=gate_info, error=error_msg)

# Vercel이 이 파일을 읽어서 실행할 때 'app' 변수를 찾도록 합니다.
# 파일 끝에 아래 한 줄이 꼭 있어야 합니다.
app = app
