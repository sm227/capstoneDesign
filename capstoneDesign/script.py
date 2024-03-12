from youtube_transcript_api import YouTubeTranscriptApi
import json

def download_script_json(id):
    video_id = id # 예시 한글 아이디: vDXDAKh8eyo, 영어 아이디: MIgmwSaJ2eo
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en'])
    # 자막 데이터를 JSON 파일로 저장
    with open(f'script_{video_id}.json', 'w', encoding='utf-8') as json_file:
        json.dump(transcript, json_file, ensure_ascii=False, indent=4)
    print(f"자막 데이터가 'script_{video_id}.json' 파일로 저장되었습니다.")

if __name__ == '__main__':
    download_script_json()