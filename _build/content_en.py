#!/usr/bin/env python3
"""The English page, section for section against content.py.

The markup helpers are imported rather than restated: they are the shape of an
element, not a language. Everything below is words.

Numbers, citations, journal names and DOIs are carried across untouched — a
translation that rounds a figure or drops a sample size has changed the claim.
Where the Korean states a limit on the work, the English states the same limit;
that section is the reason the page is credible and softening it in translation
would be the one edit that actually costs something.

build.py refuses to build if this file and content.py disagree on the section
list, which is the failure mode a parallel translation actually has.
"""

import charts
from content import assumption, head, lede, src, stat

# ─────────────────────────────────────────────────────────────── 1. hero

HERO = """
<p class="eyebrow">cfDNA methylation &middot; Self-collection &middot; Georgia</p>
<h1 class="hero__title">Removing the<br />threshold to<br /><em>getting tested</em></h1>
<p class="hero__lede">
  Multi-omics read from a few drops of blood. No draw centre, no appointment, no
  prior authorisation — it starts at home. Cancer first, then the brain, then the
  mind: the same plasma, with only the panel swapped.
</p>
<figure class="thesis">
  <blockquote>We do not fight GRAIL on accuracy.<br />We fight on reach.</blockquote>
</figure>
"""

# ────────────────────────────────────────────────────────────── 2. stakes

STAKES = (
    head(
        "The problem",
        "People do not die for want of the technology. They die because "
        "<em>the test is expensive, far away, or does not exist</em>",
    )
    + lede(
        "Without insurance a single colonoscopy runs into the thousands. Rural "
        "counties have no hospital to be screened in at all. For mental health "
        "the threshold starts with saying it out loud at work — and depression "
        "still has no blood test to measure."
    )
    + '<div class="stats stats--lead">'
    + stat(
        "5,940,000",
        "people who did not die of the five major US cancers over 45 years",
        "1975–2020",
    )
    + "</div>"
    + """
<div class="split">
  <div class="split__bar">
    <span class="split__seg split__seg--a" style="--w: 80%"><b class="num">80%</b>Prevention &middot; early detection</span>
    <span class="split__seg" style="--w: 20%"><b class="num">20%</b>Treatment</span>
  </div>
  <p class="split__note">4.75 million of them lived because it was found earlier, not because of a new drug.</p>
</div>
"""
    + src(
        "Goddard KAB et al. JAMA Oncology 2025;11(2):162-167 · NCI CISNET modelled "
        "estimate, five cancers (lung, breast, colorectal, prostate, cervical)"
    )
    + '<h3 class="sub">So even the tests that already exist reach almost no one</h3>'
    + '<div class="stats">'
    + stat(
        "18.7%", "of those eligible for lung cancer screening are screened", "1 in 5"
    )
    + stat(
        "73%",
        "of US adults are behind on at least one routine cancer screening",
        "n = 7,510",
    )
    + stat(
        "62,110",
        "additional 5-year survivors if every eligible person were simply screened",
        "~12,400 a year",
    )
    + "</div>"
    + src(
        "American Cancer Society / JAMA 2025-11-19 (2024 NHIS, 12.76 M eligible) "
        "· Prevent Cancer Foundation 2026 Early Detection Survey (7,510 adults)"
    )
)

# ────────────────────────────────────────────────────────────── 3. people

PEOPLE = (
    head("Three people", "The threshold shows up with three faces")
    + """
<div class="cards cards--3">
  <article class="card">
    <p class="card__tag">Expensive &middot; Cost</p>
    <h3>Marcus, <span class="num">58</span></h3>
    <p class="card__sub">Columbus, Georgia &middot; uninsured</p>
    <blockquote class="quote">A colonoscopy? For me that is <span class="num">$2,750</span>.</blockquote>
    <ul class="reasons">
      <li><b class="num">36%</b> of US adults delayed needed care because of cost</li>
      <li><b class="num">75%</b> the same figure among uninsured adults</li>
    </ul>
  </article>
  <article class="card">
    <p class="card__tag">Far away &middot; Distance</p>
    <h3>Daniel, <span class="num">34</span></h3>
    <p class="card__sub">Rural Georgia county &middot; high HIV risk</p>
    <blockquote class="quote">One test is a four-hour round trip.</blockquote>
    <ul class="reasons">
      <li><b class="num">53</b> Georgia counties with no hospital at all</li>
      <li><b class="num">92 M</b> Americans living in a primary care shortage area</li>
    </ul>
  </article>
  <article class="card">
    <p class="card__tag">Unmeasurable &middot; Measurability</p>
    <h3>Jihyun, <span class="num">29</span></h3>
    <p class="card__sub">Office worker &middot; 8 months of depressive symptoms</p>
    <blockquote class="quote">I know something is wrong. What do I tell my employer?</blockquote>
    <ul class="reasons">
      <li><b class="num">15%</b> of workers have told a manager about a mental health problem</li>
      <li><b class="num">0</b> objective blood markers in clinical use for depression</li>
    </ul>
  </article>
</div>
"""
    + src(
        "KFF Health Tracking Poll 2025-05 · Georgia Rural Health Transformation (state) "
        "· HRSA State of the Primary Care Workforce 2025 · NAMI/Ipsos 2026-03 "
        "· Abi-Dargham A et al., World Psychiatry 2023;22:236-262"
    )
)

# ─────────────────────────────────────────────────────────────── 4. proof

PROOF = (
    head(
        "This is a threshold problem",
        "The best technology in the world reached <em>0.17 people in 100</em>",
    )
    + lede(
        "GRAIL's Galleri finds more than 50 cancers from a single blood draw. "
        "99.5% specificity, and more than two billion dollars invested. It is "
        "the best there is."
    )
    + charts.dotfield(
        1000,
        2,
        50,
        "US adults aged 50–79 who took Galleri",
        "0.17%",
        "1.7 people in 1,000 · 185,000 tests in 2025 across 106.7 M people",
    )
    + '<div class="stats">'
    + stat("$949", "Galleri list price", "")
    + stat("$147M", "GRAIL revenue, FY2025", "")
    + stat("$80M", "Guardant Shield, FY2025", "")
    + "</div>"
    + '<h3 class="sub">The market is open in the reports only</h3>'
    + charts.gapbars(
        ("Market research estimate", 13.0, "$1.3B"),
        ("Actual revenue, listed companies", 2.27, "$227M"),
        "The gap between the market as reported and the money actually billed. "
        "What is left is not an accuracy problem. It is a threshold problem.",
    )
    + src(
        "GRAIL FY2025 results (2026-02-19) · Guardant Health FY2025 · "
        "U.S. Census ACS 2019-2023 (106.7 M US adults aged 50–79) · "
        "Grand View Research / GM Insights MCED market estimates"
    )
)

# ─────────────────────────────────────────────── 5. kit (pinned scrub)

KIT = """
<div class="kitscroll__pin">
  <header class="sec__head sec__head--stage">
    <p class="kicker">How it works</p>
    <h2 class="sec__title">From home to report</h2>
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
    <button class="stepbtn" data-dir="-1" type="button" aria-label="Previous step">&#8592;</button>
    <ol class="stepper"></ol>
    <button class="stepbtn" data-dir="1" type="button" aria-label="Next step">&#8594;</button>
  </nav>

  <p class="stage__hint">Scroll to advance &middot; &#8592; &#8594; keys &middot; drag to rotate</p>
</div>
"""

FLOW = (
    head(
        "Solution",
        "A test you had to steel yourself for, <em>on the day you decide</em>",
    )
    + """
<ol class="flow">
  <li><b class="num">01</b><h3>Self-collection</h3><p>Stabilising tube &middot; lancet + microtube</p></li>
  <li><b class="num">02</b><h3>Paperfuge</h3><p>Plasma in 90 seconds &middot; $0.20 of hardware</p></li>
  <li><b class="num">03</b><h3>Ambient return</h3><p>Stable 3–5 days &middot; no cold chain</p></li>
  <li><b class="num">04</b><h3>cfDNA + methylation</h3><p>Targeted panel &middot; PCR readout</p></li>
  <li><b class="num">05</b><h3>ML classifier</h3><p>Multi-omics training &middot; tissue of origin</p></li>
  <li><b class="num">06</b><h3>App report</h3><p>Risk trend &middot; what to do next</p></li>
</ol>
<div class="cards cards--3">
  <article class="card">
    <p class="card__tag">Expensive &rarr; low cost</p>
    <p>Not whole-genome sequencing — only the markers already discovered, read on cheap PCR. A targeted panel and paperfuge prep bring the unit cost down.</p>
  </article>
  <article class="card">
    <p class="card__tag">Far away &rarr; shipped</p>
    <p>Stabilising collection tubes hold cfDNA yield and background variance for 3–5 days at ambient temperature. The lab goes to the person.</p>
  </article>
  <article class="card">
    <p class="card__tag">Unmeasurable &rarr; quantified</p>
    <p>The body is already a number. We extend that to the brain and the mind, read off the same plasma.</p>
  </article>
</div>
<div class="caution">
  <p class="caution__label">We will say this first</p>
  <p>
    Step 02 — whether paperfuge plasma yields analysis-grade cfDNA <b>has no
    published paper behind it.</b> That experiment is our first milestone. We
    compare yield, 167 bp fragment integrity and gDNA contamination against
    standard two-stage centrifugation, by ddPCR.
  </p>
</div>
"""
    + src(
        "Bhamla MS et al., Nature Biomedical Engineering 2017;1:0009 — paperfuge "
        "125,000 rpm / 30,000 g / $0.20 / plasma separation &lt;1.5 min · "
        "Medina Diaz I et al., PLoS ONE 2016;11:e0166354 (Streck BCT, n=60) · "
        "Sorber L et al., Cancers 2019;11:458"
    )
    + '<h3 class="sub">Prototype, measured</h3>'
    + """
<dl class="dims">
  <div><dt>Lancet pen</dt><dd class="num">&#216;25 &times; 50</dd></div>
  <div><dt>Cartridge</dt><dd class="num">&#216;12 &times; 45</dd></div>
  <div><dt>Separation disc</dt><dd class="num">&#216;65</dd></div>
  <div><dt>Return case</dt><dd class="num">105 &times; 80 &times; 26</dd></div>
</dl>
"""
    + src("Measured from the CAD prototype · millimetres")
)

# ──────────────────────────────────────────────────────────── 6. evidence

EVIDENCE = (
    head("Why cfDNA methylation", "What existing blood tests <em>cannot do</em>") + """
<div class="cards cards--3">
  <article class="card card--muted">
    <h3>PSA</h3>
    <p>AUC <b class="num">0.678</b> — “no cutoff simultaneously satisfies sensitivity and specificity” (JAMA 2005, n=8,575)</p>
  </article>
  <article class="card card--muted">
    <h3>CA-125</h3>
    <p><b class="num">200,000</b>-person RCT, <b class="num">16</b> years of follow-up — stage shifted earlier, mortality did not fall (Lancet 2021)</p>
  </article>
  <article class="card card--muted">
    <h3>CBC · CMP</h3>
    <p>No diagnostic accuracy evidence exists for early cancer detection at all</p>
  </article>
</div>

<div class="paper paper--lead">
  <p class="paper__cite">Targeted methylation MCED — specificity <span class="num">99.3%</span> · n = <span class="num">6,689</span> · more than <span class="num">100,000</span> methylation regions</p>
  <p class="paper__note">
    In a controlled comparison training and validating ten classifiers on the
    same samples, <b>whole-genome methylation performed best.</b>
  </p>
  <p class="src">Liu MC et al., Annals of Oncology 2020;31:745-759 · Jamshidi A et al., Cancer Cell 2022;40:1537-1549</p>
</div>

<h3 class="sub">Modelling approach</h3>
<ul class="facts">
  <li><b class="num">12%</b><span>Methylation array plus random forest classified roughly 100 CNS tumour types, changed up to 12% of actual diagnoses, and was adopted into the WHO classification — Capper, Nature 2018</span></li>
  <li><b class="num">10:1</b><span>Ten classifiers trained and independently validated on the same samples. Whole-genome methylation was best at tissue of origin — Jamshidi, Cancer Cell 2022</span></li>
  <li><b class="num">30M</b><span>Omics foundation models lift performance in the low-data regime — Geneformer, Nature 2023. Methylation-specific models are still preprints</span></li>
</ul>
<div class="caution caution--rule">
  <p class="caution__label">Our modelling rule</p>
  <p>
    Until a cohort collected independently, elsewhere, has passed batch
    correction and a held-out validation, <b>we will not state an AUC.</b>
  </p>
</div>
"""
)

# ────────────────────────────────────────────────────────────── 7. limits

LIMITS = (
    head("What we do not claim", "Before the panel asks, <em>we will say it first</em>")
    + lede(
        "These three are limits of the whole field, and we are not an exception to them."
    )
    + """
<ol class="method">
  <li>
    <h3>Stage I sensitivity is low</h3>
    <p>
      <b class="num">16.8–18%</b> at stage I across all cancers. The pitch is
      early detection, and the earliest point is the weakest one.
    </p>
  </li>
  <li>
    <h3>Real-world PPV was <span class="num">38%</span></h3>
    <p>
      PATHFINDER, <b class="num">6,662</b> people — of the <b class="num">92</b>
      with a positive signal, <b class="num">35</b> actually had cancer.
    </p>
  </li>
  <li>
    <h3>The large RCT missed its primary endpoint</h3>
    <p>
      NHS-Galleri, <b class="num">143,000</b> people — it did not achieve the
      primary endpoint of reducing stage III/IV diagnoses. Presented before peer review.
    </p>
  </li>
</ol>
"""
    + charts.dotfield(
        92,
        35,
        23,
        "of 92 signal positives, the ones that were really cancer",
        "38%",
        "PATHFINDER, 6,662 people · the other 57 were cleared after further work-up",
    )
    + """
<figure class="thesis thesis--inline">
  <blockquote>
    Do not believe a team that says it will out-algorithm a company with two
    billion dollars and a 100,000-person cohort. We win on reach.
  </blockquote>
</figure>
"""
    + src(
        "Klein EA et al., Annals of Oncology 2021;32:1167-1177 (n=4,077) · "
        "Schrag D et al., Lancet 2023;402:1251-1260 (PATHFINDER, n=6,662) · "
        "NHS-Galleri, presented ASCO 2026 — peer-reviewed paper not yet published"
    )
)

# ───────────────────────────────────────────────────────────── 8. roadmap

ROADMAP_SEC = (
    head("Roadmap", "Same plasma, <em>one axis at a time</em>")
    + lede(
        "The point is not to read three axes from one draw. It is that the same "
        "plasma preparation carries a different panel each time."
    )
    + """
<ol class="phases">
  <li class="phase phase--now">
    <p class="phase__no"><span class="num">PHASE 1</span> · <span class="num">0–2</span> yr</p>
    <h3>Cancer</h3>
    <p>Basic blood panel + cfDNA methylation multi-cancer screening</p>
    <p class="phase__grade">Evidence established &middot; commercially viable</p>
  </li>
  <li class="phase">
    <p class="phase__no"><span class="num">PHASE 2</span> · <span class="num">2–4</span> yr</p>
    <h3>Neurodegenerative disease</h3>
    <p>Alzheimer's &middot; Parkinson's &middot; ALS — reading the brain from blood is already FDA-cleared</p>
    <p class="phase__grade">Evidence strong &middot; modality under review</p>
  </li>
  <li class="phase">
    <p class="phase__no"><span class="num">PHASE 3</span> · <span class="num">4</span> yr +</p>
    <h3>Chronic stress, quantified</h3>
    <p>Not a psychiatric diagnosis — a molecular record of cumulative stress exposure</p>
    <p class="phase__grade">Exploratory research module</p>
  </li>
</ol>

<h3 class="sub">Put the three axes and the four milestones on one timeline</h3>
"""
    + charts.timeline(
        ["0", "6 mo", "12", "18", "24", "3 yr", "4 yr", "5 yr+"],
        [
            ("Phase 1", "Cancer", [(1, 5, "now", "cfDNA methylation, multi-cancer")]),
            (
                "Phase 2",
                "Neurodegeneration",
                [(5, 8, "next", "Alzheimer's · Parkinson's · ALS")],
            ),
            ("Phase 3", "Chronic stress", [(8, 9, "later", "Exploratory module")]),
            ("M1", "Paperfuge validation", [(1, 2, "ms ms--risk", "Highest risk")]),
            ("M2", "Georgia pilot n=500", [(2, 3, "ms", "Logistics")]),
            ("M3", "CLIA lab · LDT path", [(3, 4, "ms", "Regulatory")]),
            ("M4", "Phase 2 cohort", [(4, 5, "ms", "Expansion")]),
        ],
        caption="M1–M4 all close inside Phase 1. Phase 2 begins after that.",
    )
    + """
<h3 class="sub">Phase 2 — the premise that blood can read the brain has already cleared</h3>
<div class="twocol">
  <div class="twocol__col">
    <p class="twocol__label">Established</p>
    <ul class="facts">
      <li><b class="num">2025.05</b><span>FDA clears the first Alzheimer's blood test (Lumipulse pTau217/A&beta;42) — PPV 91.7%, NPV 97.3%, n=499</span></li>
      <li><b class="num">0.97</b><span>Plasma p-tau217 AUC in primary care. Seeing the same patients, physicians were 61% accurate against the test's 91% — JAMA 2024</span></li>
      <li><b class="num">2016</b><span>First detection of brain-derived DNA in plasma by cfDNA methylation — PNAS</span></li>
    </ul>
  </div>
  <div class="twocol__col twocol__col--caution">
    <p class="twocol__label">Still unresolved</p>
    <ul class="reasons">
      <li>AUC 0.91 in ALS — but <b class="num">n=30</b> (JCI 2026)</li>
      <li>The largest study (<b class="num">n=281</b>, Sci Rep 2025) was <b>negative</b> — no gain over serum NfL and GFAP</li>
      <li>The PNAS 2016 detection was in acute brain injury</li>
    </ul>
  </div>
</div>
<div class="caution">
  <p>
    So the Phase 2 claim is not “we will catch Alzheimer's with methylation.”
    The plasma a paperfuge produces is <b>modality-neutral</b>. The same drop
    runs a p-tau217 immunoassay today and a methylation panel tomorrow.
  </p>
</div>

<h3 class="sub">Phase 3 — deliberately conservative ground</h3>
<div class="twocol">
  <div class="twocol__col twocol__col--no">
    <p class="twocol__label">We do not claim</p>
    <p><b>A “blood test for depression” does not exist.</b></p>
    <ul class="reasons">
      <li>Reanalysing eight cohorts of methylation depression classifiers (<b class="num">n=1,942</b>), proper normalisation collapsed AUC below <b class="num">0.57</b> and held-out predictive power disappeared</li>
      <li>Serotonin transporter (SLC6A4) methylation had an effect size of <b class="num">0.06</b> across a 2,296-person meta-analysis — effectively null</li>
    </ul>
  </div>
  <div class="twocol__col twocol__col--yes">
    <p class="twocol__label">We do claim</p>
    <p><b>Methylation is the most reproducible molecular record of chronic stress <i>exposure</i>.</b></p>
    <ul class="reasons">
      <li>NR3C1 methylation increased in <b class="num">89%</b> of 40 adversity-exposure studies</li>
      <li>PGC-PTSD, 23 cohorts, <b class="num">n=5,077</b> — 11 genome-wide significant CpGs</li>
      <li>Pre-deployment methylation risk scores predicted post-deployment PTSD onset (Wani 2024)</li>
    </ul>
  </div>
</div>
<div class="prose">
  <p>
    The incumbent measure is weak too — hair cortisol, the standard for chronic
    stress, showed no consistent association with subjective stress or mood
    disorder across an <b class="num">N=10,289</b> meta-analysis. <b>Beating a weak
    incumbent on a hard problem is a reasonable claim. Having a blood test for
    depression is not.</b>
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
    head("Market", "The band we take first")
    + """
<div class="funnel">
  <div class="funnel__step" style="--w: 100%">
    <p class="funnel__tier">TAM</p>
    <p class="funnel__val num">$1.3B &rarr; $5.3B</p>
    <p class="funnel__desc">Global multi-cancer early detection (MCED), 2025 &rarr; 2035 · CAGR 14.8–17%, cross-checked across two firms</p>
  </div>
  <div class="funnel__arrow"><span>United States only</span></div>
  <div class="funnel__step" style="--w: 62%">
    <p class="funnel__tier">SAM</p>
    <p class="funnel__val num">$1.75<i>B</i></p>
    <p class="funnel__desc">US MCED $522.8M + US direct-to-consumer lab testing $1.23B</p>
  </div>
  <div class="funnel__arrow"><span>3.32 M Georgians aged 50–79 &times; 2% penetration &times; $400 ASP</span></div>
  <div class="funnel__step funnel__step--ours" style="--w: 34%">
    <p class="funnel__tier">SOM <b>year 5</b></p>
    <p class="funnel__val num">$27<i>M ARR</i></p>
    <p class="funnel__desc">Conservative case: 0.5% in year 3 = $6.6M</p>
  </div>
</div>
"""
    + assumption(
        "Penetration anchor — GRAIL sits at 0.17% US penetration at a $949 price "
        "point. Do not believe a plan that assumes 5% or more. The 2035 forecasts "
        "differ by 2.5× between firms (Fact.MR: $8.2B → $16.3B, CAGR 6.5%)"
    )
    + '<h3 class="sub">Competitive landscape</h3>'
    + charts.bars(
        [
            ("MindX Sciences", 1958, "$1,958", "Single service &middot; high cost"),
            ("Guardant Shield", 1495, "$1,495", "Colorectal screening"),
            ("GRAIL Galleri", 949, "$949", "50+ cancer MCED"),
            ("Exact Cancerguard", 689, "$689", "MCED"),
            ("TruDiagnostic", 499, "$499", "Biological age"),
            (
                "PIDIA",
                450,
                "$400–500",
                "Multi-disease methylation panel &middot; no draw centre",
            ),
            (
                "Function Health",
                365,
                "$365/yr",
                "160+ tests bundled &middot; biggest threat",
            ),
            ("myLAB Box", 189, "$189", "Self-test kit"),
            ("Everlywell HIV", 69, "$69", "Single analyte"),
        ],
        caption="Bar length is proportional to list price. The top of the market is 28× the bottom.",
        ours="PIDIA",
    )
    + """
<div class="cards">
  <article class="card card--muted">
    <p class="card__tag">Biggest threat</p>
    <h3>Function Health</h3>
    <p>160+ tests for $365 a year. $298M raised at a $2.5B valuation. They resell Galleri and Alzheimer's testing as add-ons.</p>
  </article>
  <article class="card card--lead">
    <p class="card__tag">The empty band</p>
    <h3>A multi-disease methylation panel at $400–700</h3>
    <p>Cheaper than Cancerguard, more clinical than TruDiagnostic, a quarter of MindX.</p>
  </article>
</div>
"""
    + src("Each company's published pricing and FY2025 results (checked 2026-07)")
    + '<h3 class="sub">Three things only we have</h3>'
    + """
<ol class="method">
  <li>
    <h3>Threshold — there is no draw centre</h3>
    <p>Function Health sends you to a Quest location. We end at the mailbox. In 53 Georgia counties there is no clinic to go to in the first place.</p>
  </li>
  <li>
    <h3>Extension — same plasma, different panel</h3>
    <p>Competitors add analytes. We share the preparation and change only the panel. Phase 1's logistics become Phase 2 and 3's asset.</p>
  </li>
  <li>
    <h3>Focus — we start in one state</h3>
    <p>Not the whole country. One state, so shipping temperature, regulation and the partner lab are a single controlled variable — then we expand.</p>
  </li>
</ol>
<figure class="thesis thesis--inline">
  <blockquote>We are not a team building a more accurate test. We are a team building the path a test takes to reach a person.</blockquote>
</figure>
"""
)

# ───────────────────────────────────────────────────────────── 10. georgia

GEORGIA = (
    head("Beachhead", "Why we start in <em>Georgia</em>")
    + lede(
        "All three personas live inside one state, and the entire three-phase "
        "roadmap can be validated in the same population."
    )
    + '<div class="stats">'
    + stat("471.9", "Cancer incidence per 100,000", "vs 448.6 national average · +5.2%")
    + stat("12.0%", "Uninsured · 49th of 50 states", "~1.34 M people paying cash")
    + stat("53", "Counties with no hospital at all (of 159)", "2.4 M rural residents")
    + stat("65,195", "People living with HIV", "44% aged 50+ · 2,442 new cases a year")
    + "</div>"
    + charts.deltabars(
        [
            ("Cancer incidence per 100k", "471.9", "448.6", +5.2, False),
            ("Colorectal screening rate", "69.5%", "71.1%", -2.2, False),
        ],
        "US average",
        "More cancer, less screening. A beachhead is where two indicators lean the same way.",
        axis_label="Deviation from the US average",
        subject="Georgia",
    )
    + '<h3 class="sub">The Phase 2 and 3 populations are in the same state</h3>'
    + '<div class="stats">'
    + stat("188,300", "Rural Georgians 65+ with Alzheimer's or dementia", "")
    + stat("19 : 15", "Rural vs non-rural suicide rate per 100,000", "")
    + stat("69.5%", "Colorectal screening · 32nd of 50", "US average 71.1%")
    + "</div>"
    + src(
        "NCI State Cancer Profiles (2018-2022, age-adjusted) · America's Health Rankings "
        "2024 (CDC BRFSS) · Georgia Rural Health Transformation, official state "
        "application · Georgia DPH HIV Surveillance Fact Sheet 2023"
    )
)

# ────────────────────────────────────────────────────────── 11. milestones

STOPS = [
    {
        "seq": "01",
        "name": "Georgia",
        "role": "Beachhead · 0–2 yr",
        "region": "georgia",
        "paint": 3,
        "lon": -83.44,
        "lat": 32.68,
        "r": 3.0,
        "nudge": (-7.4, 3.6),
        "jump": False,
        "bow": 0,
        "sats": [],
        "facts": [
            ("12.0%", "Uninsured · 49th of 50"),
            ("53", "Counties with no hospital / 159"),
            ("471.9", "Cancer incidence · US 448.6"),
            ("3.32 M", "Aged 50–79 · initial market"),
        ],
        "why": "We validate a product that removes the threshold in the place "
        "where the threshold is highest. All three personas live inside one "
        "state, and it is small enough to hold shipping temperature, regulation "
        "and the partner lab as a single variable. 2% penetration × $400 ASP = "
        "$27M ARR in year 5.",
    },
    {
        "seq": "02",
        "name": "United States",
        "role": "Expansion · 2–4 yr",
        "region": "usa",
        "paint": 0,
        "lon": -98.35,
        "lat": 39.50,
        "r": 3.4,
        "nudge": (-1.8, -5.6),
        "jump": False,
        "bow": 0,
        "sats": [
            (-74.01, 40.71, "New York"),
            (-87.63, 41.88, "Chicago"),
            (-118.24, 34.05, "Los Angeles"),
            (-95.37, 29.76, "Houston"),
        ],
        "facts": [
            ("106.7 M", "Aged 50–79"),
            ("$1.75B", "SAM"),
            ("$522.8M", "US MCED"),
            ("$1.23B", "US direct-to-consumer lab testing"),
        ],
        "why": "A test that ends at the mailbox needs no new logistics to cross "
        "a state line. The return rate, days in transit and temperature logs "
        "proven in Georgia carry straight into the metros. Same logistics, "
        "same panel.",
    },
    {
        "seq": "03",
        "name": "Africa",
        "role": "NGO channel · 4 yr +",
        "region": "africa",
        "paint": 1,
        "lon": 21.0,
        "lat": 2.0,
        "r": 3.4,
        "nudge": (2.9, 1.6),
        "jump": True,
        "bow": 26,
        "sats": [
            (36.82, -1.29, "Nairobi"),
            (3.38, 6.52, "Lagos"),
            (28.05, -26.20, "Johannesburg"),
        ],
        "facts": [
            ("3–5 days", "Ambient stability · no cold chain"),
            ("$0.20", "Paperfuge hardware"),
            ("0", "Draw centres required"),
        ],
        "why": "Where there is no draw centre, the threshold is at its highest. "
        "Not requiring a cold chain stops being a convenience here and becomes "
        "the condition of entry — and MAP International is headquartered in "
        "Georgia, so this leg departs from the beachhead itself.",
    },
    {
        "seq": "04",
        "name": "Korea",
        "role": "Development · IP base",
        "region": "korea",
        "paint": 2,
        "lon": 127.6,
        "lat": 36.4,
        "r": 2.6,
        "nudge": (3.0, 1.6),
        "jump": True,
        "bow": -22,
        "sats": [],
        "facts": [
            ("National screening", "An existing uptake channel"),
            ("IVD", "In-vitro diagnostic authorisation"),
        ],
        "why": "Back to where the development and the IP are. A market with a "
        "working national screening channel already in place, so the threshold "
        "problem takes a different shape than it does in the US.",
    },
]

MILESTONES = (
    head("Milestones", "We test the <em>most uncertain thing first</em>")
    + charts.milestones(
        [
            ("M1", "6 mo", "Paperfuge cfDNA quality", 46, True),
            ("M2", "12 mo", "Georgia pilot, n=500", 30, False),
            ("M3", "18 mo", "CLIA lab · LDT path", 18, False),
            ("M4", "24 mo", "Phase 2 cohort", 10, False),
        ],
        "The drop is largest at the first step. That is why the order is what it is.",
        assumption(
            "The order of the drops is the risk ranking the deck states. The "
            "heights render that ranking rather than measure it, which is why the "
            "vertical axis carries no numbers."
        ),
        axis_y="Remaining uncertainty",
        axis_x="Time &rarr;",
    )
    + charts.wmap(
        STOPS,
        "Territory filling in stage by stage on a world map — one US state, then "
        "the United States, then Africa, then Korea",
        legend=("Territory accumulates", "Dashed where new logistics are needed"),
    )
    + """
<ol class="ms">
  <li class="ms__item ms__item--risk">
    <p class="ms__no"><span class="num">M1</span> · <span class="num">6</span> months</p>
    <h3>cfDNA quality of paperfuge plasma</h3>
    <p>Against standard two-stage centrifugation — cfDNA yield / 167 bp mononucleosomal fragment integrity / gDNA contamination (ddPCR) / methylation call concordance</p>
    <p class="ms__tag">Highest risk</p>
  </li>
  <li class="ms__item">
    <p class="ms__no"><span class="num">M2</span> · <span class="num">12</span> months</p>
    <h3>Georgia pilot, n = <span class="num">500</span></h3>
    <p>Uninsured and rural population — self-collection return rate, days in transit, temperature logger data, willingness to retest</p>
    <p class="ms__tag">Logistics</p>
  </li>
  <li class="ms__item">
    <p class="ms__no"><span class="num">M3</span> · <span class="num">18</span> months</p>
    <h3>CLIA-certified lab partnership · LDT path fixed</h3>
    <p>A partnership rather than our own lab, to compress regulatory time</p>
    <p class="ms__tag">Regulatory</p>
  </li>
  <li class="ms__item">
    <p class="ms__no"><span class="num">M4</span> · <span class="num">24</span> months</p>
    <h3>Phase 2 exploratory cohort opens</h3>
    <p>p-tau217 immunoassay and methylation panel collected in parallel from the same plasma</p>
    <p class="ms__tag">Expansion</p>
  </li>
</ol>
<div class="caution">
  <p>
    If M1 fails we swap step 2 of the pipeline for standard centrifugation or a
    plasma separation card. The unit cost rises, but <b>the business hypothesis
    itself survives.</b>
  </p>
</div>

<h3 class="sub">1996 &rarr; 2026</h3>
<figure class="thesis">
  <blockquote>
    Twenty years ago, would you have believed that standing on a platform for
    ten seconds could tell you your body fat and muscle mass?
  </blockquote>
</figure>
<div class="stats">
  <div class="stat"><b class="num">109</b><span>Countries InBody operates in</span></div>
  <div class="stat"><b class="num">20,000</b><span>Installations in Korea</span></div>
  <div class="stat"><b class="num">200 M</b><span>Body composition records in the cloud</span></div>
  <div class="stat"><b class="num">6,500</b><span>Of 17,000 body composition papers worldwide, the ones using InBody</span></div>
</div>
<div class="prose">
  <p>
    In 1996, measuring body fat meant submerging yourself in a water tank or
    booking an X-ray room. Thirty years on, in Korea “going for an InBody” is a
    verb, not a company name.
  </p>
  <p><b>The body has already been quantified. The mind is next.</b></p>
</div>
"""
    + src(
        "InBody official IR and company history (FY2025 revenue ₩233.9 B) · "
        "Uihaksinmun 2026-05-26"
    )
)

# ────────────────────────────────────────────────────────────── manifest

SECTIONS = [
    {"id": "hero", "label": "Overview", "cls": "sec sec--hero", "html": HERO},
    {"id": "stakes", "label": "Problem", "cls": "sec", "html": STAKES},
    {"id": "people", "label": "Three people", "cls": "sec", "html": PEOPLE},
    {"id": "proof", "label": "Threshold", "cls": "sec", "html": PROOF},
    {"id": "flow", "label": "Solution", "cls": "sec", "html": FLOW},
    {"id": "kit", "label": "Kit", "cls": "kitscroll", "html": KIT},
    {"id": "evidence", "label": "Evidence", "cls": "sec", "html": EVIDENCE},
    {"id": "limits", "label": "Limits", "cls": "sec", "html": LIMITS},
    {"id": "roadmap", "label": "Roadmap", "cls": "sec", "html": ROADMAP_SEC},
    {"id": "market", "label": "Market", "cls": "sec", "html": MARKET},
    {"id": "georgia", "label": "Beachhead", "cls": "sec", "html": GEORGIA},
    {"id": "milestones", "label": "Milestones", "cls": "sec", "html": MILESTONES},
]

PAGE_SCRIPTS = ""

FOOTER = """
<p class="footer__note">
  Every figure was checked against its original source as of July 2026.
  Pre-peer-review presentations (NHS-Galleri, PATHFINDER 2) and preprints
  (MethylGPT, CpGPT) are marked as such in the text. The cfDNA quality of
  paperfuge plasma is not yet validated and is the subject of M1. This page is a
  team project output and does not provide medical advice.
</p>
"""
