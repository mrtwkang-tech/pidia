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
from content import assumption, gloss, head, lede, src, stat

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
        "<em>the test is expensive, watched, or does not exist</em>",
    )
    + lede(
        "Without insurance a single colonoscopy runs into the thousands. Some tests "
        "go untaken because of what their name alone would mark you as. And "
        "depression still has no blood test to measure."
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
    + gloss(("Early detection", "Finding a cancer before it spreads. Found late, survival falls sharply"))
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
    + lede("The names are pseudonyms. Every number is a real statistic.")
    + """
<div class="cards cards--3">
  <article class="card">
    <p class="card__tag">Expensive &middot; Cost</p>
    <h3>Michael, <span class="num">58</span></h3>
    <p class="card__sub">Columbus, Georgia &middot; uninsured</p>
    <blockquote class="quote">It was stage three. I beat it. I am still paying for it.</blockquote>
    <p class="card__body">Diagnosed with stage III colorectal cancer. Cured, financially ruined, and living with the risk of recurrence.</p>
    <ul class="reasons">
      <li><b class="num">$2,750</b> one uninsured colonoscopy</li>
      <li><b class="num">36%</b> of US adults delayed needed care because of cost</li>
    </ul>
  </article>
  <article class="card">
    <p class="card__tag">Watched &middot; Stigma</p>
    <h3>Kofi, <span class="num">34</span></h3>
    <p class="card__sub">Africa &middot; living with HIV</p>
    <blockquote class="quote">Someone knowing I took that test — that is the part I am afraid of.</blockquote>
    <p class="card__body">She knows something is wrong. There is no money for a clinic, and a test with “HIV” in its <b>name</b> is a threshold of its own.</p>
    <ul class="reasons">
      <li><b class="num">$69</b> an HIV test already comes to the door — for <b>one analyte</b></li>
      <li><b class="num">0</b> draw centres a test that ends at the mailbox requires</li>
    </ul>
  </article>
  <article class="card">
    <p class="card__tag">Unmeasurable &middot; Measurability</p>
    <h3>Jihyun, <span class="num">29</span></h3>
    <p class="card__sub">Office worker &middot; 8 months of depressive symptoms</p>
    <blockquote class="quote">With diabetes you show them a number. I have nothing to show.</blockquote>
    <p class="card__body">A person with diabetes can ask for accommodation with one HbA1c figure. Jihyun has no such figure.</p>
    <ul class="reasons">
      <li><b class="num">15%</b> of workers have told a manager about a mental health problem</li>
      <li><b class="num">0</b> objective blood markers in clinical use for depression</li>
    </ul>
  </article>
</div>
"""
    + src(
        "KFF Health Tracking Poll 2025-05 · NAMI/Ipsos 2026-03 · "
        "Abi-Dargham A et al., World Psychiatry 2023;22:236-262 · "
        "Self-test pricing from each company's published pages (checked 2026-07)"
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
    <p class="card__tag">Watched &rarr; the mailbox</p>
    <p>Nobody walks into a clinic, so nobody sees the walk. Stabilising tubes hold for 3–5 days at ambient temperature, so the lab goes to the person.</p>
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
    + gloss(("cfDNA", "DNA fragments shed by dying cells into the blood — including a tumour's"), ("Methylation", "A chemical tag on DNA. A switch for genes, and a record of what a body has been through"), ("Paperfuge", "A centrifuge made of paper and string. Spun by hand to separate plasma"))
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

<dl class="gloss"><div><dt>MCED</dt><dd>Multi-cancer early detection — many cancers from one blood draw</dd></div><div><dt>AUC</dt><dd>Test performance. 0.5 is a coin toss, 1.0 is perfect</dd></div></dl>
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


# ──────────────────────────────────────────────────────────── 6b. model

MODEL = (
    head("Model", "What the AI does is <em>one thing</em>")
    + lede(
        "Pick, out of hundreds of thousands of CpG sites, the few that best "
        "explain the disease. Nothing more. The shape of the problem is what "
        "rules most of the candidate models out."
    )
    + gloss(("CpG", "A place in DNA where a C is followed by a G. Where methylation attaches — tens of millions of them in a human genome"))
    + '<h3 class="sub">From blood to a matrix</h3>'
    + """
<ol class="flow flow--4">
  <li><b class="num">01</b><h3>Bisulfite conversion</h3><p>Unmethylated C &rarr; U (read as T) · methylated 5mC stays C</p></li>
  <li><b class="num">02</b><h3>Beadchip hybridisation</h3><p>A complementary probe per CpG site · Type I/II</p></li>
  <li><b class="num">03</b><h3>Single-base extension</h3><p>The base that attaches decides the fluorescent channel</p></li>
  <li><b class="num">04</b><h3>Beta value</h3><p>&beta; = M / (M + U + 100) · between 0 and 1</p></li>
</ol>
<div class="paper">
  <p class="paper__cite">The input matrix — rows are people, columns are the <span class="num">&beta;</span> of each CpG site, the label is disease status</p>
  <p class="paper__note">
    <b class="num">Hundreds of thousands</b> of columns against
    <b class="num">hundreds</b> of rows. That ratio is the whole problem, and it
    has a name: <b>high dimension, low sample size.</b>
  </p>
</div>
"""
    + charts.matrix(
        180,
        5,
        [88, 89, 90, 91, 92],
        "Samples<tspan x=\"21\" dy=\"5\">hundreds</tspan>",
        "CpG sites &mdash; hundreds of thousands",
        "3–5 kept",
        "Hundreds of thousands across, hundreds down. That one ratio decides "
        "most of what can be used. The few marked columns are the entire output.",
    )
    + gloss(("&beta; value", "How methylated one CpG site is, on a scale from 0 to 1"), ("Bisulfite", "A chemical step that rewrites methylated and unmethylated sites as different letters"))
    + '<h3 class="sub">Which is why it is not deep learning</h3>'
    + """
<div class="twocol">
  <div class="twocol__col twocol__col--no">
    <p class="twocol__label">Not used</p>
    <ul class="reasons">
      <li><b>Deep learning (CNN · Transformer)</b> — with hundreds of samples against hundreds of thousands of dimensions, overfitting arrives first. And a black box is a liability in a regulatory submission</li>
      <li><b>k-NN</b> — at this many dimensions the notion of “distance” stops meaning anything</li>
    </ul>
  </div>
  <div class="twocol__col twocol__col--yes">
    <p class="twocol__label">Used</p>
    <ul class="reasons">
      <li><b>Random forest</b> — accumulating impurity decrease at every split gives a <b>variable importance</b> ranking. Bootstrapping keeps one outlier from steering it, and the tree structure catches non-linearity and interaction without being told to</li>
      <li><b>Elastic-Net</b> — L1's feature selection with L2's even contribution. The point is the <b>group effect</b>: co-methylated CpGs are kept together or dropped together. LASSO alone keeps one of them at random</li>
      <li><b>Logistic regression</b> — for the <b>final panel</b>, once it is down to three to five markers. The coefficients have to be explainable for the submission to be a submission</li>
    </ul>
  </div>
</div>
"""
    + src(
        "Zou H &amp; Hastie T, J R Stat Soc B 2005;67:301-320 (Elastic-Net) · "
        "Breiman L, Machine Learning 2001;45:5-32 (Random Forest) · "
        "&beta; as defined by the Illumina Infinium assay"
    )
    + '<h3 class="sub">The most expensive lesson in this field</h3>'
    + charts.gapbars(
        ("Batch-wise processed data", 0.76, "AUC 0.76"),
        ("Held out, after harmonisation", 0.57, "AUC &lt;0.57"),
        "Same data, same models. Every cohort, run and lab leaves a technical "
        "fingerprint, and when cases and controls sit unevenly across batches the "
        "model learns <b>the batch, not the biology.</b> Across 6 cohorts, 8 "
        "batches and 12 strategies, not one of the 1,987 nominally significant "
        "CpGs survived every batch.",
        lead="",
    )
    + charts.batches(
        [
            [(14 + (i % 4) * 9, 13 + (i // 4) * 12, i % 2) for i in range(12)],
            [(56 + (i % 4) * 9, 13 + (i // 4) * 12, i % 3 == 0) for i in range(12)],
        ],
        "Coloured by batch",
        "Coloured by disease",
        "The same points in the same places. Only the colouring rule changed. "
        "Asked to separate them, a model finds the left picture every time.",
        "A schematic. Not real coordinates — a picture of why a batch effect "
        "looks like performance",
    )
    + '<div class="caution">'
    + '<p class="caution__label">So, our rule</p>'
    + "<p>Until a cohort collected independently, elsewhere, has passed batch "
    + "correction and a held-out validation, <b>we will not state an AUC.</b></p></div>"
    + gloss(("Batch", "Data processed at the same time in the same lab"), ("Harmonisation", "Correcting data from different batches onto one scale"), ("Hold-out", "Data never used in training. Opened exactly once, at the end"))
    + '<h3 class="sub">Settled before the model is named</h3>'
    + """
<ol class="method">
  <li>
    <h3>What is being predicted</h3>
    <p>A separate model per disease. Cancer, neurodegeneration and chronic stress have different kinds of ground truth, so they do not share a model.</p>
  </li>
  <li>
    <h3>What the ground truth is</h3>
    <p>Histopathology for cancer; neurologist diagnosis with MRI/PET for neurodegeneration; standardised instruments and follow-up for stress. <b>The reliability of the label is the ceiling on model performance.</b></p>
  </li>
  <li>
    <h3>Who the controls are</h3>
    <p>Not healthy volunteers — people from the same risk group who did not convert during follow-up. With healthy controls the model learns risk-group membership, not disease.</p>
  </li>
  <li>
    <h3>What is being controlled for</h3>
    <p>Age, sex, medication, blood cell composition (cell-type deconvolution), batch. Without adjustment the model learns age rather than disease.</p>
  </li>
  <li>
    <h3>How often the validation set is opened</h3>
    <p>Once. Querying it repeatedly and adjusting is tuning, not validation. Repeat samples from one person all stay on the same side of the split.</p>
  </li>
</ol>
"""
    + '<h3 class="sub">What methylation is actually best at</h3>'
    + lede(
        "Methylation's most successful application is not diagnosis. It is "
        "<b>estimating age</b> — and the lineage of those clocks says exactly what "
        "we can and cannot claim in Phase 3."
    )
    + """
<div class="compare__scroll">
  <table class="ctable">
    <thead><tr><th scope="col">Clock</th><th scope="col">Generation</th><th scope="col">Trained on</th><th scope="col">Size</th></tr></thead>
    <tbody>
      <tr><th scope="row">Horvath</th><td class="num">1st</td><td>Chronological age · multi-tissue</td><td class="num">353 CpG</td></tr>
      <tr><th scope="row">Hannum</th><td class="num">1st</td><td>Chronological age · blood</td><td class="num">71 CpG</td></tr>
      <tr><th scope="row">PhenoAge</th><td class="num">2nd</td><td>Mortality risk from clinical phenotypes</td><td class="num">513 CpG</td></tr>
      <tr class="ctable__ours"><th scope="row">GrimAge</th><td class="num">2nd</td><td>Mortality + 7 plasma proteins + pack-years</td><td>Best at predicting death</td></tr>
      <tr class="ctable__ours"><th scope="row">DunedinPACE</th><td class="num">3rd</td><td><b>Pace</b> of ageing · longitudinal</td><td>Biological years per year</td></tr>
    </tbody>
  </table>
</div>
<div class="caution">
  <p class="caution__label">The signal appears in a specific place</p>
  <p>
    Psychiatric burden scores were significantly associated with acceleration
    <b>only in the 2nd and 3rd generation clocks</b> (adjusted R&sup2;
    <b class="num">0.22</b> and <b class="num">0.33</b>). Nothing in the 1st
    generation, which is trained on chronological age. The reading that fits the
    data is not that psychiatric illness ages you faster, but that it
    <b>accumulates health damage.</b>
  </p>
</div>
<div class="caution caution--rule">
  <p class="caution__label">Which is why we do not use a clock as our metric</p>
  <p>
    GrimAge has <b>pack-years built into it.</b> A large share of any
    “depression → GrimAge acceleration” may simply be smoking. Direction flips
    with ancestry, and in the 1st generation cell composition explains much of
    the variance. Nothing here is usable without population-specific
    recalibration.
  </p>
</div>
"""
    + '<h3 class="sub">So we measure exposure, not the disease</h3>'
    + lede(
        "Instead of hunting for a methylation marker of depression, use the "
        "<b>methylation signature of its risk factors</b> — each of which has "
        "already been validated in samples tens of thousands strong."
    )
    + """
<div class="paper paper--lead">
  <p class="paper__cite">prediction = <i>f</i>( MS<sub>smoking</sub>, MS<sub>BMI</sub>, MS<sub>alcohol</sub>, MS<sub>education</sub>, MS<sub>HDL</sub>, MS<sub>cholesterol</sub> )</p>
  <p class="paper__note">
    It redefines methylation from “a marker of the disease” into
    <b>a biological archive of environmental exposure.</b>
  </p>
  <p class="src">Barbu MC et al., 2022 — surrogate trait scores</p>
</div>
<figure class="thesis thesis--inline">
  <blockquote>
    People under-report how much they smoke.<br />AHRR methylation does not.
  </blockquote>
</figure>
<div class="prose">
  <p>
    An <b>exposure measurement that bypasses self-report.</b> That is the use of
    methylation the current evidence actually supports, and it is why our Phase 3
    is “a molecular record of cumulative stress exposure” rather than “a
    diagnosis of depression”.
  </p>
</div>
"""
    + src(
        "Horvath S, Genome Biol 2013;14:R115 · Hannum G et al., Mol Cell 2013;49:359-367 · "
        "Levine ME et al., Aging 2018;10:573-591 (PhenoAge) · Lu AT et al., Aging "
        "2019;11:303-327 (GrimAge) · Belsky DW et al., eLife 2022;11:e73420 "
        "(DunedinPACE) · Barbu MC et al., 2022"
    )
    + '<h3 class="sub">Prevalence outweighs accuracy</h3>'
    + charts.gapbars(
        ("Psychiatric clinic (40% prevalence)", 66.7, "PPV 66.7%"),
        ("General population (5% prevalence)", 13.6, "PPV 13.6%"),
        "The <b>same test</b>, at 75% sensitivity and 75% specificity both times. "
        "Only the prevalence changed. Run a psychiatric biomarker as a "
        "population screen and 86 of every 100 positives are false. That is why "
        "our Phase 3 quantifies <b>exposure</b> rather than diagnosing.",
    )
    + assumption(
        "A worked example at 75% sensitivity and specificity, run at 5% and 40% "
        "prevalence. Not the measured performance of any particular test — a "
        "demonstration of how Bayes' rule behaves on this problem"
    )
    + src(
        "Sales AJ et al., Acta Neuropsychiatr 2021;33:217-241 · "
        "Barbu MC et al., 2021 — penalised regression explained 1.75% of depression variance · "
        "Translational Psychiatry 2024 — 6 cohorts · 8 batches · 12 strategies "
        "(all classifiers AUC &lt;0.57 after harmonisation)"
    )
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
    + gloss(("PPV", "Given a positive result, the chance it is real"), ("Stage I", "The earliest stage of a cancer — and the hardest to find"))
    + '<h3 class="sub">What that looks like counted out</h3>'
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
<h3 class="sub">Which leaves a band empty</h3>
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
        "tag": "12.0% uninsured · 53 counties, no hospital",
        "role": "Beachhead · 0–2 yr",
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
        "tag": "SAM $1.75B · 106.7 M aged 50–79",
        "role": "Expansion · 2–4 yr",
        "region": "usa",
        "paint": 0,
        "lon": -98.35,
        "lat": 39.50,
        "r": 3.4,
        "nudge": (0.0, -13.0),
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
        "tag": "No cold chain · 0 draw centres",
        "role": "NGO channel · 4 yr +",
        "region": "africa",
        "paint": 1,
        "lon": 21.0,
        "lat": 2.0,
        "r": 3.4,
        "nudge": (15.0, 7.0),
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
        "tag": "National screening · IVD pathway",
        "role": "Development · IP base",
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
    + '<h3 class="sub">In that order, on the map</h3>'
    + charts.wmap(
        STOPS,
        "Territory filling in stage by stage on a world map — one US state, then "
        "the United States, then Africa, then Korea",
        legend=("Territory accumulates", "Dashed where new logistics are needed"),
    )
    + """
"""
    + gloss(("CLIA", "US clinical laboratory certification. Required before a result can be used in care"), ("LDT", "A test a lab develops and runs only in-house. A different regulatory path"), ("ddPCR", "A method that counts DNA fragments one at a time"))
    + """
<h3 class="sub">Four validations, one at a time</h3>
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
    {"id": "model", "label": "Model", "cls": "sec", "html": MODEL},
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
