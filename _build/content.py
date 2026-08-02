#!/usr/bin/env python3
"""Every word on the page, as data. Written against PIDIA_pitch_deck.pptx.

One SECTIONS list drives the rail, the section order, the anchors and the scroll
controller's table. Editing the site should mean editing this file and nothing
else.

House rule — every element is a measurement, a source, or the object itself. A
sentence that is none of those does not go on the page. Numbers carry a `src`
line naming where they came from; where there is no source, the figure is
labelled an assumption in the same visual register.

The deck's strongest move is that it states its own limits before anyone asks,
so the "하지 않는 주장" section is load-bearing and sits in the middle of the
page rather than buried at the end.
"""

import charts

# ─────────────────────────────────────────────────────────────── helpers


def src(text):
    return f'<p class="src">{text}</p>'


def assumption(text):
    return f'<p class="src src--assumed">{text}</p>'


def stat(value, label, note=""):
    note = f"<i>{note}</i>" if note else ""
    return (
        f'<div class="stat"><b class="num">{value}</b>'
        f"<span>{label}</span>{note}</div>"
    )


def lede(text):
    return f'<p class="lede">{text}</p>'


def head(kicker, title):
    return (
        f'<header class="sec__head"><p class="kicker">{kicker}</p>'
        f'<h2 class="sec__title">{title}</h2></header>'
    )


# ─────────────────────────────────────────────────────────────── 1. hero

HERO = """
<p class="eyebrow">cfDNA methylation &middot; Self-collection &middot; Georgia</p>
<h1 class="hero__title">검사의 문턱을<br /><em>없앤다</em></h1>
<p class="hero__lede">
  혈액 몇 방울에서 읽는 다중 오믹스. 채혈센터도, 예약도, 보험 승인도 없이
  집에서 시작합니다. 암에서 시작해 뇌를 지나 정신까지, 같은 혈장 위에 패널만
  갈아 끼웁니다.
</p>
<figure class="thesis">
  <blockquote>정확도로 GRAIL과 싸우지 않습니다.<br />도달 거리로 싸웁니다.</blockquote>
</figure>
"""

# ────────────────────────────────────────────────────────────── 2. stakes

STAKES = (
    head(
        "문제",
        "기술이 없어서 죽는 게 아닙니다. <em>검사가 비싸고, 멀고, 잴 수 없어서</em> 죽습니다",
    )
    + lede(
        "보험이 없으면 대장내시경 한 번이 수천 달러입니다. 시골 카운티에는 검사받을 "
        "병원이 아예 없습니다. 정신건강은 회사에 말을 꺼내는 것부터가 문턱이고, "
        "우울증은 아직 피로 잴 방법조차 없습니다."
    )
    + '<div class="stats stats--lead">'
    + stat("5,940,000", "미국 5대 암에서 45년간 죽지 않은 사람", "1975–2020")
    + "</div>"
    + """
<div class="split">
  <div class="split__bar">
    <span class="split__seg split__seg--a" style="--w: 80%"><b class="num">80%</b>예방 · 조기발견</span>
    <span class="split__seg" style="--w: 20%"><b class="num">20%</b>치료</span>
  </div>
  <p class="split__note">475만 명은 신약이 아니라, 더 일찍 알아서 살았습니다.</p>
</div>
"""
    + src(
        "Goddard KAB et al. JAMA Oncology 2025;11(2):162-167 · NCI CISNET 모델링 "
        "추정치, 5대 암(폐·유방·대장직장·전립선·자궁경부) 기준"
    )
    + '<h3 class="sub">그래서 이미 있는 검사조차 대부분에게 닿지 않습니다</h3>'
    + '<div class="stats">'
    + stat("18.7%", "폐암 검진 자격자 중 실제 수검률", "5명 중 1명")
    + stat("73%", "정기 암검진이 하나 이상 밀린 미국 성인", "7,510명 설문")
    + stat(
        "62,110", "자격자 전원이 검진만 받아도 5년간 더 사는 사람", "연 약 1.24만 명"
    )
    + "</div>"
    + src(
        "American Cancer Society / JAMA 2025-11-19 (2024 NHIS, 자격 대상자 1,276만 명) "
        "· Prevent Cancer Foundation 2026 Early Detection Survey (성인 7,510명)"
    )
)

# ────────────────────────────────────────────────────────────── 3. people

PEOPLE = (
    head("세 사람", "문턱은 세 가지 얼굴로 나타납니다")
    + """
<div class="cards cards--3">
  <article class="card">
    <p class="card__tag">비싸다 &middot; Cost</p>
    <h3>마커스, <span class="num">58</span></h3>
    <p class="card__sub">조지아 콜럼버스 · 무보험</p>
    <blockquote class="quote">대장내시경이요? 저한테는 <span class="num">2,750</span>달러입니다.</blockquote>
    <ul class="reasons">
      <li><b class="num">36%</b> 비용 때문에 필요한 진료를 미룬 미국 성인</li>
      <li><b class="num">75%</b> 무보험 성인 기준 같은 비율</li>
    </ul>
  </article>
  <article class="card">
    <p class="card__tag">멀다 &middot; Distance</p>
    <h3>다니엘, <span class="num">34</span></h3>
    <p class="card__sub">조지아 농촌 카운티 · HIV 고위험군</p>
    <blockquote class="quote">검사 한 번 받으려면 왕복 네 시간입니다.</blockquote>
    <ul class="reasons">
      <li><b class="num">53</b>개 조지아에서 병원이 아예 없는 카운티</li>
      <li><b class="num">9,200만</b> 1차진료 부족지역에 사는 미국인</li>
    </ul>
  </article>
  <article class="card">
    <p class="card__tag">잴 수 없다 &middot; Measurability</p>
    <h3>지현, <span class="num">29</span></h3>
    <p class="card__sub">직장인 · 우울 증상 8개월째</p>
    <blockquote class="quote">힘든 건 아는데, 회사에 뭐라고 말하죠?</blockquote>
    <ul class="reasons">
      <li><b class="num">15%</b> 정신건강 문제를 관리자에게 말한 근로자</li>
      <li><b class="num">0</b>개 우울증에 임상적으로 쓰이는 객관적 혈액 지표</li>
    </ul>
  </article>
</div>
"""
    + src(
        "KFF Health Tracking Poll 2025-05 · Georgia Rural Health Transformation(주정부) "
        "· HRSA State of the Primary Care Workforce 2025 · NAMI/Ipsos 2026-03 "
        "· Abi-Dargham A et al., World Psychiatry 2023;22:236-262"
    )
)

# ─────────────────────────────────────────────────────────────── 4. proof

PROOF = (
    head(
        "이것은 문턱 문제입니다",
        "세계 최고의 기술이 <em>100명 중 0.17명</em>에게 닿았습니다",
    )
    + lede(
        "GRAIL Galleri는 혈액 한 번으로 50종 이상의 암을 찾습니다. 특이도 99.5%, "
        "2조 원 넘게 투입된 현존 최고 수준의 기술입니다."
    )
    + charts.dotfield(
        1000,
        2,
        50,
        "미국 50–79세 중 Galleri 수검자",
        "0.17%",
        "1,000명 가운데 1.7명 · 2025년 18.5만 건 / 1억 670만 명",
    )
    + '<div class="stats">'
    + stat("$949", "Galleri 정가", "")
    + stat("$147M", "GRAIL 2025 매출", "")
    + stat("$80M", "Guardant Shield 2025", "")
    + "</div>"
    + '<h3 class="sub">시장은 보고서에만 열려 있습니다</h3>'
    + charts.gapbars(
        ("시장조사 보고서 추정", 13.0, "$1.3B"),
        ("상장사 실제 매출 합계", 2.27, "$227M"),
        "보고서가 잡은 시장과 실제로 청구된 금액의 차이. 남은 문제는 정확도가 아니라 문턱입니다.",
    )
    + src(
        "GRAIL FY2025 실적발표(2026-02-19) · Guardant Health FY2025 · "
        "U.S. Census ACS 2019-2023(미국 50–79세 1억 670만 명) · "
        "Grand View Research / GM Insights MCED 시장 추정"
    )
)

# ─────────────────────────────────────────────── 5. kit (pinned scrub)
# The dimension callouts moved here from the hero, where they read as a strip
# floating with nothing to attach to. Next to the object they are annotating,
# they are a spec table rather than an ornament.

KIT = """
<div class="kitscroll__pin">
  <header class="sec__head sec__head--stage">
    <p class="kicker">작동 방식</p>
    <h2 class="sec__title">집에서 리포트까지</h2>
  </header>

  <section class="panel">
    <p class="panel__kicker"></p>
    <h3 class="panel__title"></h3>
    <p class="panel__lede"></p>
    <dl class="panel__specs"></dl>
    <div class="panel__lists"></div>
    <p class="panel__note"></p>
  </section>

  <nav class="stepnav">
    <button class="stepbtn" data-dir="-1" type="button" aria-label="이전 단계">&#8592;</button>
    <ol class="stepper"></ol>
    <button class="stepbtn" data-dir="1" type="button" aria-label="다음 단계">&#8594;</button>
  </nav>

  <p class="stage__hint">스크롤로 단계 이동 &middot; &#8592; &#8594; 키 &middot; 드래그로 회전</p>
</div>
"""

FLOW = (
    head("솔루션", "큰 맘 먹어야 했던 검사를, <em>마음먹은 날에</em>")
    + """
<ol class="flow">
  <li><b class="num">01</b><h3>자가 채혈</h3><p>안정화 튜브 · 랜싯 + 마이크로튜브</p></li>
  <li><b class="num">02</b><h3>페이퍼 퓨지</h3><p>혈장 분리 90초 · 장비값 $0.20</p></li>
  <li><b class="num">03</b><h3>상온 반송</h3><p>3–5일 안정 · 콜드체인 불필요</p></li>
  <li><b class="num">04</b><h3>cfDNA + 메틸화</h3><p>표적 패널 · PCR 기반 판독</p></li>
  <li><b class="num">05</b><h3>ML 분류기</h3><p>다중 오믹스 학습 · 조직기원 추정</p></li>
  <li><b class="num">06</b><h3>앱 리포트</h3><p>위험도 추이 · 행동 가이드</p></li>
</ol>
<div class="cards cards--3">
  <article class="card">
    <p class="card__tag">비싸다 &rarr; 저비용</p>
    <p>시퀀싱 전량이 아니라 발굴된 마커만 값싼 PCR로 읽습니다. 표적 패널과 페이퍼 퓨지 전처리로 원가를 낮춥니다.</p>
  </article>
  <article class="card">
    <p class="card__tag">멀다 &rarr; 배송</p>
    <p>안정화 채혈 튜브는 상온에서 3–5일 cfDNA 수율과 배경 변이가 유지됩니다. 검사실이 사람에게 갑니다.</p>
  </article>
  <article class="card">
    <p class="card__tag">잴 수 없다 &rarr; 정량화</p>
    <p>몸은 이미 숫자입니다. 뇌와 정신을 같은 혈장에서 읽을 수 있는 축으로 확장합니다.</p>
  </article>
</div>
<div class="caution">
  <p class="caution__label">먼저 인정합니다</p>
  <p>
    02단계 — 페이퍼 퓨지 혈장으로 분석 등급 cfDNA를 얻을 수 있는가는 <b>아직 논문이
    없습니다.</b> 저희 1호 마일스톤이 바로 그 검증 실험입니다. 표준 2단계 원심분리
    대비 수율 · 167bp 단편 무결성 · gDNA 오염률을 ddPCR로 비교합니다.
  </p>
</div>
"""
    + src(
        "Bhamla MS et al., Nature Biomedical Engineering 2017;1:0009 — 페이퍼 퓨지 "
        "125,000 rpm / 30,000 g / $0.20 / 혈장 분리 &lt;1.5분 · "
        "Medina Diaz I et al., PLoS ONE 2016;11:e0166354 (Streck BCT, n=60) · "
        "Sorber L et al., Cancers 2019;11:458"
    )
    + '<h3 class="sub">프로토타입 실측</h3>'
    + """
<dl class="dims">
  <div><dt>채혈펜</dt><dd class="num">&#216;25 &times; 50</dd></div>
  <div><dt>카트리지</dt><dd class="num">&#216;12 &times; 45</dd></div>
  <div><dt>혈장분리 원판</dt><dd class="num">&#216;65</dd></div>
  <div><dt>반송 케이스</dt><dd class="num">105 &times; 80 &times; 26</dd></div>
</dl>
"""
    + src("CAD 설계 기준 프로토타입 실측값 · 단위 mm")
)

# ──────────────────────────────────────────────────────────── 6. evidence

EVIDENCE = head("왜 cfDNA 메틸화인가", "기존 혈액검사가 <em>못 하는 일</em>") + """
<div class="cards cards--3">
  <article class="card card--muted">
    <h3>PSA</h3>
    <p>AUC <b class="num">0.678</b> — “민감도와 특이도를 동시에 만족하는 컷오프는 존재하지 않는다” (JAMA 2005, n=8,575)</p>
  </article>
  <article class="card card--muted">
    <h3>CA-125</h3>
    <p><b class="num">20만</b>명 RCT <b class="num">16</b>년 추적 — 병기는 앞당겼지만 사망률은 줄지 않음 (Lancet 2021)</p>
  </article>
  <article class="card card--muted">
    <h3>CBC · CMP</h3>
    <p>조기 암 검출에 대한 진단 정확도 근거 자체가 존재하지 않음</p>
  </article>
</div>

<div class="paper paper--lead">
  <p class="paper__cite">표적 메틸화 MCED — 특이도 <span class="num">99.3%</span> · n = <span class="num">6,689</span> · <span class="num">10</span>만 개 이상 메틸화 영역</p>
  <p class="paper__note">
    동일 샘플로 10개 분류기를 학습·검증한 통제 비교에서 <b>전장 메틸화가 최고 성능</b>이었습니다.
  </p>
  <p class="src">Liu MC et al., Annals of Oncology 2020;31:745-759 · Jamshidi A et al., Cancer Cell 2022;40:1537-1549</p>
</div>

<h3 class="sub">모델링 접근</h3>
<ul class="facts">
  <li><b class="num">12%</b><span>메틸화 어레이 + 랜덤포레스트로 중추신경계 종양 약 100종 분류. 실제 진단을 최대 12%에서 변경했고 WHO 분류 체계에 채택 — Capper, Nature 2018</span></li>
  <li><b class="num">10:1</b><span>동일 샘플에 10개 분류기를 학습·독립검증. 전장 메틸화가 조직기원 예측 최고 성능 — Jamshidi, Cancer Cell 2022</span></li>
  <li><b class="num">30M</b><span>오믹스 파운데이션 모델이 소량 데이터에서 성능을 끌어올림 — Geneformer, Nature 2023. 메틸화 특화 모델은 아직 preprint</span></li>
</ul>
<div class="caution caution--rule">
  <p class="caution__label">저희의 모델링 원칙</p>
  <p>
    외부에서 독립 수집된 코호트에 배치 보정을 걸고 홀드아웃 검증을 통과하기
    전까지, <b>저희는 어떤 AUC 숫자도 말하지 않습니다.</b>
  </p>
</div>
"""


# ──────────────────────────────────────────────────────────── 6b. model
# The one section that says what the AI actually does. It leads with the shape
# of the data rather than the name of a model, because the shape is what rules
# most of the models out.

MODEL = (
    head("모델", "AI가 하는 일은 <em>하나로 정해져 있습니다</em>")
    + lede(
        "수십만 개의 CpG 자리 가운데 질환을 가장 잘 설명하는 소수를 골라내는 것. "
        "그 이상도 이하도 아닙니다. 문제의 모양이 이미 쓸 수 있는 모델을 대부분 "
        "배제합니다."
    )
    + '<h3 class="sub">혈액이 행렬이 되기까지</h3>'
    + """
<ol class="flow flow--4">
  <li><b class="num">01</b><h3>바이설파이트 처리</h3><p>비메틸화 C &rarr; U(증폭 시 T) · 메틸화 5mC는 C로 남음</p></li>
  <li><b class="num">02</b><h3>비드칩 하이브리다이제이션</h3><p>CpG 자리마다 상보 프로브 · Type I/II</p></li>
  <li><b class="num">03</b><h3>단일 염기 신장</h3><p>붙는 염기에 따라 형광 채널이 갈림</p></li>
  <li><b class="num">04</b><h3>베타값 환산</h3><p>&beta; = M / (M + U + 100) · 0에서 1 사이</p></li>
</ol>
<div class="paper">
  <p class="paper__cite">입력 행렬 — 행은 사람, 열은 CpG 자리의 <span class="num">&beta;</span>값, 라벨은 질환 유무</p>
  <p class="paper__note">
    열이 <b class="num">수십만</b>, 행이 <b class="num">수백</b>입니다. 이 비율이
    이 문제의 전부이고, <b>고차원 저샘플</b>이라 부릅니다.
  </p>
</div>
"""
    + charts.matrix(
        180,
        5,
        [88, 89, 90, 91, 92],
        "샘플<tspan x=\"21\" dy=\"5\">수백 명</tspan>",
        "CpG 자리 &mdash; 수십만 개",
        "최종 3–5개",
        "가로로 수십만, 세로로 수백. 이 비율 하나가 쓸 수 있는 모델을 대부분 "
        "정합니다. 표시된 몇 줄이 이 모든 작업의 결과물입니다.",
    )
    + '<h3 class="sub">그래서 딥러닝이 아닙니다</h3>'
    + """
<div class="twocol">
  <div class="twocol__col twocol__col--no">
    <p class="twocol__label">쓰지 않습니다</p>
    <ul class="reasons">
      <li><b>딥러닝(CNN · Transformer)</b> — 샘플 수백에 차원 수십만이면 오버피팅이 먼저 옵니다. 규제 제출 자료로 블랙박스는 불리합니다</li>
      <li><b>k-NN</b> — 차원이 이만큼 많으면 “거리”라는 개념 자체가 무의미해집니다</li>
    </ul>
  </div>
  <div class="twocol__col twocol__col--yes">
    <p class="twocol__label">씁니다</p>
    <ul class="reasons">
      <li><b>랜덤 포레스트</b> — 분기마다 불순도 감소를 누적해 <b>변수 중요도</b>를 매깁니다. 부트스트랩이라 이상치 하나에 흔들리지 않고, 트리 구조가 비선형·상호작용을 그대로 잡습니다</li>
      <li><b>Elastic-Net</b> — L1의 변수 선택과 L2의 고른 기여를 함께 씁니다. 핵심은 <b>group effect</b>: 함께 메틸화되는 CpG 무리를 같이 살리거나 같이 버립니다. LASSO 단독은 그중 하나만 무작위로 남깁니다</li>
      <li><b>로지스틱 회귀</b> — 마커가 3–5개로 좁혀진 <b>최종 패널</b> 단계. 계수를 그대로 설명할 수 있어야 인허가 서류가 됩니다</li>
    </ul>
  </div>
</div>
"""
    + src(
        "Zou H &amp; Hastie T, J R Stat Soc B 2005;67:301-320 (Elastic-Net) · "
        "Breiman L, Machine Learning 2001;45:5-32 (Random Forest) · "
        "&beta;값 정의는 Illumina Infinium 어세이 규격"
    )
    + '<h3 class="sub">이 분야에서 가장 비싼 교훈</h3>'
    + charts.gapbars(
        ("배치별로 처리한 데이터", 0.76, "AUC 0.76"),
        ("배치 보정 후 홀드아웃", 0.57, "AUC &lt;0.57"),
        "같은 데이터, 같은 모델입니다. 코호트·처리 시기·실험실마다 기술적 지문이 "
        "남고 환자와 대조군이 배치에 몰려 있으면, 모델은 생물학이 아니라 "
        "<b>배치를 학습합니다.</b> 6개 독립 집단 · 8개 배치 · 12가지 전략에서 "
        "명목 유의 CpG 1,987개 중 모든 배치를 버틴 것은 하나도 없었습니다.",
        lead="",
    )
    + charts.batches(
        [
            [(14 + (i % 4) * 9, 13 + (i // 4) * 12, i % 2) for i in range(12)],
            [(56 + (i % 4) * 9, 13 + (i // 4) * 12, i % 3 == 0) for i in range(12)],
        ],
        "배치로 칠하면",
        "질환으로 칠하면",
        "같은 점, 같은 자리입니다. 칠하는 규칙만 바꿨습니다. "
        "가르라고 시키면 모델은 언제나 왼쪽을 찾아냅니다.",
        "도식입니다. 실제 좌표가 아니라 배치 효과가 왜 성능처럼 보이는지를 "
        "보이기 위한 그림입니다",
    )
    + '<div class="caution">'
    + '<p class="caution__label">그래서 저희의 규칙</p>'
    + "<p>외부에서 독립 수집된 코호트에 배치 보정을 걸고 홀드아웃 검증을 통과하기 "
    + "전까지, <b>저희는 어떤 AUC 숫자도 말하지 않습니다.</b></p></div>"
    + '<h3 class="sub">모델 이름보다 먼저 정하는 것</h3>'
    + """
<ol class="method">
  <li>
    <h3>무엇을 예측하는가</h3>
    <p>질환별로 별도 모델입니다. 암 · 퇴행성 뇌질환 · 만성 스트레스는 정답의 성격이 서로 다르므로 한 모델에 담지 않습니다.</p>
  </li>
  <li>
    <h3>정답은 무엇인가</h3>
    <p>암은 조직검사 병리 확진, 퇴행성 뇌질환은 신경과 전문의 진단 + MRI/PET, 스트레스는 표준화 설문과 추적 관찰. <b>정답의 신뢰도가 모델 성능의 상한입니다.</b></p>
  </li>
  <li>
    <h3>대조군은 누구인가</h3>
    <p>건강한 일반인이 아니라 같은 위험군 중 추적 기간 내 미발생자. 건강 대조군을 쓰면 모델이 배우는 것은 질환 유무가 아니라 위험군 여부입니다.</p>
  </li>
  <li>
    <h3>무엇을 통제하는가</h3>
    <p>연령 · 성별 · 약물 · 혈액세포 조성(cell-type deconvolution) · 배치. 보정하지 않으면 모델은 질환이 아니라 연령을 학습합니다.</p>
  </li>
  <li>
    <h3>검증군은 몇 번 여는가</h3>
    <p>한 번입니다. 반복해 조회하며 조정하면 그건 검증이 아니라 튜닝입니다. 같은 사람의 반복검사는 전부 한쪽에만 둡니다.</p>
  </li>
</ol>
"""
    + '<h3 class="sub">메틸화가 실제로 가장 잘하는 일</h3>'
    + lede(
        "메틸화의 가장 성공적인 응용은 질환 진단이 아니라 <b>나이 추정</b>입니다. "
        "그리고 그 계보를 보면 저희가 3단계에서 무엇을 말할 수 있고 무엇을 말할 수 "
        "없는지가 그대로 나옵니다."
    )
    + """
<div class="compare__scroll">
  <table class="ctable">
    <thead><tr><th scope="col">시계</th><th scope="col">세대</th><th scope="col">훈련 대상</th><th scope="col">규모</th></tr></thead>
    <tbody>
      <tr><th scope="row">Horvath</th><td class="num">1세대</td><td>역년 · 다조직</td><td class="num">353 CpG</td></tr>
      <tr><th scope="row">Hannum</th><td class="num">1세대</td><td>역년 · 혈액</td><td class="num">71 CpG</td></tr>
      <tr><th scope="row">PhenoAge</th><td class="num">2세대</td><td>임상 표현형 기반 사망 위험</td><td class="num">513 CpG</td></tr>
      <tr class="ctable__ours"><th scope="row">GrimAge</th><td class="num">2세대</td><td>사망률 + 혈장 단백질 7종 + 흡연년수</td><td>사망 예측 최강</td></tr>
      <tr class="ctable__ours"><th scope="row">DunedinPACE</th><td class="num">3세대</td><td>노화 <b>속도</b> · 종단 데이터</td><td>역년당 생물학적 년수</td></tr>
    </tbody>
  </table>
</div>
<div class="caution">
  <p class="caution__label">신호가 나오는 곳이 정해져 있습니다</p>
  <p>
    정신질환 부담 점수는 <b>2·3세대 시계에서만</b> 가속과 유의하게 연관됐습니다
    (수정 R&sup2; <b class="num">0.22</b> · <b class="num">0.33</b>). 역년으로
    훈련된 1세대에서는 나오지 않습니다. 정신질환이 나이를 빨리 먹게 하는 것이
    아니라, <b>건강 손상을 누적시킨다</b>고 읽는 편이 데이터에 맞습니다.
  </p>
</div>
<div class="caution caution--rule">
  <p class="caution__label">그래서 시계를 지표로 쓰지 않습니다</p>
  <p>
    GrimAge에는 <b>흡연년수가 아예 내장</b>되어 있습니다. “우울증 → GrimAge 가속”의
    상당 부분이 흡연일 수 있다는 뜻입니다. 인종·조상에 따라 방향이 뒤집히고, 1세대는
    세포 조성이 상당 부분을 설명합니다. 인구집단별 재보정 없이 쓰면 안 됩니다.
  </p>
</div>
"""
    + '<h3 class="sub">그래서 질환이 아니라 노출을 잽니다</h3>'
    + lede(
        "우울증의 메틸화 표지를 찾는 대신, <b>위험요인의 메틸화 시그니처</b>를 씁니다. "
        "각 형질의 점수는 수만 명 규모에서 이미 검증된 것들입니다."
    )
    + """
<div class="paper paper--lead">
  <p class="paper__cite">예측 = <i>f</i>( MS<sub>흡연</sub>, MS<sub>BMI</sub>, MS<sub>음주</sub>, MS<sub>교육</sub>, MS<sub>HDL</sub>, MS<sub>총콜레스테롤</sub> )</p>
  <p class="paper__note">
    메틸화를 “질환의 표지”가 아니라 <b>환경 노출의 생물학적 기록보관소</b>로
    다시 정의하는 접근입니다.
  </p>
  <p class="src">Barbu MC et al., 2022 — 대리 형질 점수(surrogate trait score)</p>
</div>
<figure class="thesis thesis--inline">
  <blockquote>
    사람은 흡연량을 축소해서 말합니다.<br />AHRR 메틸화는 그러지 않습니다.
  </blockquote>
</figure>
<div class="prose">
  <p>
    자기보고를 우회하는 <b>노출 측정 도구</b>. 이것이 현재 근거가 실제로 지지하는
    메틸화의 용도이고, 저희 3단계가 “우울증 진단”이 아니라 “누적 스트레스 노출의
    분자 기록”인 이유입니다.
  </p>
</div>
"""
    + src(
        "Horvath S, Genome Biol 2013;14:R115 · Hannum G et al., Mol Cell 2013;49:359-367 · "
        "Levine ME et al., Aging 2018;10:573-591 (PhenoAge) · Lu AT et al., Aging "
        "2019;11:303-327 (GrimAge) · Belsky DW et al., eLife 2022;11:e73420 "
        "(DunedinPACE) · Barbu MC et al., 2022"
    )
    + '<h3 class="sub">유병률이 정확도보다 세게 작용합니다</h3>'
    + charts.gapbars(
        ("정신과 클리닉 (유병률 40%)", 66.7, "PPV 66.7%"),
        ("일반 인구 (유병률 5%)", 13.6, "PPV 13.6%"),
        "민감도와 특이도가 똑같이 75%인 <b>같은 검사</b>입니다. 유병률만 바뀌었습니다. "
        "정신과 바이오마커를 일반 인구 스크리닝에 쓰면 양성 100명 중 86명이 "
        "위양성입니다. 저희 3단계가 진단이 아니라 <b>노출의 정량화</b>인 이유입니다.",
    )
    + assumption(
        "민감도·특이도 75%, 유병률 5%와 40%를 넣은 계산 예시입니다. 특정 검사의 "
        "실측값이 아니라 베이즈 정리가 이 문제에서 어떻게 작동하는지를 보이는 수치입니다"
    )
    + src(
        "Sales AJ et al., Acta Neuropsychiatr 2021;33:217-241 · "
        "Barbu MC et al., 2021 — 벌점 회귀로 우울증 분산 1.75% 설명 · "
        "Translational Psychiatry 2024 — 6개 코호트 · 8개 배치 · 12가지 전략 "
        "(배치 보정 후 전 분류기 AUC &lt;0.57)"
    )
)

# ────────────────────────────────────────────────────────────── 7. limits
# The deck leads with its own weaknesses. Keeping that here, mid-page, is the
# single most credible thing on the site.

LIMITS = (
    head("하지 않는 주장", "심사위원께서 물으시기 전에 <em>먼저 말씀드립니다</em>")
    + lede("이 세 가지는 이 분야 전체의 한계이고, 저희도 예외가 아닙니다.")
    + """
<ol class="method">
  <li>
    <h3>Stage I 민감도는 낮습니다</h3>
    <p>
      전체 암 기준 1기 민감도 <b class="num">16.8–18%</b>. 조기 발견을 표방하지만
      가장 이른 시점이 가장 약합니다.
    </p>
  </li>
  <li>
    <h3>실사용 PPV는 <span class="num">38%</span>였습니다</h3>
    <p>
      PATHFINDER <b class="num">6,662</b>명 — 신호 양성 <b class="num">92</b>명 중
      진짜 암은 <b class="num">35</b>명이었습니다.
    </p>
  </li>
  <li>
    <h3>대규모 RCT는 1차 지표를 못 넘었습니다</h3>
    <p>
      NHS-Galleri <b class="num">14.3만</b>명 — 3·4기 진단 감소라는 1차 평가변수를
      달성하지 못했습니다. 동료심사 전 발표입니다.
    </p>
  </li>
</ol>
"""
    + '<h3 class="sub">실제로 세어보면 이렇습니다</h3>'
    + charts.dotfield(
        92,
        35,
        23,
        "신호 양성 92명 중 실제로 암이었던 사람",
        "38%",
        "PATHFINDER 6,662명 · 나머지 57명은 추가 검사 끝에 암이 아니었습니다",
    )
    + """
<figure class="thesis thesis--inline">
  <blockquote>
    2조 원과 10만 명 코호트를 가진 회사를 알고리즘으로 이기겠다는 팀은 믿지
    마십시오. 저희는 도달 거리로 이깁니다.
  </blockquote>
</figure>
"""
    + src(
        "Klein EA et al., Annals of Oncology 2021;32:1167-1177(n=4,077) · "
        "Schrag D et al., Lancet 2023;402:1251-1260(PATHFINDER, n=6,662) · "
        "NHS-Galleri, ASCO 2026 발표 — 동료심사 논문 미출간"
    )
)

# ───────────────────────────────────────────────────────────── 8. roadmap

ROADMAP_SEC = (
    head("로드맵", "같은 혈장에서, <em>축을 하나씩</em> 늘립니다")
    + lede(
        "핵심은 한 번의 채혈로 세 축을 다 읽는 것이 아니라, 같은 혈장 전처리 위에 "
        "패널만 갈아 끼우는 구조입니다."
    )
    + """
<ol class="phases">
  <li class="phase phase--now">
    <p class="phase__no"><span class="num">PHASE 1</span> · <span class="num">0–2</span>년</p>
    <h3>암</h3>
    <p>기본 혈액 패널 + cfDNA 메틸화 다중암 스크리닝</p>
    <p class="phase__grade">근거 확립 · 상용 가능</p>
  </li>
  <li class="phase">
    <p class="phase__no"><span class="num">PHASE 2</span> · <span class="num">2–4</span>년</p>
    <h3>퇴행성 뇌질환</h3>
    <p>알츠하이머 · 파킨슨 · ALS — 혈액으로 뇌를 보는 건 이미 FDA 승인됨</p>
    <p class="phase__grade">근거 강함 · 모달리티 검토 중</p>
  </li>
  <li class="phase">
    <p class="phase__no"><span class="num">PHASE 3</span> · <span class="num">4</span>년 +</p>
    <h3>만성 스트레스 정량화</h3>
    <p>정신질환 진단이 아니라, 누적 스트레스 노출의 분자 기록</p>
    <p class="phase__grade">탐색 연구 모듈</p>
  </li>
</ol>

<h3 class="sub">세 축과 네 마일스톤을 한 축 위에 놓으면</h3>
"""
    + charts.timeline(
        ["0", "6개월", "12", "18", "24", "3년", "4년", "5년+"],
        [
            ("Phase 1", "암", [(1, 5, "now", "cfDNA 메틸화 다중암")]),
            ("Phase 2", "퇴행성 뇌질환", [(5, 8, "next", "알츠하이머 · 파킨슨 · ALS")]),
            ("Phase 3", "만성 스트레스", [(8, 9, "later", "탐색 연구 모듈")]),
            ("M1", "페이퍼 퓨지 검증", [(1, 2, "ms ms--risk", "최고 위험")]),
            ("M2", "조지아 파일럿 n=500", [(2, 3, "ms", "물류 검증")]),
            ("M3", "CLIA 랩 · LDT 경로", [(3, 4, "ms", "규제")]),
            ("M4", "Phase 2 탐색 코호트", [(4, 5, "ms", "확장")]),
        ],
        caption="M1–M4는 전부 Phase 1 안에서 끝납니다. 2단계는 그 뒤에 시작합니다.",
    )
    + """
<h3 class="sub">Phase 2 — 혈액으로 뇌를 본다는 전제는 이미 통과됐습니다</h3>
<div class="twocol">
  <div class="twocol__col">
    <p class="twocol__label">확립된 근거</p>
    <ul class="facts">
      <li><b class="num">2025.05</b><span>FDA, 최초의 알츠하이머 혈액검사 승인(Lumipulse pTau217/A&beta;42) — PPV 91.7%, NPV 97.3%, n=499</span></li>
      <li><b class="num">0.97</b><span>혈장 p-tau217 1차 의료 AUC. 같은 환자를 본 1차 진료의사 정확도 61% vs 검사 91% — JAMA 2024</span></li>
      <li><b class="num">2016</b><span>cfDNA 메틸화로 뇌 유래 DNA를 혈장에서 검출한 최초 선례 — PNAS</span></li>
    </ul>
  </div>
  <div class="twocol__col twocol__col--caution">
    <p class="twocol__label">아직 미해결</p>
    <ul class="reasons">
      <li>ALS에서 AUC 0.91 — 단 <b class="num">n=30</b> (JCI 2026)</li>
      <li>최대 규모 연구(<b class="num">n=281</b>, Sci Rep 2025)는 <b>음성</b> — 혈청 NfL·GFAP 대비 추가 이득 없음</li>
      <li>PNAS 2016의 검출은 급성 뇌손상 상황이었습니다</li>
    </ul>
  </div>
</div>
<div class="caution">
  <p>
    그래서 Phase 2 주장은 “메틸화로 알츠하이머를 잡겠다”가 아닙니다. 페이퍼 퓨지가
    만드는 혈장은 <b>모달리티 중립</b>입니다. 같은 한 방울로 오늘은 p-tau217
    면역측정을, 내일은 메틸화 패널을 돌립니다.
  </p>
</div>

<h3 class="sub">Phase 3 — 의도적으로 보수적인 영역</h3>
<div class="twocol">
  <div class="twocol__col twocol__col--no">
    <p class="twocol__label">주장하지 않습니다</p>
    <p><b>“우울증 혈액검사”는 존재하지 않습니다.</b></p>
    <ul class="reasons">
      <li>메틸화 우울증 분류기 8개 코호트(<b class="num">n=1,942</b>)를 재분석하니, 제대로 정규화하면 AUC가 <b class="num">0.57</b> 아래로 붕괴하고 홀드아웃 예측력이 사라졌습니다</li>
      <li>세로토닌 수송체(SLC6A4) 메틸화는 2,296명 메타분석에서 효과 크기 <b class="num">0.06</b> — 사실상 무효</li>
    </ul>
  </div>
  <div class="twocol__col twocol__col--yes">
    <p class="twocol__label">주장합니다</p>
    <p><b>메틸화는 만성 스트레스 “노출”의 가장 재현성 높은 분자 기록입니다.</b></p>
    <ul class="reasons">
      <li>역경 노출 연구 40편 중 <b class="num">89%</b>에서 NR3C1 메틸화 증가</li>
      <li>PGC-PTSD 23개 코호트 <b class="num">n=5,077</b> — 유전체 수준 유의 CpG 11개</li>
      <li>파병 전 메틸화 위험점수가 파병 후 PTSD 발병을 예측 (Wani 2024)</li>
    </ul>
  </div>
</div>
<div class="prose">
  <p>
    기존 지표도 약합니다 — 만성 스트레스의 표준으로 쓰이는 모발 코르티솔은
    <b class="num">N=10,289</b> 메타분석에서 주관적 스트레스·기분장애와 일관된
    연관이 없었습니다. <b>약한 기존 지표를 어려운 문제에서 이기겠다는 건 말이
    됩니다. 우울증 혈액검사를 가졌다는 건 말이 안 됩니다.</b>
  </p>
</div>
"""
    + src(
        "FDA 2025-05-16 · Palmqvist S et al., JAMA 2024;332:1245-1257 · "
        "Lehmann-Werman R et al., PNAS 2016;113:E1826 · Chatterton Z et al., "
        "Sci Rep 2025;15:38844 · Sokolov AV &amp; Schi&ouml;th HB, Transl Psychiatry "
        "2024;14:287 · Turecki G &amp; Meaney MJ, Biol Psychiatry 2016;79:87-96 · "
        "Katrinli S et al., Genome Med 2024;16:147 · Stalder T et al., "
        "Psychoneuroendocrinology 2017;77:261-274"
    )
)

# ────────────────────────────────────────────────────────────── 9. market

MARKET = (
    head("시장", "선점할 구간")
    + """
<div class="funnel">
  <div class="funnel__step" style="--w: 100%">
    <p class="funnel__tier">TAM</p>
    <p class="funnel__val num">$1.3B &rarr; $5.3B</p>
    <p class="funnel__desc">글로벌 다중암 조기검진(MCED) 시장, 2025 &rarr; 2035 · CAGR 14.8–17%, 2개 기관 교차검증</p>
  </div>
  <div class="funnel__arrow"><span>미국 한정</span></div>
  <div class="funnel__step" style="--w: 62%">
    <p class="funnel__tier">SAM</p>
    <p class="funnel__val num">$1.75<i>B</i></p>
    <p class="funnel__desc">미국 MCED $522.8M + 미국 소비자직접 랩테스트 $1.23B</p>
  </div>
  <div class="funnel__arrow"><span>조지아 50–79세 332만 명 &times; 침투율 2% &times; ASP $400</span></div>
  <div class="funnel__step funnel__step--ours" style="--w: 34%">
    <p class="funnel__tier">SOM <b>5년차</b></p>
    <p class="funnel__val num">$27<i>M ARR</i></p>
    <p class="funnel__desc">보수 시나리오 3년차 0.5% = $6.6M</p>
  </div>
</div>
"""
    + assumption(
        "침투율 앵커 — GRAIL은 $949 가격대에서 미국 침투율 0.17%입니다. "
        "5% 이상을 가정하는 계획은 믿지 마십시오. 2035년 전망치는 기관별로 2.5배 "
        "차이납니다(Fact.MR은 $82억 → $163억, CAGR 6.5%)"
    )
    + '<h3 class="sub">경쟁 지형</h3>'
    + charts.bars(
        [
            ("MindX Sciences", 1958, "$1,958", "단일 서비스 · 고비용"),
            ("Guardant Shield", 1495, "$1,495", "대장암 스크리닝"),
            ("GRAIL Galleri", 949, "$949", "50종+ MCED"),
            ("Exact Cancerguard", 689, "$689", "MCED"),
            ("TruDiagnostic", 499, "$499", "생물학적 나이"),
            ("PIDIA", 450, "$400–500", "다질환 메틸화 패널 · 채혈센터 불필요"),
            ("Function Health", 365, "$365/년", "160여 개 검사 종합 · 최대 위협"),
            ("myLAB Box", 189, "$189", "자가진단 키트"),
            ("Everlywell HIV", 69, "$69", "단일 항목"),
        ],
        caption="가로 길이는 정가에 비례합니다. 위쪽 끝은 아래쪽 끝의 28배입니다.",
        ours="PIDIA",
    )
    + """
<h3 class="sub">그래서 비어 있는 구간</h3>
<div class="cards">
  <article class="card card--muted">
    <p class="card__tag">최대 위협</p>
    <h3>Function Health</h3>
    <p>연 $365에 160여 개 검사. $298M 조달, 기업가치 $2.5B. Galleri와 알츠하이머 검사를 애드온으로 재판매합니다.</p>
  </article>
  <article class="card card--lead">
    <p class="card__tag">빈 공간</p>
    <h3>$400–700 구간의 다질환 메틸화 패널</h3>
    <p>Cancerguard보다 싸고, TruDiagnostic보다 임상적이고, MindX의 4분의 1 가격.</p>
  </article>
</div>
"""
    + src("각 사 공식 가격 페이지 및 2025 회계연도 실적 발표 기준(2026-07 확인)")
    + '<h3 class="sub">우리만 가진 세 가지</h3>'
    + """
<ol class="method">
  <li>
    <h3>문턱 — 채혈센터가 없습니다</h3>
    <p>Function Health는 Quest 지점에 가야 합니다. 저희는 우편함에서 끝납니다. 조지아 53개 카운티에는 애초에 갈 병원이 없습니다.</p>
  </li>
  <li>
    <h3>확장 — 같은 혈장, 다른 패널</h3>
    <p>경쟁사는 검사 항목을 늘립니다. 저희는 전처리를 공유하고 패널만 바꿉니다. 1단계 물류가 2·3단계의 자산이 됩니다.</p>
  </li>
  <li>
    <h3>밀착 — 한 주에서 시작합니다</h3>
    <p>미국 전역이 아니라 조지아 한 주. 배송 온도, 규제, 파트너 랩을 하나의 변수로 통제하고 그 다음에 확장합니다.</p>
  </li>
</ol>
<figure class="thesis thesis--inline">
  <blockquote>더 정확한 검사를 만드는 팀이 아니라, 검사가 사람에게 도달하는 경로를 만드는 팀입니다.</blockquote>
</figure>
"""
)

# ───────────────────────────────────────────────────────────── 10. georgia

GEORGIA = (
    head("비치헤드", "왜 <em>조지아</em>에서 시작하는가")
    + lede(
        "세 페르소나가 한 주 안에 전부 있고, 3단계 로드맵 전체가 같은 인구에서 검증 가능합니다."
    )
    + '<div class="stats">'
    + stat("471.9", "암 발생률 (10만 명당)", "전국 평균 448.6 대비 +5.2%")
    + stat("12.0%", "무보험률 · 전국 49위", "약 134만 명 · 현금결제 고객층")
    + stat("53", "병원이 아예 없는 카운티 (159개 중)", "농촌 인구 240만 명")
    + stat("65,195", "HIV 감염인 수", "44%가 50세 이상 · 신규 연 2,442명")
    + "</div>"
    + charts.deltabars(
        [
            ("암 발생률 (10만 명당)", "471.9", "448.6", +5.2, False),
            ("대장암 검진율", "69.5%", "71.1%", -2.2, False),
        ],
        "전국 평균",
        "암은 더 걸리고 검진은 덜 받습니다. 두 지표가 같은 방향으로 벌어지는 곳이 비치헤드입니다.",
        axis_label="전국 평균 기준 편차",
        subject="조지아",
    )
    + '<h3 class="sub">2·3단계의 대상 인구까지 같은 주에 있습니다</h3>'
    + '<div class="stats">'
    + stat("188,300", "조지아 농촌 65세 이상 알츠하이머·치매 환자", "")
    + stat("19 : 15", "농촌 자살률 (10만 명당), 비농촌 대비", "")
    + stat("69.5%", "대장암 검진율 · 전국 32위", "미국 평균 71.1%")
    + "</div>"
    + src(
        "NCI State Cancer Profiles(2018-2022 연령보정) · America's Health Rankings "
        "2024(CDC BRFSS) · Georgia Rural Health Transformation, 조지아 주정부 공식 "
        "신청서 · Georgia DPH HIV Surveillance Fact Sheet 2023"
    )
)

# ────────────────────────────────────────────────────────── 11. milestones

# The entry sequence. Every figure in `facts` is stated and sourced elsewhere on
# this page — the beachhead numbers in the Georgia section, the market numbers in
# the market section — so the map argues with the page's own evidence rather than
# introducing figures of its own.
#
# Stop 03 is reached through the beachhead rather than around it: MAP
# International, which supplies medicines to the developing world, is
# headquartered in Georgia, so the Africa leg leaves from the state the pilot
# runs in.
STOPS = [
    {
        "seq": "01",
        "name": "조지아",
        "tag": "무보험 12.0% · 병원 없는 카운티 53",
        "role": "비치헤드 · 0–2년",
        "region": "georgia",
        "paint": 3,
        "lon": -83.44,
        "lat": 32.68,
        "r": 3.0,
        "nudge": (-4.0, 14.0),
        "jump": False,
        "bow": 0,
        "sats": [],
        "facts": [
            ("12.0%", "무보험률 · 전국 49위"),
            ("53", "병원이 없는 카운티 / 159"),
            ("471.9", "암 발생률 · 전국 448.6"),
            ("332만", "50–79세 · 초기 시장"),
        ],
        "why": "문턱이 가장 높은 곳에서 문턱을 없애는 제품을 검증합니다. "
        "세 페르소나가 한 주 안에 전부 있고, 배송 온도·규제·파트너 랩을 "
        "변수 하나로 묶을 수 있는 크기입니다. 침투율 2% × ASP $400 = "
        "5년차 SOM $27M ARR.",
    },
    {
        "seq": "02",
        "name": "미국 전역",
        "tag": "SAM $1.75B · 50–79세 1억 670만",
        "role": "확장 · 2–4년",
        "region": "usa",
        "paint": 0,
        "lon": -98.35,
        "lat": 39.50,
        "r": 3.4,
        "nudge": (0.0, -13.0),
        "jump": False,
        "bow": 0,
        "sats": [
            (-74.01, 40.71, "뉴욕"),
            (-87.63, 41.88, "시카고"),
            (-118.24, 34.05, "LA"),
            (-95.37, 29.76, "휴스턴"),
        ],
        "facts": [
            ("1억 670만", "50–79세 인구"),
            ("$1.75B", "SAM"),
            ("$522.8M", "미국 MCED"),
            ("$1.23B", "소비자직접 랩테스트"),
        ],
        "why": "우편으로 끝나는 검사는 주 경계를 넘는 데 새 물류가 필요하지 "
        "않습니다. 조지아에서 검증한 회수율·반송 소요일·온도 로거를 그대로 "
        "들고 대도시로 갑니다. 같은 물류, 같은 패널.",
    },
    {
        "seq": "03",
        "name": "아프리카",
        "tag": "콜드체인 불필요 · 채혈센터 0",
        "role": "국제기구 채널 · 4년 +",
        "region": "africa",
        "paint": 1,
        "lon": 21.0,
        "lat": 2.0,
        "r": 3.4,
        "nudge": (15.0, 7.0),
        "jump": True,
        "bow": 26,
        "sats": [
            (36.82, -1.29, "나이로비"),
            (3.38, 6.52, "라고스"),
            (28.05, -26.20, "요하네스버그"),
        ],
        "facts": [
            ("3–5일", "상온 안정 · 콜드체인 불필요"),
            ("$0.20", "페이퍼 퓨지 장비값"),
            ("0", "필요한 채혈센터 수"),
        ],
        "why": "채혈센터가 없는 곳이 문턱이 가장 높은 곳입니다. 콜드체인을 "
        "요구하지 않는 것이 여기서는 편의가 아니라 진입 조건이고, "
        "MAP International 본사가 조지아에 있어 이 다리는 비치헤드에서 "
        "출발합니다.",
    },
    {
        "seq": "04",
        "name": "한국",
        "tag": "국가암검진 채널 · IVD 인허가",
        "role": "개발 · IP 거점",
        "region": "korea",
        "paint": 2,
        "lon": 127.6,
        "lat": 36.4,
        "r": 2.6,
        "nudge": (5.5, -6.0),
        "jump": True,
        "bow": -22,
        "sats": [],
        "facts": [
            ("국가암검진", "기존 수검 채널"),
            ("IVD", "체외진단의료기기 인허가"),
        ],
        "why": "개발과 IP가 있는 곳으로 돌아옵니다. 이미 전 국민 수검 채널이 "
        "작동하는 시장이라, 문턱 문제의 형태가 미국과 다릅니다.",
    },
]


MILESTONES = (
    head("마일스톤", "가장 불확실한 것을 <em>가장 먼저</em> 검증합니다")
    + charts.milestones(
        [
            ("M1", "6개월", "페이퍼 퓨지 cfDNA 품질", 46, True),
            ("M2", "12개월", "조지아 파일럿 n=500", 30, False),
            ("M3", "18개월", "CLIA 랩 · LDT 경로", 18, False),
            ("M4", "24개월", "Phase 2 탐색 코호트", 10, False),
        ],
        "첫 단계에서 가장 크게 떨어집니다. 그것이 이 순서를 고른 이유입니다.",
        assumption(
            "낙폭의 순서는 덱이 밝힌 위험 순위입니다. 높이는 그 순위를 그린 것이지 "
            "측정값이 아니며, 그래서 세로축에 숫자가 없습니다."
        ),
        axis_y="남은 불확실성",
        axis_x="시간 &rarr;",
    )
    + '<h3 class="sub">그 순서대로, 지도 위에서</h3>'
    + charts.wmap(
        STOPS,
        "세계지도 위에 단계별로 채워지는 진출 영역 — 조지아 한 주에서 미국 전역, "
        "아프리카, 한국 순",
        legend=("진출 영역은 누적됩니다", "점선은 물류가 새로 필요한 구간"),
    )
    + """
<h3 class="sub">네 개의 검증, 하나씩</h3>
<ol class="ms">
  <li class="ms__item ms__item--risk">
    <p class="ms__no"><span class="num">M1</span> · <span class="num">6</span>개월</p>
    <h3>페이퍼 퓨지 혈장의 cfDNA 품질 검증</h3>
    <p>표준 2단계 원심분리 대비 — cfDNA 수율 / 167bp 단핵소체 단편 무결성 / gDNA 오염률(ddPCR) / 메틸화 콜 일치도</p>
    <p class="ms__tag">최고 위험</p>
  </li>
  <li class="ms__item">
    <p class="ms__no"><span class="num">M2</span> · <span class="num">12</span>개월</p>
    <h3>조지아 파일럿 n = <span class="num">500</span></h3>
    <p>무보험·농촌 인구 대상 자가채취 회수율, 반송 소요일, 온도 로거 데이터, 재검사 의향</p>
    <p class="ms__tag">물류 검증</p>
  </li>
  <li class="ms__item">
    <p class="ms__no"><span class="num">M3</span> · <span class="num">18</span>개월</p>
    <h3>CLIA 인증 랩 파트너십 · LDT 경로 확정</h3>
    <p>자체 랩 구축 대신 파트너십으로 규제 시간을 압축</p>
    <p class="ms__tag">규제</p>
  </li>
  <li class="ms__item">
    <p class="ms__no"><span class="num">M4</span> · <span class="num">24</span>개월</p>
    <h3>Phase 2 탐색 코호트 개시</h3>
    <p>동일 혈장에서 p-tau217 면역측정 + 메틸화 패널 병행 수집</p>
    <p class="ms__tag">확장</p>
  </li>
</ol>
<div class="caution">
  <p>
    M1이 실패하면 파이프라인의 2단계를 표준 원심분리 또는 혈장분리 카드로
    교체합니다. 원가는 오르지만 <b>사업 가설 자체는 유지됩니다.</b>
  </p>
</div>

<h3 class="sub">1996 &rarr; 2026</h3>
<figure class="thesis">
  <blockquote>
    20년 전에, 발판 위에 10초만 서 있으면 체지방량과 근육량을 다 알 수 있다고
    하면 믿으셨겠습니까?
  </blockquote>
</figure>
<div class="stats">
  <div class="stat"><b class="num">109</b><span>인바디 진출 국가</span></div>
  <div class="stat"><b class="num">20,000</b><span>국내 설치처</span></div>
  <div class="stat"><b class="num">2억</b><span>클라우드 축적 체성분 데이터 건수</span></div>
  <div class="stat"><b class="num">6,500</b><span>전 세계 체성분 논문 17,000편 중 인바디 사용</span></div>
</div>
<div class="prose">
  <p>
    1996년, 체지방을 재려면 물탱크에 잠수하거나 X선 촬영실로 가야 했습니다. 30년
    뒤 오늘, ‘인바디 재러 간다’는 회사 이름이 아니라 동사가 됐습니다.
  </p>
  <p><b>몸은 이미 정량화됐습니다. 다음은 정신입니다.</b></p>
</div>
"""
    + src("인바디 공식 IR 및 연혁(2025년 매출 2,339억 원) · 의학신문 2026-05-26")
)


# ────────────────────────────────────────────────────────────── manifest

SECTIONS = [
    {"id": "hero", "label": "개요", "cls": "sec sec--hero", "html": HERO},
    {"id": "stakes", "label": "문제", "cls": "sec", "html": STAKES},
    {"id": "people", "label": "세 사람", "cls": "sec", "html": PEOPLE},
    {"id": "proof", "label": "문턱", "cls": "sec", "html": PROOF},
    {"id": "flow", "label": "솔루션", "cls": "sec", "html": FLOW},
    {"id": "kit", "label": "키트", "cls": "kitscroll", "html": KIT},
    {"id": "evidence", "label": "근거", "cls": "sec", "html": EVIDENCE},
    {"id": "model", "label": "모델", "cls": "sec", "html": MODEL},
    {"id": "limits", "label": "한계", "cls": "sec", "html": LIMITS},
    {"id": "roadmap", "label": "로드맵", "cls": "sec", "html": ROADMAP_SEC},
    {"id": "market", "label": "시장", "cls": "sec", "html": MARKET},
    {"id": "georgia", "label": "비치헤드", "cls": "sec", "html": GEORGIA},
    {"id": "milestones", "label": "마일스톤", "cls": "sec", "html": MILESTONES},
]

# The worldmap and roadmap grid belonged to the old liver-cancer positioning and
# are not in the deck; nothing here needs a post-render script.
PAGE_SCRIPTS = ""

FOOTER = """
<p class="footer__note">
  모든 수치는 2026년 7월 기준으로 원출처를 확인했습니다. 동료심사 전
  발표(NHS-Galleri, PATHFINDER 2)와 preprint(MethylGPT, CpGPT)는 본문에 그 사실을
  명시했습니다. 페이퍼 퓨지 혈장의 cfDNA 품질은 아직 검증 전이며 M1의 대상입니다.
  본 페이지는 팀 프로젝트 산출물이며 의료적 조언을 제공하지 않습니다.
</p>
"""
