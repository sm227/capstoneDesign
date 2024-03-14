from django.shortcuts import render
import openai

# OpenAI API 키 설정
openai.api_key = 'YOUR_API_KEY'

def summarize_text(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text', '')
        summary = summarize(input_text)
        return render(request, 'summary.html', {'input_text': input_text, 'summary': summary})
    return render(request, 'index.html')

def summarize(input_text):
    # GPT 모델 및 엔진 설정
    model = "text-davinci-003"

    # 요약할 문장 및 추가적인 정보
    prompt = f"요약해줘: {input_text}"

    # GPT 요약 생성 요청
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=100,  # 요약의 최대 길이
        temperature=0.5,  # 창의성 조절
        top_p=1.0,  # 선택 확률에 대한 상한선
        n=1  # 생성할 요약의 수
    )

    # 생성된 요약 반환
    summary = response.choices[0].text.strip()
    return summary
