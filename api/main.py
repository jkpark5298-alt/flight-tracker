from flask import Flask, render_template_string, request
from FlightRadar24 import FlightRadar24API

app = Flask(__name__)
fr_api = FlightRadar24API()

# HTML 디자인을 변수에 담아 직접 사용 (파일 경로 문제 해결)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>에어인천 항공기 조회</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; padding: 20px; line-height: 1.6; }
        input { padding: 10px; width: 80%; margin-bottom: 10px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        .result { margin-top: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .error { color: red; }
    </style>
</head>
<body>
    <h2>에어인천 항공기 점검 조회</h2>
    <form method="POST">
        <input type="text" name="flight_number" placeholder="편명 입력 (예: KJ601)" value="{{ flight_no }}">
        <input type="text" name="gate_info" placeholder="주기장 정보 (선택)" value="{{ gate_info }}">
        <button type="submit">조회하기</button>
    </form>

    {% if error %}<p class="error">{{ error }}</p>{% endif %}

    {% if flight %}
    <div class="result">
        <h3>✈️ 조회 결과 ({{ flight.number }})</h3>
        <p><strong>기재 번호:</strong> {{ flight.registration }}</p>
        <p><strong>출발지:</strong> {{ flight.origin_airport_iata }}</p>
        <p><strong>도착지:</strong> {{ flight.destination_airport_iata }}</p>
        <p><strong>기종:</strong> {{ flight.aircraft_code }}</p>
        {% if gate_info %}<p><strong>지정 주기장:</strong> {{ gate_info }}</p>{% endif %}
    </div>
    {% endif %}
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
                error_msg = f"{flight_no} 편명을 찾을 수 없습니다."
        except Exception:
            error_msg = "조회 중 오류가 발생했습니다."

    return render_template_string(HTML_TEMPLATE, flight=flight_data, flight_no=flight_no, gate_info=gate_info, error=error_msg)

# Vercel용 핸들러
app = app
