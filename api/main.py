from flask import Flask, render_template_string, request
from pyFlightRadar24 import FlightRadar24API

app = Flask(__name__)
fr_api = FlightRadar24API()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>에어인천 항공기 추적</title>
    <style>
        body { font-family: -apple-system, sans-serif; padding: 20px; background-color: #f2f2f7; }
        .container { max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        h2 { color: #007aff; text-align: center; }
        input { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 10px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #007aff; color: white; border: none; border-radius: 10px; font-weight: bold; width: 100%; cursor: pointer; }
        .result { margin-top: 20px; padding: 15px; background: #f0f8ff; border-radius: 10px; border-left: 5px solid #007aff; }
    </style>
</head>
<body>
    <div class="container">
        <h2>✈️ 실시간 항공기 조회</h2>
        <form method="POST">
            <input type="text" name="f_no" placeholder="편명 입력 (예: KJ601)" value="{{ f_no }}" required>
            <input type="text" name="gate" placeholder="주기장 정보 (선택)" value="{{ gate }}">
            <button type="submit">조회하기</button>
        </form>
        {% if error %}<p style="color:red; text-align:center;">{{ error }}</p>{% endif %}
        {% if flight %}
        <div class="result">
            <p><strong>편명:</strong> {{ flight.number }}</p>
            <p><strong>기재 번호:</strong> {{ flight.registration }}</p>
            <p><strong>기종:</strong> {{ flight.aircraft_code }}</p>
            <p><strong>구간:</strong> {{ flight.origin_airport_iata }} → {{ flight.destination_airport_iata }}</p>
            {% if gate %}<p><strong>주기장:</strong> {{ gate }}</p>{% endif %}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    flight_data, f_no, gate, error_msg = None, '', '', None
    if request.method == 'POST':
        f_no = request.form.get('f_no', '').upper().strip()
        gate = request.form.get('gate', '')
        try:
            flights = fr_api.get_flights()
            for f in flights:
                if f.number == f_no:
                    flight_data = f
                    break
            if not flight_data:
                error_msg = f"{f_no}를 찾을 수 없습니다."
        except:
            error_msg = "데이터 호출 중 오류 발생"
    return render_template_string(HTML_TEMPLATE, flight=flight_data, f_no=f_no, gate=gate, error=error_msg)

# Vercel용 핸들러
app = app
