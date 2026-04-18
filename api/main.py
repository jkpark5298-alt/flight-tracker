from flask import Flask, render_template_string, request
from FlightRadar24 import FlightRadar24API

app = Flask(__name__)
fr_api = FlightRadar24API()

# HTML 디자인을 변수에 직접 넣어 파일 경로 문제를 해결합니다.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>에어인천 항공기 추적</title>
    <style>
        body { font-family: -apple-system, sans-serif; padding: 20px; background-color: #f4f7f9; color: #333; }
        .container { max-width: 500px; margin: auto; background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h2 { color: #007aff; text-align: center; margin-bottom: 20px; }
        input { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 10px; box-sizing: border-box; font-size: 16px; }
        button { width: 100%; padding: 14px; background: #007aff; color: white; border: none; border-radius: 10px; font-weight: bold; font-size: 16px; cursor: pointer; }
        .result { margin-top: 25px; padding: 15px; background: #f0f8ff; border-radius: 10px; border-left: 5px solid #007aff; }
        .error { color: #ff3b30; font-size: 0.9em; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h2>✈️ 실시간 항공기 조회</h2>
        <form method="POST">
            <input type="text" name="flight_number" placeholder="편명 입력 (예: KJ601)" value="{{ flight_no }}" required>
            <input type="text" name="gate_info" placeholder="주기장 (선택 사항)" value="{{ gate_info }}">
            <button type="submit">지금 조회하기</button>
        </form>

        {% if error %}<p class="error">⚠️ {{ error }}</p>{% endif %}

        {% if flight %}
        <div class="result">
            <p><strong>🔹 편명:</strong> {{ flight.number }}</p>
            <p><strong>🔹 기재 번호:</strong> {{ flight.registration }}</p>
            <p><strong>🔹 현재 기종:</strong> {{ flight.aircraft_code }}</p>
            <p><strong>🔹 운항 구간:</strong> {{ flight.origin_airport_iata }} → {{ flight.destination_airport_iata }}</p>
            {% if gate_info %}<p><strong>🔹 배정 주기장:</strong> {{ gate_info }}</p>{% endif %}
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
                error_msg = f"{flight_no} 편명의 데이터를 찾을 수 없습니다."
        except Exception:
            error_msg = "FlightRadar24 서버 연결에 실패했습니다."

    return render_template_string(HTML_TEMPLATE, flight=flight_data, flight_no=flight_no, gate_info=gate_info, error=error_msg)

# Vercel이 실행할 핸들러 명시
app = app
