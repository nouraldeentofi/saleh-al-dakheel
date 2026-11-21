# -*- coding: utf-8 -*-
"""Every word on Saleh's site, in Arabic and English, in one place.

Each text is T("عربي", "English"). Facts come only from brief.md.
Small markup the build understands:
  [[18]]   a number that counts up when it scrolls into view ([[40+]] keeps the +)
  A trailing "." on a title becomes the animated full stop.
Latin words and numbers inside Arabic text are wrapped in dir="ltr" by the build.
"""

def T(ar, en):
    return {"ar": ar, "en": en}

# ------------------------------------------------------------------ CONFIG
CONFIG = {
    # The live address. Canonical, hreflang, sitemap and og tags are built from it.
    # Later, with his own domain: "https://salehaldakheel.com/"
    "BASE_URL": "https://nouraldeentofi.github.io/saleh-al-dakheel/",
    # Preview he has not approved yet: True = <meta name="robots" content="noindex"> on every page.
    "PREVIEW": True,
    # Photo path inside site/assets/img (square, 800 px or more). Empty = the «ص.» monogram.
    "PHOTO": "",
    "EMAIL": "Saleh.h.aldakheel@gmail.com",
    "PHONE": "",       # e.g. "+966 5x xxx xxxx" (empty = hidden)
    "WHATSAPP": "",    # digits only, e.g. "9665xxxxxxxx" (empty = hidden)
    "LINKEDIN": "https://www.linkedin.com/in/saleh-al-dakheel/",
    "MAKER": "https://nouraldeentofi.com",
    "DOMAIN": "",      # custom domain for GitHub Pages (writes CNAME when set)
}

PERSON = {
    "name": T("صالح الدخيل", "Saleh Al Dakheel"),
    "mono": T("ص", "S"),
    "role_short": T("مدير مشاريع في EPMO", "Projects Manager, EPMO"),
    "role": T("مدير مشاريع في مكتب إدارة المشاريع المؤسسي (EPMO) بوزارة الموارد البشرية والتنمية الاجتماعية",
              "Projects Manager, EPMO, at the Ministry of Human Resources and Social Development"),
    "city": T("الرياض، المملكة العربية السعودية", "Riyadh, Saudi Arabia"),
    "alternate_names": [
        "صالح الدخيل", "صالح الدخيّل", "الدخيل",
        "Saleh Al Dakheel", "Saleh Al-Dakheel", "Saleh AlDakheel", "Saleh Aldakheel",
        "Saleh H. Aldakheel", "Saleh H. Al Dakheel", "Salih Al Dakheel", "Saleh Al Dakhil",
        "Saleh Dakheel", "Saleh Aldakhil",
    ],
}

NAV = [
    ("index", T("الرئيسية", "Home")),
    ("career", T("المسيرة", "Career")),
    ("consulting", T("الاستشارات", "Consulting")),
    ("approach", T("المنهج", "Approach")),
    ("credentials", T("الشهادات", "Credentials")),
    ("contact", T("تواصل", "Contact")),
]

UI = {
    "skip": T("تخطَّ إلى المحتوى", "Skip to content"),
    "menu": T("القائمة", "Menu"),
    "menu_close": T("إغلاق القائمة", "Close menu"),
    "close": T("إغلاق", "Close"),
    "pages": T("الصفحات", "Pages"),
    "nav_main": T("التنقل الرئيسي", "Main navigation"),
    "nav_foot": T("صفحات الموقع", "Site pages"),
    "nav_menu": T("قائمة الصفحات", "Page menu"),
    "lang_to": T("English", "العربية"),
    "lang_label": T("Read this page in English", "اقرأ هذه الصفحة بالعربية"),
    "email_me": T("راسلني", "Email me"),
    "copy": T("انسخ البريد", "Copy email"),
    "copied": T("نُسخ البريد", "Email copied"),
    "write": T("اكتب رسالة", "Write an email"),
    "linkedin_open": T("حسابي على لينكدإن", "My LinkedIn profile"),
    "linkedin": T("لينكدإن", "LinkedIn"),
    "email": T("البريد", "Email"),
    "city": T("المدينة", "City"),
    "show": T("عرض التفاصيل", "Show details"),
    "hide": T("إخفاء التفاصيل", "Hide details"),
    "next": T("الصفحة التالية", "Next page"),
    "today": T("اليوم", "Today"),
    "valid_until": T("سارية حتى", "Valid until"),
    "prev_card": T("القيمة السابقة", "Previous value"),
    "next_card": T("القيمة التالية", "Next value"),
    "sheet": T("الورقة", "Sheet"),
    "made": T("تصميم وتطوير نور الدين طفي", "Design and development by"),
    "rights": T("صالح الدخيل", "Saleh Al Dakheel"),
    "top": T("إلى أعلى الصفحة", "Back to top"),
}

# ------------------------------------------------------------------ HOME
HOME = {
    "title": T("صالح الدخيل | مدير مشاريع في EPMO بوزارة الموارد البشرية والتنمية الاجتماعية",
               "Saleh Al Dakheel | Projects Manager, EPMO, Ministry of Human Resources and Social Development"),
    "desc": T("صالح الدخيل، مدير مشاريع في مكتب إدارة المشاريع المؤسسي بوزارة الموارد البشرية والتنمية الاجتماعية في الرياض. يقود 18 مشروعًا نشطًا في برنامج سخاء. PMP وPMI-PMOCP، ومهندس كيميائي من جامعة الملك فهد للبترول والمعادن.",
              "Saleh Al Dakheel, Projects Manager at the EPMO of Saudi Arabia's Ministry of Human Resources and Social Development in Riyadh. Leads 18 active projects in the Sakhaa Program. PMP and PMI-PMOCP; chemical engineer from KFUPM."),
    "name": T("صالح الدخيل.", "Saleh Al Dakheel."),
    "motto": [T("دائمًا أتعلّم.", "Always learning."), T("دائمًا أبني.", "Always building."), T("دائمًا أرفع السقف.", "Always aiming higher.")],
    "role": T("مدير مشاريع في مكتب إدارة المشاريع المؤسسي (EPMO) بوزارة الموارد البشرية والتنمية الاجتماعية، في الرياض.",
              "Projects Manager in the EPMO of the Ministry of Human Resources and Social Development, in Riyadh."),
    "cta1": T("اقرأ مسيرتي كجدول زمني", "Read my career as a schedule"),
    "cta2": T("راسلني على البريد", "Email me"),
    "dots_title": T("برنامج سخاء، اليوم.", "Sakhaa Program, today."),
    "dots_lead": T("18 مشروعًا نشطًا أقودها", "18 active projects I lead"),
    "dots_over": T("82 أشرف على تمكينها", "82 whose enablement I oversee"),
    "dots_aria": T("رسم بالنقاط: 18 نقطة ممتلئة للمشاريع النشطة التي يقودها، و82 دائرة للمشاريع التي يشرف على تمكينها في برنامج سخاء.",
                   "Dot drawing: 18 solid dots for the active projects he leads and 82 rings for the projects whose enablement he oversees in the Sakhaa Program."),

    "job_title": T("من المانح إلى التقرير التنفيذي.", "From donor to executive update."),
    "job_lead": T("برنامج سخاء مبادرة من وزارة الموارد البشرية والتنمية الاجتماعية، متوائمة مع رؤية 2030، لمشاريع تنمية مستدامة يرعاها مانحون. فيه أقود [[18]] مشروعًا نشطًا، وأشرف على تمكين [[82]]، منذ يوليو 2026.",
                  "The Sakhaa Program is HRSD's Vision 2030-aligned initiative for donor-sponsored sustainable development projects. Since July 2026 I lead [[18]] active projects in it and oversee the enablement of [[82]]."),
    "tabs": [
        {"id": "gov", "icon": "gov", "label": T("الحوكمة", "Governance"),
         "text": T("أطبّق معايير الحوكمة ومنهجيات EPMO وقوالبه على المشاريع كلها.", "I apply EPMO governance standards, methodologies and templates across projects.")},
        {"id": "donors", "icon": "donor", "label": T("المانحون", "Donors"),
         "text": T("أدير العلاقة مع المانحين والجهات الحكومية، وأوفّق بين توقعاتهم وخطط التسليم.", "I manage donor and government relationships, aligning expectations and delivery plans.")},
        {"id": "risk", "icon": "risk", "label": T("المخاطر", "Risk"),
         "text": T("أتابع الالتزامات والمعالم ومخاطر المحفظة، وأصعّد المشكلات مبكرًا.", "I track commitments, milestones and portfolio risks, and escalate issues early.")},
        {"id": "report", "icon": "report", "label": T("التقارير", "Reporting"),
         "text": T("أعدّ لوحات المتابعة وتقارير مؤشرات الأداء والتحديثات التنفيذية لكبار أصحاب المصلحة.", "I prepare dashboards, KPI reports and executive updates for senior stakeholders.")},
    ],
    "tabs_label": T("ما أفعله في EPMO", "What I do in the EPMO"),

    "path_title": T("ثلاث جهات منذ يناير 2023.", "Three organisations since January 2023."),
    "path_rows": [
        {"org": T("أرامكو السعودية", "Saudi Aramco"), "role": T("متدرب، مهندس تآكل", "Trainee, corrosion engineer"), "when": T("2023", "2023"), "s": "2023-01", "e": "2023-08"},
        {"org": T("Align Consulting", "Align Consulting"), "role": T("مساعد مستشار، ثم مستشار", "Assistant Consultant, then Consultant"), "when": T("2024–2026", "2024–2026"), "s": "2024-10", "e": "2026-07"},
        {"org": T("وزارة الموارد البشرية والتنمية الاجتماعية", "Ministry of Human Resources and Social Development"), "role": T("مدير مشاريع، EPMO", "Projects Manager, EPMO"), "when": T("منذ 2026", "Since 2026"), "s": "2026-07", "e": "now"},
    ],
    "path_cta": T("افتح الجدول الكامل مع الشهادات", "Open the full schedule, certificates included"),

    "align_title": T("في Align: أكثر من 40 مبادرة استراتيجية.", "At Align: 40+ strategic initiatives."),
    "align_text": T("خلال سنة وعشرة أشهر قدت ونسّقت أكثر من [[7+]] مشاريع لجهات حكومية وشركات، وسلّمت أكثر من [[40+]] مبادرة استراتيجية، وصممت إطار Marketing PMO وطبّقته عبر عدة وحدات أعمال.",
                    "In one year and ten months I led and coordinated [[7+]] projects for government and corporate clients, delivered [[40+]] strategic initiatives, and designed and implemented a Marketing PMO framework across multiple business units."),
    "align_cta": T("اقرأ ما بنيته لكل جهة", "See what I built for each client"),

    "cred_title": T("PMP، ثم PMOCP.", "PMP, then PMOCP."),
    "cred_line": T("ومعهما اعتماد مهني من الهيئة السعودية للمهندسين، وبرنامج McKinsey Forward.",
                   "Alongside them: a professional accreditation from the Saudi Council of Engineers and the McKinsey Forward Program."),
    "cred_cta": T("كل الشهادات والتعليم", "All certificates and education"),

    "quote": T("الملكية يجب أن تكون في كل شخص. ليست مهارة فقط، إنها عقلية.",
               "Ownership should be in every person. It's not just a skill, it's a mindset."),
    "quote_src": T("من منشور كتبته على لينكدإن عن الملكية والتدخّل", "From my LinkedIn post on ownership and interference"),
    "quote_cta": T("متى تكون ملكية، ومتى تصير تدخّلًا", "When it's ownership, and when it's interference"),
}

# ------------------------------------------------------------------ CAREER
GANTT = {
    "start": "2022-01", "end": "2027-01",
    "rows": [
        {"id": "kfupm", "kind": "study", "label": T("جامعة الملك فهد للبترول والمعادن", "KFUPM"),
         "s": "2018-08", "e": "2024-06",
         "cap_t": T("بكالوريوس الهندسة الكيميائية", "BSc Chemical Engineering"),
         "cap_d": T("أغسطس 2018 – يونيو 2024", "Aug 2018 – Jun 2024"),
         "cap_x": T("جامعة الملك فهد للبترول والمعادن. ومن أنشطتي نادي IE الرياضي.", "King Fahd University of Petroleum & Minerals. Activities: IE Sports Club.")},
        {"id": "aramco", "kind": "role", "label": T("أرامكو السعودية", "Saudi Aramco"),
         "s": "2023-01", "e": "2023-08",
         "cap_t": T("متدرب، مهندس تآكل", "Internship trainee, corrosion engineer"),
         "cap_d": T("يناير – أغسطس 2023", "Jan – Aug 2023"),
         "cap_x": T("إدارة خطوط الأنابيب بالمنطقة الشمالية، الظهران.", "Northern Area Pipeline Department, Dhahran.")},
        {"id": "align1", "kind": "role", "label": T("Align: مساعد مستشار", "Align: Assistant Consultant"),
         "s": "2024-10", "e": "2025-10",
         "cap_t": T("مساعد مستشار في Align Consulting", "Assistant Consultant, Align Consulting"),
         "cap_d": T("أكتوبر 2024 – أكتوبر 2025", "Oct 2024 – Oct 2025"),
         "cap_x": T("الدمام، المنطقة الشرقية.", "Dammam, Eastern Province.")},
        {"id": "align2", "kind": "role", "label": T("Align: مستشار", "Align: Consultant"),
         "s": "2025-11", "e": "2026-07",
         "cap_t": T("مستشار في Align Consulting", "Consultant, Align Consulting"),
         "cap_d": T("نوفمبر 2025 – يوليو 2026", "Nov 2025 – Jul 2026"),
         "cap_x": T("ترقّيت إلى مستشار في نوفمبر 2025.", "Promoted to Consultant in November 2025.")},
        {"id": "hrsd", "kind": "role", "label": T("الوزارة: مدير مشاريع EPMO", "HRSD: Projects Manager, EPMO"),
         "s": "2026-07", "e": "now",
         "cap_t": T("مدير مشاريع، EPMO", "Projects Manager, EPMO"),
         "cap_d": T("يوليو 2026 – الآن", "Jul 2026 – present"),
         "cap_x": T("وزارة الموارد البشرية والتنمية الاجتماعية، الرياض. 18 مشروعًا نشطًا في برنامج سخاء.", "Ministry of Human Resources and Social Development, Riyadh. 18 active projects in the Sakhaa Program.")},
    ],
    "miles_label": T("الشهادات", "Certificates"),
    "miles": [
        {"id": "m-coursera", "d": "2022-09", "n": 1,
         "cap_t": T("Foundations of Project Management", "Foundations of Project Management"),
         "cap_d": T("Coursera، سبتمبر 2022", "Coursera, Sep 2022"),
         "cap_x": T("وأنا ما زلت طالبًا في الجامعة.", "While I was still at university.")},
        {"id": "m-mustashar", "d": "2024-02", "n": 1,
         "cap_t": T("Foundational Consulting Skills", "Foundational Consulting Skills"),
         "cap_d": T("مسرعة مستشار، فبراير 2024", "Mustashar Accelerator, Feb 2024"),
         "cap_x": T("قبل ثمانية أشهر من بدايتي في Align.", "Eight months before I started at Align.")},
        {"id": "m-jul24", "d": "2024-07", "n": 3,
         "cap_t": T("ثلاث شهادات في يوليو 2024", "Three certificates in July 2024"),
         "cap_d": T("يوليو 2024", "Jul 2024"),
         "cap_x": T("McKinsey Forward Program، والحزام الأصفر في Six Sigma، والاعتماد المهني من الهيئة السعودية للمهندسين.", "McKinsey Forward Program, Six Sigma Yellow Belt, and the Saudi Council of Engineers professional accreditation.")},
        {"id": "m-pmp", "d": "2025-09", "n": 1,
         "cap_t": T("PMP®", "PMP®"),
         "cap_d": T("PMI، سبتمبر 2025", "PMI, Sep 2025"),
         "cap_x": T("درستها ليلًا وأنا أقود مشاريع العملاء نهارًا.", "Studied at night while leading client projects by day.")},
        {"id": "m-pmocp", "d": "2026-05", "n": 1,
         "cap_t": T("PMI-PMOCP", "PMI-PMOCP"),
         "cap_d": T("PMI، مايو 2026", "PMI, May 2026"),
         "cap_x": T("بعد ثمانية أشهر من PMP.", "Eight months after the PMP.")},
    ],
}

CAREER = {
    "title": T("المسيرة | صالح الدخيل", "Career | Saleh Al Dakheel"),
    "desc": T("مسيرة صالح الدخيل: متدرب مهندس تآكل في أرامكو السعودية 2023، ثم مساعد مستشار ومستشار في Align Consulting بالدمام، ثم مدير مشاريع في EPMO بوزارة الموارد البشرية والتنمية الاجتماعية منذ يوليو 2026.",
              "Saleh Al Dakheel's career: corrosion engineering trainee at Saudi Aramco (2023), Assistant Consultant then Consultant at Align Consulting in Dammam, and Projects Manager in the EPMO of HRSD since July 2026."),
    "h1": T("من أنابيب أرامكو إلى مكتب المشاريع.", "From Aramco pipelines to the PMO."),
    "lead": T("يناير 2023: متدرب في الظهران. يوليو 2026: مدير مشاريع في الوزارة بالرياض. وبينهما Align Consulting في الدمام.",
              "January 2023: a trainee in Dhahran. July 2026: a projects manager at the ministry in Riyadh. In between, Align Consulting in Dammam."),
    "gantt_title": T("أدوار وشهادات على خط زمني واحد.", "Roles and certificates on one timeline."),
    "gantt_lead": T("الأشرطة للأدوار والدراسة، والنقاط للشهادات. اضغط على أي شريط أو نقطة لتقرأها.",
                    "Bars are roles and study, dots are certificates. Tap any bar or dot to read it."),
    "gantt_aria": T("مخطط جانت لمسيرة صالح الدخيل من 2022 إلى اليوم", "Gantt chart of Saleh Al Dakheel's career from 2022 to today"),
    "roles": [
        {
            "id": "hrsd",
            "org": T("وزارة الموارد البشرية والتنمية الاجتماعية.", "Ministry of Human Resources and Social Development."),
            "title": T("مدير مشاريع، مكتب إدارة المشاريع المؤسسي (EPMO)", "Projects Manager, EPMO"),
            "meta": [T("يوليو 2026 – الآن", "Jul 2026 – present"), T("الرياض، حضوري", "Riyadh, on-site"), T("دوام كامل", "Full-time")],
            "points": [
                T("أقود [[18]] مشروعًا نشطًا، وأشرف على تمكين [[82]] في برنامج سخاء: مبادرة الوزارة المتوائمة مع رؤية 2030 لمشاريع التنمية المستدامة التي يرعاها مانحون.",
                  "I lead [[18]] active projects and oversee the enablement of [[82]] in the Sakhaa Program, HRSD's Vision 2030-aligned initiative for donor-sponsored sustainable development projects."),
                T("أدير العلاقة مع المانحين والجهات الحكومية، وأوفّق بين التوقعات وخطط التسليم.", "I manage donor and government relationships, aligning expectations and delivery plans."),
                T("أتابع الالتزامات والمعالم ومخاطر المحفظة، وأصعّد المشكلات مبكرًا.", "I track commitments, milestones and portfolio risks, escalating issues early."),
                T("أعدّ لوحات المتابعة وتقارير مؤشرات الأداء والتحديثات التنفيذية لكبار أصحاب المصلحة.", "I prepare dashboards, KPI reports and executive updates for senior stakeholders."),
                T("أطبّق معايير الحوكمة ومنهجيات EPMO وقوالبه على المشاريع.", "I apply EPMO governance standards, methodologies and templates across projects."),
            ],
            "more": [],
        },
        {
            "id": "align",
            "org": T("Align Consulting.", "Align Consulting."),
            "title": T("مساعد مستشار، ثم مستشار", "Assistant Consultant, then Consultant"),
            "steps": [T("مستشار: نوفمبر 2025 – يوليو 2026", "Consultant: Nov 2025 – Jul 2026"), T("مساعد مستشار: أكتوبر 2024 – أكتوبر 2025", "Assistant Consultant: Oct 2024 – Oct 2025")],
            "meta": [T("سنة و10 أشهر", "1 yr 10 mos"), T("الدمام، المنطقة الشرقية، حضوري", "Dammam, Eastern Province, on-site"), T("دوام كامل", "Full-time")],
            "points": [
                T("قدت ونسّقت أكثر من [[7+]] مشاريع لجهات حكومية وشركات، ضمن النطاق والجدول.", "Led and coordinated [[7+]] projects for government and corporate clients, within scope and timeline."),
                T("صممت إطار Marketing PMO وطبّقته، فانتظمت إجراءات المشاريع وحوكمتها عبر عدة وحدات أعمال.", "Designed and implemented a Marketing PMO framework that streamlined project processes and governance across multiple business units."),
                T("سلّمت أكثر من [[40+]] مبادرة استراتيجية لجهات حكومية وشركات.", "Delivered [[40+]] strategic initiatives for government and corporate clients."),
            ],
            "more": [
                T("بنيت الجداول الزمنية، وأدرت الاعتماديات، ويسّرت تقييم المخاطر.", "Developed project schedules, managed dependencies and facilitated risk assessments."),
                T("أدرت ورش العمل وحوّلت مخرجاتها إلى خرائط طريق وخطط تسليم.", "Facilitated workshops and translated outcomes into project roadmaps and delivery plans."),
                T("تابعت الأداء بلوحات المتابعة ومؤشرات الأداء والتقارير التنفيذية.", "Monitored performance through dashboards, KPIs and executive reports."),
                T("وجّهت الفرق في جمع المتطلبات وتنقيح الـ backlog والتخطيط التكيفي، موازنًا بين Agile والممارسات التقليدية.", "Guided teams in requirement gathering, backlog refinement and adaptive planning, balancing Agile and traditional PM practices."),
            ],
        },
        {
            "id": "aramco",
            "org": T("أرامكو السعودية.", "Saudi Aramco."),
            "title": T("متدرب، مهندس تآكل في إدارة خطوط الأنابيب بالمنطقة الشمالية", "Internship trainee, corrosion engineer, Northern Area Pipeline Department"),
            "meta": [T("يناير – أغسطس 2023", "Jan – Aug 2023"), T("الظهران", "Dhahran")],
            "points": [
                T("أجريت فحوصًا للكشف عن العيوب والتآكل والضرر الميكانيكي والأعطال، وحققت في أسباب الأعطال، وقدّمت توصيات تمنع تكرارها.", "Inspected for defects, corrosion, mechanical damage and failures, investigated failure causes, and recommended how to prevent repeat failures."),
                T("قدّمت الدعم الفني للتشغيل في التحكم بالتآكل ومنعه، والفحص وتقييم الحالة (الصلاحية للخدمة).", "Gave operations technical support on corrosion control and prevention, inspection and condition assessment (fitness for service)."),
                T("تابعت خطط سلامة الأصول، ونسّقت الاجتماعات حتى لا يتوقف العمل.", "Monitored integrity plans and coordinated meetings to keep the work flowing."),
            ],
            "more": [
                T("نفّذت فحوص UT وPT وفق معايير SAES وإجراءات السلامة في أرامكو.", "Performed UT and PT per SAES and Aramco safety procedures."),
                T("حلّلت بيانات التآكل (UT والكوبونات والمجسّات) باستخدام APM Meridium وPCMS.", "Analysed corrosion data (UT, coupons, probes) using APM Meridium and PCMS."),
                T("طبّقت الفحص المبني على المخاطر (RBI) وفق API 580/581، بما يتوافق مع نماذج المخاطر في أرامكو.", "Implemented API 580/581-based RBI aligned with Aramco's risk models."),
                T("قيّمت المعدات وفق API 579/ASME FFS-1.", "Evaluated equipment using API 579/ASME FFS-1."),
                T("راجعت التهديدات (CO₂/H₂S، والتآكل الميكروبي MIC، والتعرية) وطرق الحد منها وفق مواصفات أرامكو.", "Reviewed threats (CO₂/H₂S, MIC, erosion) and mitigation methods per Aramco specifications."),
            ],
            "note": T("ولدي خطاب توصية من هذه الفترة، منشور على حسابي في لينكدإن.", "A recommendation letter from this role is on my LinkedIn profile."),
        },
    ],
}

# ------------------------------------------------------------------ CONSULTING
CONSULTING = {
    "title": T("الاستشارات | صالح الدخيل", "Consulting | Saleh Al Dakheel"),
    "desc": T("عمل صالح الدخيل في Align Consulting: أكثر من 7 مشاريع وأكثر من 40 مبادرة استراتيجية، وMarketing PMO لأربع جهات، واستراتيجية تسويق لـ National Centre for Palms and Dates.",
              "Saleh Al Dakheel's work at Align Consulting: 7+ projects, 40+ strategic initiatives, a Marketing PMO for four clients and a marketing strategy for the National Centre for Palms and Dates."),
    "h1": T("خمس جهات، وأربعة مكاتب Marketing PMO.", "Five clients. Four Marketing PMOs."),
    "lead": T("في Align Consulting، بين أكتوبر 2024 ويوليو 2026، قدت ونسّقت أكثر من [[7+]] مشاريع، وسلّمت أكثر من [[40+]] مبادرة استراتيجية لجهات حكومية وشركات.",
              "At Align Consulting, from October 2024 to July 2026, I led and coordinated [[7+]] projects and delivered [[40+]] strategic initiatives for government and corporate clients."),
    "list_title": T("ما بنيته لكل جهة.", "What I built for each client."),
    "pmo_tag": T("Marketing PMO", "Marketing PMO"),
    "clients": [
        {"name": "National Centre for Palms and Dates", "pmo": False,
         "text": T("قدت تطوير استراتيجية تسويق شاملة وإطار للحملات، لرفع حضور المركز على المستوى الوطني.", "I led the development of a comprehensive marketing strategy and campaign framework to raise the Centre's national presence."),
         "tags": [T("استراتيجية تسويق", "Marketing strategy"), T("إطار الحملات", "Campaign framework")]},
        {"name": "Ahmed Al Mousa Holding Company", "pmo": True,
         "text": T("صممت استراتيجية العلامة والتواصل من الصفر، ثم أسست Marketing PMO متكاملًا وشغّلته.", "I designed the brand and communication strategy from the ground up, then established and operationalised a full-scale Marketing PMO."),
         "tags": [T("استراتيجية العلامة", "Brand strategy"), T("التواصل", "Communication")]},
        {"name": "Jewar", "pmo": True,
         "text": T("حددت تموضع العلامة وبنيت استراتيجية تواصل متكاملة، وأطلقت Marketing PMO مفصّلًا على احتياجها.", "I defined the brand positioning, built an integrated communication strategy and launched a tailored Marketing PMO."),
         "tags": [T("تموضع العلامة", "Brand positioning"), T("التواصل", "Communication")]},
        {"name": "Ahmed Al Mousa Engineering Consultants", "pmo": True,
         "text": T("هيكلت استراتيجية العلامة والتواصل، وطبّقت نموذج Marketing PMO.", "I structured the branding and communication strategy and implemented a Marketing PMO model."),
         "tags": [T("العلامة", "Branding"), T("التواصل", "Communication")]},
        {"name": "Pencil & Co.", "pmo": True,
         "text": T("صنعت هوية العلامة وأساس التواصل، ثم طوّرت Marketing PMO مخصصًا وشغّلته.", "I created the brand identity and communication foundation, then developed and deployed a customised Marketing PMO."),
         "tags": [T("هوية العلامة", "Brand identity"), T("أساس التواصل", "Communication foundation")]},
    ],
    "how_title": T("من ورشة العمل إلى خارطة الطريق.", "From the workshop to the roadmap."),
    "how_lead": T("هكذا كنت أعمل في Align.", "How I worked at Align."),
    "how": [
        {"icon": "layers", "text": T("أدرت ورش العمل، وحوّلت مخرجاتها إلى خرائط طريق وخطط تسليم.", "I facilitated workshops and turned their outcomes into roadmaps and delivery plans.")},
        {"icon": "cal", "text": T("بنيت الجداول الزمنية، وأدرت الاعتماديات، ويسّرت تقييم المخاطر.", "I built the schedules, managed dependencies and facilitated risk assessments.")},
        {"icon": "report", "text": T("تابعت الأداء بلوحات المتابعة ومؤشرات الأداء والتقارير التنفيذية.", "I monitored performance through dashboards, KPIs and executive reports.")},
        {"icon": "gov", "text": T("وجّهت الفرق في جمع المتطلبات وتنقيح الـ backlog والتخطيط التكيفي، وجمعت بين Agile والممارسات التقليدية.", "I guided teams through requirement gathering, backlog refinement and adaptive planning, balancing Agile with traditional practice.")},
    ],
}

# ------------------------------------------------------------------ APPROACH
APPROACH = {
    "title": T("المنهج | صالح الدخيل", "Approach | Saleh Al Dakheel"),
    "desc": T("كيف يعمل صالح الدخيل: الفرق بين الملكية والتدخّل ومصفوفة RACI، وأربع قيم: التفكير الاستراتيجي، والملكية، والتميّز والاحترافية، والتكيّف.",
              "How Saleh Al Dakheel works: ownership versus interference and the RACI matrix, and four values: strategic thinking, ownership, excellence and professionalism, adaptability."),
    "h1": T("الملكية عقلية.", "Ownership is a mindset."),
    "lead": T("أربع قيم كتبتها في ملفي التعريفي، وفكرة كتبت عنها على لينكدإن: أن تملك عملك شيء، وأن تدخل في عمل غيرك شيء آخر.",
              "Four values from my portfolio, and an idea I wrote about on LinkedIn: owning your work is one thing, stepping into someone else's is another."),
    "seg_title": T("متى تكون ملكية، ومتى تصير تدخّلًا؟", "When is it ownership, and when is it interference?"),
    "seg": [
        {"id": "own", "label": T("الملكية", "Ownership"),
         "text": T("أن تتحمل مسؤولية ما يخصك فعلًا.", "Taking responsibility for what actually belongs to you.")},
        {"id": "int", "label": T("التدخّل", "Interference"),
         "text": T("أن تدخل في أمور ليست لك.", "Stepping into matters that are not yours.")},
    ],
    "seg_label": T("قارن بين الملكية والتدخّل", "Compare ownership and interference"),
    "seg_note": T("ويحدث الخلط بينهما حين لا تكون هناك مصفوفة RACI.", "The two get mixed up when there is no RACI matrix in place."),
    "values_title": T("أربع قيم أحاسب نفسي بها.", "Four values I hold myself to."),
    "values_label": T("القيم الأربع", "The four values"),
    "values": [
        {"name": T("التفكير الاستراتيجي", "Strategic Thinking"),
         "text": T("أحلّ المشكلات بمنهجية، وعيني على الأثر البعيد وتوافقه مع العمل.", "A structured problem-solver focused on long-term impact and business alignment.")},
        {"name": T("الملكية", "Ownership"),
         "text": T("أقود بمسؤولية كاملة، وأوصل النتيجة من البداية إلى النهاية.", "I lead with full accountability, driving results from start to finish.")},
        {"name": T("التميّز والاحترافية", "Excellence & Professionalism"),
         "text": T("أسلّم نتائج دقيقة ومتقنة، بحسّ مهني.", "I deliver precise, high-quality outcomes with a professional edge.")},
        {"name": T("التكيّف", "Adaptability"),
         "text": T("أعمل جيدًا حين تتغير الظروف بسرعة، وأضيف قيمة في قطاعات مختلفة.", "I thrive in fast-changing settings, adding value across industries.")},
    ],
    "belief": T("أرى أن النجاح الحقيقي يجمع التفكير الاستراتيجي والتنفيذ القوي وعلاقات تدوم.",
                "I believe real success comes from combining strategic thinking, strong execution, and building relationships that last."),
    "night_title": T("بالنهار مشاريع، وبالليل دراسة.", "Projects by day, study by night."),
    "night_text": T("حين دخلت الاستشارات وعدت نفسي ألا يتوقف التعلّم. كنت أقود المشاريع نهارًا تحت ضغط العملاء والمواعيد، وأعود في الليل طالبًا. الانضباط هو ما أبقاني مستمرًا، وتعلّمت في الطريق أن أستخدم Agile وWaterfall بعمق أكبر.",
                    "When I started in consulting I promised myself the learning wouldn't stop. By day I led projects under client pressure and deadlines; by night I was a student again. Discipline is what kept me going, and on the way I learned to use Agile and Waterfall more deeply."),
    "night_q1": T("الإنجاز مو الشهادة بحد ذاتها… الإنجاز الحقيقي هو الرحلة اللي صنعتني وأنا أوصل لها.",
                  "The achievement isn't the certificate itself. The real achievement is the road that shaped me on the way to it."),
    "night_q2": T("هذي مجرد محطة في طريق أطول.", "This is just one stop on a longer road."),
    "night_src": T("من منشوري عن شهادة الـ PMP", "From my post about the PMP"),
    "pmp_title": T("ليش فجأة الكل صار عنده شهادة PMP؟", "Why does everyone suddenly have a PMP?"),
    "pmp_text": T("سؤال فتحت به منشورًا عن تغيّر اختبار PMP في يوليو 2026: نحو القيمة والذكاء الاصطناعي وطريقة التفكير، لا الحفظ. وختمته بسؤال للقرّاء.",
                  "The hook of my post on the PMP exam change in July 2026: towards value, AI and a way of thinking, not memorising. I ended it with a question to readers."),
    "top_title": T("5 إلى 10% فقط.", "Only 5–10%."),
    "top_text": T("تقول الأبحاث إن 5 إلى 10% فقط من المهنيين يُعدّون من أصحاب المواهب العليا. أعمل كل يوم لأكون منهم.",
                  "Research says that only 5–10% of professionals are considered top talent. I'm working every day to be part of that group."),
}

# ------------------------------------------------------------------ CREDENTIALS
CREDENTIALS = {
    "title": T("الشهادات | صالح الدخيل", "Credentials | Saleh Al Dakheel"),
    "desc": T("شهادات صالح الدخيل: PMI-PMOCP (مايو 2026)، وPMP (سبتمبر 2025)، واعتماد مهني من الهيئة السعودية للمهندسين، وMcKinsey Forward، وSix Sigma Yellow Belt، وبكالوريوس الهندسة الكيميائية من جامعة الملك فهد للبترول والمعادن.",
              "Saleh Al Dakheel's credentials: PMI-PMOCP (May 2026), PMP (Sep 2025), Saudi Council of Engineers professional accreditation, McKinsey Forward, Six Sigma Yellow Belt, and a BSc in Chemical Engineering from KFUPM."),
    "h1": T("شهادتان من PMI خلال ثمانية أشهر.", "Two PMI credentials, eight months apart."),
    "lead": T("PMP في سبتمبر 2025، ثم PMI-PMOCP في مايو 2026. وقبلهما بكالوريوس الهندسة الكيميائية وخمسة برامج.",
              "The PMP in September 2025, then the PMI-PMOCP in May 2026. Before them, a chemical engineering degree and five programmes."),
    "valid_title": T("سارية اليوم.", "Valid today."),
    "valid_lead": T("الخط من تاريخ الإصدار إلى تاريخ الانتهاء، والنقطة حيث نحن اليوم.", "Each line runs from issue to expiry; the dot marks today."),
    "valid": [
        {"name": T("PMO Certified Professional (PMI-PMOCP)", "PMO Certified Professional (PMI-PMOCP)"), "short": "PMI-PMOCP",
         "by": T("Project Management Institute", "Project Management Institute"), "s": "2026-05", "e": "2029-05",
         "s_l": T("مايو 2026", "May 2026"), "e_l": T("مايو 2029", "May 2029"),
         "note": T("اعتراف رسمي بمعرفة وظيفية احترافية في مكاتب إدارة المشاريع، وبالقدرة على دعم الـ PMO وإنشائه وقيادته.", "Formal recognition of professional-level PMO functional knowledge and the ability to support, create, and lead a PMO.")},
        {"name": T("Project Management Professional (PMP)®", "Project Management Professional (PMP)®"), "short": "PMP®",
         "by": T("Project Management Institute", "Project Management Institute"), "s": "2025-09", "e": "2028-09",
         "s_l": T("سبتمبر 2025", "Sep 2025"), "e_l": T("سبتمبر 2028", "Sep 2028"),
         "note": T("نلتها وأنا أقود مشاريع العملاء في Align.", "Earned while leading client projects at Align.")},
        {"name": T("الاعتماد المهني", "Professional Accreditation"), "short": "SCE",
         "by": T("الهيئة السعودية للمهندسين", "Saudi Council of Engineers"), "s": "2024-07", "e": "2028-07",
         "s_l": T("يوليو 2024", "Jul 2024"), "e_l": T("يوليو 2028", "Jul 2028"),
         "note": T("حصلت عليه في الشهر نفسه الذي أنهيت فيه McKinsey Forward وSix Sigma.", "Earned the same month I completed McKinsey Forward and Six Sigma.")},
    ],
    "valid_label": T("الشهادات السارية", "Valid credentials"),
    "valid_from": T("من", "from"), "valid_to": T("إلى", "to"),
    "prog_title": T("قبل PMP: خمسة برامج منذ 2020.", "Before the PMP: five programmes since 2020."),
    "progs": [
        {"name": "McKinsey Forward Program", "by": T("McKinsey & Company", "McKinsey & Company"), "d": T("يوليو 2024", "Jul 2024")},
        {"name": "Six Sigma Yellow Belt (SSYB)", "by": T("6sigmastudy", "6sigmastudy"), "d": T("يوليو 2024", "Jul 2024")},
        {"name": "Foundational Consulting Skills", "by": T("مسرعة مستشار", "Mustashar Accelerator"), "d": T("فبراير 2024", "Feb 2024")},
        {"name": "Foundations of Project Management", "by": T("Coursera", "Coursera"), "d": T("سبتمبر 2022", "Sep 2022")},
        {"name": "Soft Skills Training", "by": T("upGrad KnowledgeHut", "upGrad KnowledgeHut"), "d": T("مايو 2020", "May 2020")},
    ],
    "edu_title": T("هندسة كيميائية من جامعة الملك فهد.", "Chemical engineering at KFUPM."),
    "edu_school": T("جامعة الملك فهد للبترول والمعادن", "King Fahd University of Petroleum & Minerals"),
    "edu_degree": T("بكالوريوس الهندسة الكيميائية", "BSc, Chemical Engineering"),
    "edu_when": T("أغسطس 2018 – يونيو 2024", "Aug 2018 – Jun 2024"),
    "edu_act": T("من أنشطتي: نادي IE الرياضي.", "Activities: IE Sports Club."),
    "lang_title": T("اللغات", "Languages"),
    "langs": [T("العربية", "Arabic"), T("الإنجليزية", "English")],
}

# ------------------------------------------------------------------ CONTACT
CONTACT = {
    "title": T("تواصل | صالح الدخيل", "Contact | Saleh Al Dakheel"),
    "desc": T("تواصل مع صالح الدخيل بالبريد أو عبر لينكدإن. الرياض، المملكة العربية السعودية.",
              "Contact Saleh Al Dakheel by email or on LinkedIn. Riyadh, Saudi Arabia."),
    "h1": T("من الرياض، على البريد ولينكدإن.", "In Riyadh, on email and LinkedIn."),
    "lead": T("للتواصل المهني: البريد أو لينكدإن.",
              "For professional contact: email or LinkedIn."),
    "faq_title": T("أسئلة شائعة عن صالح.", "Common questions about Saleh."),
    "faq": [
        {"q": T("أين يعمل صالح الدخيل اليوم؟", "Where does Saleh Al Dakheel work today?"),
         "a": T("مدير مشاريع في مكتب إدارة المشاريع المؤسسي (EPMO) بوزارة الموارد البشرية والتنمية الاجتماعية في الرياض، منذ يوليو 2026. يقود 18 مشروعًا نشطًا ويشرف على تمكين 82 في برنامج سخاء.",
                "He is a Projects Manager in the EPMO of the Ministry of Human Resources and Social Development in Riyadh, since July 2026. He leads 18 active projects and oversees the enablement of 82 in the Sakhaa Program.")},
        {"q": T("ما شهاداته في إدارة المشاريع؟", "What project management credentials does he hold?"),
         "a": T("PMP من PMI (سبتمبر 2025)، وPMI-PMOCP (مايو 2026)، والحزام الأصفر في Six Sigma، وبرنامج McKinsey Forward، واعتماد مهني من الهيئة السعودية للمهندسين.",
                "The PMP from PMI (September 2025), the PMI-PMOCP (May 2026), a Six Sigma Yellow Belt, the McKinsey Forward Program, and a professional accreditation from the Saudi Council of Engineers.")},
        {"q": T("ما خبرته في الاستشارات؟", "What consulting experience does he have?"),
         "a": T("سنة وعشرة أشهر في Align Consulting بالدمام، مساعد مستشار ثم مستشار: أكثر من 7 مشاريع، وأكثر من 40 مبادرة استراتيجية، وإطار Marketing PMO، لجهات منها National Centre for Palms and Dates وAhmed Al Mousa Holding Company وJewar وAhmed Al Mousa Engineering Consultants وPencil & Co.",
                "One year and ten months at Align Consulting in Dammam, as Assistant Consultant and then Consultant: 7+ projects, 40+ strategic initiatives and a Marketing PMO framework, for clients including the National Centre for Palms and Dates, Ahmed Al Mousa Holding Company, Jewar, Ahmed Al Mousa Engineering Consultants and Pencil & Co.")},
        {"q": T("ماذا درس صالح؟", "What did Saleh study?"),
         "a": T("بكالوريوس الهندسة الكيميائية من جامعة الملك فهد للبترول والمعادن (2018–2024). وتدرّب عام 2023 في أرامكو السعودية مهندسَ تآكل في إدارة خطوط الأنابيب بالمنطقة الشمالية.",
                "A BSc in Chemical Engineering from King Fahd University of Petroleum & Minerals (2018–2024). In 2023 he trained at Saudi Aramco as a corrosion engineer in the Northern Area Pipeline Department.")},
        {"q": T("كيف أتواصل معه؟", "How can I contact him?"),
         "a": T("بالبريد Saleh.h.aldakheel@gmail.com، أو برسالة على لينكدإن.",
                "By email at Saleh.h.aldakheel@gmail.com, or with a message on LinkedIn.")},
    ],
}

NOT_FOUND = {
    "title": T("الصفحة غير موجودة | صالح الدخيل", "Page not found | Saleh Al Dakheel"),
    "h1": T("هذه الصفحة غير موجودة.", "This page doesn't exist."),
    "lead": T("ربما تغيّر الرابط. الصفحات كلها من هنا.", "The link may have changed. Every page is one tap away."),
    "cta": T("العودة إلى الرئيسية", "Back to the home page"),
}

# For the JSON-LD "knowsAbout" and "hasOccupation" (both languages)
KNOWS_ABOUT = [
    "Project management", "إدارة المشاريع", "PMO", "Enterprise PMO (EPMO)", "مكتب إدارة المشاريع المؤسسي",
    "Portfolio governance", "حوكمة المحافظ", "Portfolio risk management", "إدارة مخاطر المحفظة",
    "KPI reporting", "Executive reporting", "Stakeholder management", "Donor relations",
    "Marketing PMO", "Brand and communication strategy", "Agile", "Waterfall", "Hybrid project management",
    "Project scheduling", "Risk assessment", "Workshop facilitation", "Roadmapping",
    "Corrosion engineering", "Risk-based inspection (API 580/581)", "Fitness for service (API 579/ASME FFS-1)",
    "Chemical engineering", "الهندسة الكيميائية", "Vision 2030",
]
OCCUPATIONS = [
    ("Projects Manager", ["Project Manager", "مدير مشاريع", "مدير مشروع", "EPMO Projects Manager", "PMO Manager", "مدير مشاريع في مكتب إدارة المشاريع"]),
    ("Management Consultant", ["Consultant", "مستشار", "مستشار إدارة", "Assistant Consultant", "مساعد مستشار", "PMO Consultant"]),
    ("Chemical Engineer", ["مهندس كيميائي", "Corrosion Engineer", "مهندس تآكل"]),
]
