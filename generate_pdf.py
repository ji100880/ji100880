from pathlib import Path

W, H = 595, 842


def utf16_hex(s: str) -> str:
    return s.encode('utf-16-be').hex().upper()


def text_cmd(x, y, size, text):
    return f"BT /F1 {size} Tf 1 0 0 1 {x} {y} Tm <{utf16_hex(text)}> Tj ET\n"


def rect_cmd(x, y, w, h, fill_rgb=None, stroke_rgb=None, lw=1):
    cmd = ""
    if fill_rgb:
        cmd += f"{fill_rgb[0]} {fill_rgb[1]} {fill_rgb[2]} rg\n"
    if stroke_rgb:
        cmd += f"{stroke_rgb[0]} {stroke_rgb[1]} {stroke_rgb[2]} RG\n{lw} w\n"
    op = 'B' if fill_rgb and stroke_rgb else ('f' if fill_rgb else 'S')
    cmd += f"{x} {y} {w} {h} re {op}\n"
    return cmd

pages = []

# Page 1 cover
c = ""
c += rect_cmd(0, 0, W, H, fill_rgb=(0.04, 0.18, 0.39))
c += rect_cmd(30, 760, 180, 24, fill_rgb=(0.12,0.35,0.72), stroke_rgb=(0.7,0.85,1), lw=0.8)
c += text_cmd(38, 768, 10, "2026 실전 가이드 · 초보자용")
c += text_cmd(42, 670, 34, "ChatGPT Pro")
c += text_cmd(42, 625, 34, "결제자 지침서")
c += text_cmd(42, 575, 16, "일반 모드와 PRO의 차이부터")
c += text_cmd(42, 550, 16, "초보자를 위한 디테일 사용법까지")
c += text_cmd(42, 70, 12, "작성: AI 활용 실무 가이드")
pages.append(c)

# Page 2 differences
c = ""
c += rect_cmd(24, 790, 6, 24, fill_rgb=(0.18,0.5,0.98))
c += text_cmd(36, 796, 20, "1. 일반 모드 vs PRO 모드 핵심 차이")
c += rect_cmd(24, 738, 547, 40, fill_rgb=(0.94,0.97,1), stroke_rgb=(0.75,0.84,1), lw=0.7)
c += text_cmd(34, 752, 11, "초보자 기준: 결과물 완성도, 혼잡 시간 안정성, 긴 작업 유지력에서 차이가 큽니다.")
# table
start_y=690
row_h=64
cols=[24,100,230,370,571]
for r in range(5):
    y=start_y-r*row_h
    c+=rect_cmd(24,y-row_h,547,row_h,stroke_rgb=(0.75,0.84,1),lw=0.7)
for x in cols[1:-1]:
    c+=f"{0.75} {0.84} {1} RG 0.7 w {x} {start_y-5*row_h} m {x} {start_y} l S\n"
headers=["구분","일반","PRO","체감 포인트"]
for i,h in enumerate(headers):
    c+=text_cmd(cols[i]+6,start_y-22,11,h)
rows=[
("응답 품질","기본 수준","정교한 추론","보고서 완성도 향상"),
("혼잡 시간대","지연 가능","상대적 안정","마감 직전 유리"),
("고급 기능","일부 제한","넓은 접근","복합 작업 가능"),
("맥락 유지","이탈 가능","긴 대화 안정","반복 수정 시간 절약"),
]
for r,row in enumerate(rows, start=1):
    yy=start_y-r*row_h-22
    for i,t in enumerate(row):
        c+=text_cmd(cols[i]+6,yy,10,t)
# mini chart blocks
c+=text_cmd(24,120,14,"도표: 일반 vs PRO 효율 비교")
for i,label in enumerate(["정확도","속도 안정","복합작업","결과 완성"]):
    y=90-i*20
    c+=text_cmd(28,y,9,label)
    c+=rect_cmd(90,y-4,120+i*8,8,fill_rgb=(0.72,0.82,0.97))
    c+=rect_cmd(230,y-4,210+i*12,8,fill_rgb=(0.18,0.5,0.98))
pages.append(c)

# Page 3 tips
c=""
c+=rect_cmd(24,790,6,24,fill_rgb=(0.18,0.5,0.98))
c+=text_cmd(36,796,20,"2. PRO 모드 사용 시 좋은 점")
for i,(title,body) in enumerate([
("① 결과물 품질 향상","목차·핵심 메시지·실행안까지 구조화된 출력"),
("② 반복 작업 자동화","메일·회의록·SNS 초안 생성 시간을 단축"),
("③ 복합 요청 처리","요약 + 표 + 대본 + 체크리스트 동시 생성"),
("④ 실수 감소","형식 누락, 톤 불일치, 항목 빠짐을 감소"),
]):
    y=720-i*92
    c+=rect_cmd(24,y-70,547,80,fill_rgb=(0.97,0.99,1),stroke_rgb=(0.79,0.87,1),lw=0.7)
    c+=text_cmd(36,y-20,13,title)
    c+=text_cmd(36,y-44,11,body)

c+=text_cmd(24,320,16,"초보자 필수 프롬프트 공식")
for i,t in enumerate([
"1) 역할 지정: 너는 7년차 실무자다.",
"2) 결과 형식 지정: 표 + 핵심 5줄 + 실행 일정.",
"3) 제약 조건: 쉬운 한국어, 분량 제한.",
"4) 검증 요청: 누락 항목 자체점검표 추가.",
]):
    c+=text_cmd(36,290-i*24,11,t)

c+=text_cmd(24,168,14,"워크플로우 도표")
steps=["목표설정","역할부여","초안생성","품질점검","최종본"]
for i,s in enumerate(steps):
    x=36+i*108
    c+=rect_cmd(x,118,96,30,fill_rgb=(0.85,0.92,1),stroke_rgb=(0.18,0.5,0.98),lw=0.8)
    c+=text_cmd(x+16,129,10,s)
pages.append(c)

# Page4
c=""
c+=rect_cmd(24,790,6,24,fill_rgb=(0.18,0.5,0.98))
c+=text_cmd(36,796,20,"3. 이외 반드시 알아야 할 기능")
c+=text_cmd(24,748,13,"A. 프로젝트형 대화 관리")
for i,t in enumerate([
"- 주제별 대화방 분리로 맥락 오염 방지",
"- 첫 메시지에 목표/대상/톤/금지사항 명시",
"- 중간 결과는 v1, v2 버전으로 고정",
]):
    c+=text_cmd(34,724-i*22,11,t)
c+=text_cmd(24,640,13,"B. 품질을 높이는 디테일")
for i,t in enumerate([
"- Before/After 교정 요청으로 문장 완성도 향상",
"- 정확성/명확성/실행성/톤 기준으로 자체평가",
"- 1차-2차-최종본 3단계 재작성 루프",
]):
    c+=text_cmd(34,616-i*22,11,t)
c+=text_cmd(24,532,13,"C. 실수 방지 체크리스트")
for i,t in enumerate([
"1) 독자 레벨(초급/중급/전문가) 지정",
"2) 분량과 형식(표/불릿/문단) 명시",
"3) 금지사항(과장 표현 금지 등) 작성",
"4) 최종 오탈자/중복/누락 점검 요청",
]):
    c+=text_cmd(34,508-i*22,11,t)
c+=rect_cmd(24,310,547,120,fill_rgb=(0.93,0.96,1),stroke_rgb=(0.75,0.84,1),lw=0.7)
c+=text_cmd(36,390,14,"한 줄 요약")
c+=text_cmd(36,362,12,"PRO의 핵심은 빠른 답변이 아니라")
c+=text_cmd(36,338,12,"실무급 결과물을 일관되게 재현하는 데 있습니다.")
c+=text_cmd(24,80,10,"디자인 톤: 블루 계열 전자책 스타일")
pages.append(c)

objects=[]
objects.append('<< /Type /Catalog /Pages 2 0 R >>')
# pages root placeholder added later

font_obj_num=3
# plan obj numbers
obj_num=4
content_nums=[]
page_nums=[]
for _ in pages:
    content_nums.append(obj_num); obj_num+=1
    page_nums.append(obj_num); obj_num+=1
kids=' '.join(f'{n} 0 R' for n in page_nums)
objects.append(f'<< /Type /Pages /Count {len(page_nums)} /Kids [ {kids} ] >>')
objects.append('<< /Type /Font /Subtype /Type0 /BaseFont /HYSMyeongJo-Medium /Encoding /UniKS-UCS2-H /DescendantFonts [ << /Type /Font /Subtype /CIDFontType0 /BaseFont /HYSMyeongJo-Medium /CIDSystemInfo << /Registry (Adobe) /Ordering (Korea1) /Supplement 1 >> >> ] >>')
for i,p in enumerate(pages):
    data=p.encode('latin-1')
    objects.append((f'<< /Length {len(data)} >>\nstream\n'.encode()+data+b'endstream'))
    objects.append(f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {W} {H}] /Resources << /Font << /F1 3 0 R >> >> /Contents {content_nums[i]} 0 R >>')

out=Path('/workspace/ji100880/CHATGPT_PRO_결제자_지침서.pdf')
with out.open('wb') as f:
    f.write(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
    offs=[0]
    for n,obj in enumerate(objects, start=1):
        offs.append(f.tell())
        f.write(f'{n} 0 obj\n'.encode())
        if isinstance(obj, bytes): f.write(obj+b'\n')
        else: f.write(obj.encode()+b'\n')
        f.write(b'endobj\n')
    xref=f.tell(); total=len(objects)+1
    f.write(f'xref\n0 {total}\n'.encode()); f.write(b'0000000000 65535 f \n')
    for i in range(1,total): f.write(f'{offs[i]:010d} 00000 n \n'.encode())
    f.write(f'trailer\n<< /Size {total} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF'.encode())
print('generated', out)
