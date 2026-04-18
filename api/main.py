from flask import Flask, render_template_string, request
from pyFlightRadar24 import FlightRadar24API

app = Flask(__name__)
fr_api = FlightRadar24API()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>에어인천 추적기</title>
    <style>
        body { font-family: -apple-system, sans-serif; padding: 20px; background: #f2f2f7; }
        .card { max-width: 450px; margin: auto; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #007aff; color: white; border: none; border-radius: 8px; font-weight: bold; }
        .res { margin-top: 15px; padding: 10px; background: #f0f8ff; border-radius: 8px; border-left: 4px solid #007aff; }
    </style>
</head>
<body>
    <div class="card">
        <h3>✈️ 실시간 항공기 조회</h3>
        <form method="POST">
            <input type="text" name="fn" placeholder="편명 (KJ601)" value="{{ fn }}" required>
            <input type="text" name="gt" placeholder="주기장 (선택)" value="{{ gt }}">
            <button type="submit">조회</button>
        </form>
        {% if err %}<p style="color:red; font-size:14px;">{{ err }}</p>{% endif %}
        {% if f %}
        <div class="res">
            <p>✈️ <b>기재:</b> {{ f.registration }} ({{ f.aircraft_code }})</p>
            <p>📍 <b>구간:</b> {{ f.origin_airport_iata }} → {{ f.destination_airport_iata }}</p>
            {% if gt %}<p>🅿️ <b>주기장:</b> {{ gt }}</p>{% endif %}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    f_data, fn, gt, err = None, '', '', None
    if request.method == 'POST':
        fn = request.form.get('fn', '').upper().strip()
        gt = request.form.get('gt', '')
        try:
            flights = fr_api.get_flights()
            for fl in flights:
                if fl.number == fn:
                    f_data = fl
                    break
            if not f_data: err = "비행 정보를 찾을 수 없습니다."
        except: err = "데이터 연결 실패"
    return render_template_string(HTML_TEMPLATE, f=f_data, fn=fn, gt=gt, err=err)

app = app
