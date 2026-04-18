import os
import boto3
from flask import Flask, render_template, request
from FlightRadar24 import FlightRadar24API

app = Flask(__name__)
fr_api = FlightRadar24API()

def get_rekognition_client():
    return boto3.client(
        'rekognition',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name='ap-northeast-2'
    )

def extract_info(image_bytes):
    try:
        client = get_rekognition_client()
        response = client.detect_text(Image={'Bytes': image_bytes})
        texts = [det['DetectedText'] for det in response['TextDetections'] if det['Type'] == 'LINE']
        
        flight_no = None
        gate = None
        
        for text in texts:
            clean_text = text.replace(" ", "").upper()
            # 항공편명 패턴 인식 (영문+숫자 조합 5자 이상)
            if any(char.isdigit() for char in clean_text) and len(clean_text) >= 5:
                flight_no = clean_text
            if 'GATE' in clean_text or 'SPOT' in clean_text or '주기장' in text:
                gate = text
        return flight_no, gate
    except Exception as e:
        print(f"OCR Error: {e}")
        return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    flight_data = None
    flight_no = request.form.get('flight_number', '').upper()
    gate_info = request.form.get('gate_info', '')
    error_msg = None

    if request.method == 'POST':
        action = request.form.get('action')

        # 사진 업로드 시 자동 인식
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            scanned_no, scanned_gate = extract_info(file.read())
            if scanned_no: flight_no = scanned_no
            if scanned_gate: gate_info = scanned_gate
            if not scanned_no:
                error_msg = "사진에서 편명을 찾지 못했습니다. 직접 수정해주세요."
        
        # 조회 버튼 클릭 시 데이터 호출
        elif action == 'search' and flight_no:
            try:
                flights = fr_api.get_flights()
                for f in flights:
                    if f.number == flight_no:
                        details = fr_api.get_flight_details(f)
                        f.set_flight_details(details)
                        flight_data = f
                        break
                if not flight_data:
                    error_msg = f"{flight_no} 편의 실시간 정보를 찾을 수 없습니다."
            except Exception as e:
                error_msg = "데이터 조회 중 오류가 발생했습니다."

    return render_template('index.html', flight=flight_data, flight_no=flight_no, gate_info=gate_info, error=error_msg)

if __name__ == "__main__":
    app.run()
