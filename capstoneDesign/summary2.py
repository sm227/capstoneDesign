import json
import requests

# OpenAI API를 사용하기 위한 설정
api_url = "https://api.openai.com/v1/completions"
api_key = "YOUR_API_KEY_HERE"  # 여기에 OpenAI API Key를 입력하세요.
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# JSON 데이터를 로드. 실제 사용에서는 파일 경로나 웹 요청 등 다양한 방법으로 데이터를 얻을 수 있습니다.
json_data = {
    "item": {
        "text": "여기에 요약하고 싶은 긴 텍스트를 넣으세요."
    }
}

# JSON 데이터에서 텍스트 추출
text_to_summarize = json_data['item']['text']

# 요약을 위한 프롬프트 설정
prompt = f"요약: {text_to_summarize}"

# GPT-3 요청 데이터 구성
data = {
    "model": "text-davinci-003",  # 사용할 모델을 지정하세요. 모델 버전은 사용 가능한 최신 버전으로 업데이트해야 할 수 있습니다.
    "prompt": prompt,
    "temperature": 0.7,
    "max_tokens": 150
}

# GPT-3 API 요청
response = requests.post(api_url, headers=headers, json=data)

# 요청 결과 확인
if response.status_code == 200:
    response_data = response.json()
    summary = response_data['choices'][0]['text'].strip()
    print("원본 텍스트:", text_to_summarize)
    print("요약된 텍스트:", summary)
else:
    print("요청에 실패했습니다. 상태 코드:", response.status_code)
