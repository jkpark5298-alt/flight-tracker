from flask import Flask, render_template_string, request
from FlightRadar24 import FlightRadar24API
import os

app = Flask(__name__)
fr_api = FlightRadar24API()

# HTML 디자인을 파일이 아닌 변수로 직접 관리 (파일 경로 문제 해결)
HTML_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <title>에어인천 항공기 추적</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: -apple-system, sans-serif; padding: 20px; background-color: #f4f4f9; }
        .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #007aff; color: white; border: none; border-radius: 8px; font-weight: bold; }
        .result { margin-top: 20px; padding: 15px; background: #e9f5ff; border-radius: 8px; }
        .error { color: #ff3b30; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>✈️ 항공기 실시간 조회</h2>
        <form method="POST">
            <input type="text" name="flight_number" placeholder="편명 입력 (예: KJ601)" value="{{ flight_no }}" required>
            <input type="text" name="gate_info" placeholder="주기장 (선택)" value="{{ gate_info }}">
            <button type="submit">조회하기</button>
        </form>

        {% if error %}<p class="error">{{ error }}</p>{% endif %}

        {% if flight %}
        <div class="result">
            <p><strong>편명:</strong> {{ flight.number }}</p>
            <p><strong>기재 번호:</strong> {{ flight.registration }}</p>
            <p><strong>기종:</strong> {{ flight.aircraft_code }}</p>
            <p><strong>현재 구간:</strong> {{ flight.origin_airport_iata }} → {{ flight.destination_airport_iata }}</p>
            {% if gate_info %}<p><strong>주기장:</strong> {{ gate_info }}</p>{% endif %}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    flight_data = None
    flight_no = request.form.get('flight_number', '').upper().strip()
    gate_info = request.form.get('gate_info', '')
    error_msg = None

    if request.method == 'POST' and flight_no:
        try:
            flights = fr_api.get_flights()
            for f in flights:
                if f.number == flight_no:
                    details = fr_api.get_flight_details(f)
                    f.set_flight_details(details)
                    flight_data = f
                    break
            if not flight_data:
                error_msg = f"{flight_no} 편명을 현재 찾을 수 없습니다."
        except:
            error_msg = "데이터 서버 연결 중 오류가 발생했습니다."

    return render_template_string(HTML_LAYOUT, flight=flight_data, flight_no=flight_no, gate_info=gate_info, error=error_msg)

# Vercel이 인식할 수 있도록 객체 노출
app = app
