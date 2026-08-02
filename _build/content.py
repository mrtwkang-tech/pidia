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

# The entry sequence, in the order it is walked. Stop 03 is reached through the
# beachhead rather than around it: MAP International, which supplies medicines to
# the developing world, is headquartered in Georgia, so the Africa leg leaves
# from the same state the pilot runs in.
STOPS = [
    {
        "seq": "01",
        "name": "조지아",
        "role": "비치헤드 — 단일 주에서 시작합니다",
        "lon": -84.39,
        "lat": 33.75,
        "note": "애틀랜타",
        "kind": "plan",
        "nudge": (-7.4, 3.4),
        "sats": [],
        "kpi": ["M2 파일럿 n=500", "SOM $27M ARR (5년차)"],
    },
    {
        "seq": "02",
        "name": "미국 대도시",
        "role": "동일 물류 · 동일 패널로 확장",
        "lon": -98.35,
        "lat": 39.50,
        "note": "뉴욕 · 시카고 · LA · 휴스턴",
        "kind": "plan",
        "r": 13,
        "nudge": (-1.8, -15.0),
        "sats": [
            (-74.01, 40.71, "뉴욕"),
            (-87.63, 41.88, "시카고"),
            (-118.24, 34.05, "LA"),
            (-95.37, 29.76, "휴스턴"),
        ],
        "kpi": ["SAM $1.75B", "CLIA 랩 파트너십 · LDT 경로"],
    },
    {
        "seq": "03",
        "name": "아프리카",
        "role": "국제기구 채널 — 채혈센터가 없는 곳이 가장 큰 문턱입니다",
        "lon": 36.82,
        "lat": -1.29,
        "note": "나이로비 · 라고스 · 요하네스버그",
        "kind": "plan",
        "nudge": (2.8, 1.6),
        "sats": [(3.38, 6.52, "라고스"), (28.05, -26.20, "요하네스버그")],
        "kpi": ["상온 반송 · 콜드체인 불필요", "MAP International 본사가 조지아"],
    },
    {
        "seq": "04",
        "name": "한국",
        "role": "개발 · IP 거점으로의 복귀",
        "lon": 126.98,
        "lat": 37.57,
        "note": "서울",
        "kind": "plan",
        "nudge": (2.8, 1.6),
        "sats": [],
        "kpi": ["국가암검진 채널", "체외진단의료기기 인허가"],
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
    + charts.wmap(
        STOPS,
        "세계지도 위의 시장 진입 순서 — 조지아에서 미국 대도시로, 아프리카를 거쳐 한국까지",
    )
    + """
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
