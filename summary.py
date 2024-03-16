# single_turn.py
def test1():

    import google.generativeai as genai
    import os
    genai.configure(api_key="AIzaSyB842rnY66Om_-2SwSnh-R98c7v_OWiB9Q")
    model = genai.GenerativeModel('gemini-pro')
    with open("example.txt", "r", encoding='UTF8') as f:
        example = f.read()


    response = model.generate_content(example)
    print(response.text)
test1()
