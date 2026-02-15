# ChatGPT Pro 결제자 지침서 (다운로드 안내)

이 저장소에는 최종 PDF 지침서가 포함되어 있습니다.

## 바로 다운로드할 파일

- `CHATGPT_PRO_결제자_지침서.pdf`
- `ChatGPT_PRO_Guide_KR.pdf` (영문 파일명 버전)

## 웹페이지에서 바로 받는 링크 (GitHub)

> 상대경로 링크는 **GitHub 저장소 페이지 안에서** 눌렀을 때 정상 동작합니다.
> 채팅창처럼 저장소 컨텍스트가 없는 곳에서는 `Invalid URL`이 날 수 있습니다.

### 1) 파일 열기 링크 (README 내부에서 클릭)
- [CHATGPT_PRO_결제자_지침서.pdf](./CHATGPT_PRO_결제자_지침서.pdf)
- [ChatGPT_PRO_Guide_KR.pdf](./ChatGPT_PRO_Guide_KR.pdf)

### 2) 바로 다운로드 링크 (README 내부에서 클릭)
- [CHATGPT_PRO_결제자_지침서.pdf 다운로드](./CHATGPT_PRO_결제자_지침서.pdf?raw=1)
- [ChatGPT_PRO_Guide_KR.pdf 다운로드](./ChatGPT_PRO_Guide_KR.pdf?raw=1)

### 3) 절대 URL 예시 (채팅창/메신저에서 클릭할 때)
- `https://github.com/<OWNER>/<REPO>/blob/<BRANCH>/ChatGPT_PRO_Guide_KR.pdf`
- `https://raw.githubusercontent.com/<OWNER>/<REPO>/<BRANCH>/ChatGPT_PRO_Guide_KR.pdf`

## GitHub에서 수동으로 다운로드하는 방법

1. 저장소의 `README.md` 페이지로 이동
2. 위 링크 중 하나를 클릭
3. 파일 페이지에서 우측 상단의 **Download raw file** 버튼 클릭

또는 저장소 메인에서 **Code → Download ZIP**으로 전체 파일을 내려받을 수 있습니다.

## GitHub에 커밋/푸시 되었는지 확인하는 방법 (Windows)

사용자 로컬 경로가 `C:/Users/ms/Downloads/JI100880`인 경우, PowerShell에서 아래 순서로 확인합니다.

```powershell
cd C:/Users/ms/Downloads/JI100880

git remote -v
git branch --show-current
git status
git log --oneline -n 5
git fetch origin
git status -sb
```

확인 포인트:
- `git remote -v`에 GitHub 주소가 보여야 합니다.
- `git status`가 `nothing to commit, working tree clean`이면 로컬 변경사항은 커밋 완료 상태입니다.
- `git status -sb`에서 `ahead 1`처럼 보이면 **로컬 커밋은 되었지만 아직 push 전** 상태입니다.
- push는 아래 명령으로 진행합니다.

```powershell
git push origin <현재브랜치명>
```

## 재생성 방법(선택)

PDF를 다시 생성하려면 아래 명령을 실행하세요.

```bash
python generate_pdf.py
```
