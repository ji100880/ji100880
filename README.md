# PDF → PPT 변환 API

PDF 파일을 업로드하면 각 페이지를 이미지로 렌더링한 뒤, 페이지별 슬라이드로 구성된 PPTX를 반환하는 FastAPI 예제입니다.

## 설치

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 실행

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## API

### `GET /health`
서버 상태 확인

### `POST /convert/pdf-to-ppt`
- form-data 키: `file` (PDF)
- 응답: 변환된 `.pptx` 파일 다운로드

예시:

```bash
curl -X POST "http://localhost:8000/convert/pdf-to-ppt" \
  -F "file=@sample.pdf" \
  --output converted.pptx
```
