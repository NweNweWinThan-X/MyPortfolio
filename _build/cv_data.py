# -*- coding: utf-8 -*-
"""Single source of content for every CV layout.

Nothing here may be invented; every line traces to the source CV documents.
Reconstructed after the original build directory was lost — reproduces
cv-form/NWENWE_WINTHAN_Resume_version1.pdf as published at commit 9540d34.
"""
import base64
import os

NAME = "NWE NWE WIN THAN"
TITLE = "Senior Software Engineer"
SUBTITLE = "Full-Stack Developer"
TITLE_V2 = "Senior Software Engineer — Full-Stack Developer"

CONTACT = {
    "location": "Tokyo, Japan",
    "phone": "+81 70-2252-7003",
    "email": "nwenwewinthan777@gmail.com",
    "linkedin": "linkedin.com/in/nwe-nwe-win-than",
    "github": "github.com/NweNweWinThan-X",
    "portfolio": "nwenwewinthan-portfolio.vercel.app",
    "visa": "Valid Japanese work visa",
}

SUMMARY = (
    "Full-stack software engineer with 8+ years building and operating business-critical web "
    "systems, including nearly 4 years in Tokyo. Three of those systems were in the financial "
    "domain — a securities CRM, a banking platform covering payments, fund management and loan "
    "products, and a financial business system. Current stack is Java 21 and Spring Boot with "
    "React; previously C# / .NET MVC and PHP / Laravel. Owns features end to end across both "
    "tiers, from requirements definition through operational testing, and led three projects "
    "as team leader for teams of five to seven."
)

SUMMARY_SHORT = (
    "Full-stack software engineer with 8+ years building business-critical web systems, "
    "including nearly 4 years in Tokyo across three financial-domain platforms — a securities "
    "CRM, a banking system covering payments, fund management and loan servicing, and a "
    "financial business system. Java 21 and Spring Boot today; C# / .NET and PHP / Laravel "
    "before that. Team leader on three projects, teams of five to seven."
)

EXPERIENCE = [
    {
        "role": "Senior Software Engineer",
        "company": "Generic Solutions Co., Ltd.",
        "location": "Tokyo, Japan",
        "dates": "Nov 2024 – Present",
        "from": "2024", "to": "Present",
        "projects": "GS8 Banking System · GS8 WorkBench",
        "stack": "Java 21, Spring Boot, Thymeleaf, React, Tailwind CSS, MySQL, PostgreSQL, "
                 "Docker, AWS, Tomcat, GitLab",
        "bullets": [
            "Build front-end and back-end features for a banking platform covering payment "
            "processing, fund management and loan servicing, carrying each from detailed design "
            "through unit, integration, system and operational testing.",
            "Develop REST endpoints and Spring Boot service layers that back both React and "
            "Thymeleaf interfaces from a single domain model, so the two rendering paths cannot "
            "drift apart.",
            "Optimise database queries and application logic on loan-servicing screens, reducing "
            "page response times on the heaviest views.",
            "Delivered attendance, work-reporting, paid-leave and task-progress features for GS8 "
            "WorkBench, an internal workforce platform used across the organisation.",
            "Author design documents, UT/IT specifications and test cases, then review "
            "teammates' code against them to hold one quality bar across a six-person team.",
        ],
    },
    {
        "role": "Software Engineer",
        "company": "Starsoft Co., Ltd.",
        "location": "Tokyo, Japan",
        "dates": "Dec 2022 – Oct 2024",
        "from": "2022", "to": "2024",
        "projects": "WF Document Integration System · Tokai Tokyo Securities CRM",
        "stack": "VB.NET, C#, ASP.NET, .NET Framework, MVC, jQuery, Oracle, SQL Server 2012, "
                 "IIS, TFS, Azure DevOps",
        "bullets": [
            "Validated an Oracle version upgrade across an entire production brokerage CRM — "
            "full-screen verification, new-versus-current comparison, then regression and system "
            "testing — protecting a live securities system through the migration.",
            "Implemented detailed design through operational testing for case management, "
            "scheduling and approval-document features on an enterprise workflow platform across "
            "a 17-month engagement.",
            "Built batch programs for scheduled document processing, removing manual steps from "
            "the approval pipeline.",
            "Replaced an Excel-and-macro inquiry-tracking process with a web module, moving "
            "customer enquiry handling into the system of record.",
            "Produced UT/IT specifications and test cases, and handled QA and specification "
            "clarification with project leads throughout.",
        ],
    },
    {
        "role": "Developer → Senior Developer → Team Leader",
        "company": "Seattle Consulting Co., Ltd. / META TEAM Co., Ltd.",
        "location": "Yangon, Myanmar",
        "dates": "Jun 2018 – Oct 2022",
        "from": "2018", "to": "2022",
        "projects": "ToolSite · Axis · Spider",
        "stack": "PHP, Laravel, Vue.js, Vuex, Nuxt.js, Vuetify, Sass, MySQL, PostgreSQL, "
                 "Docker, AWS (S3/SNS/CloudWatch), GitHub",
        "bullets": [
            "Owned product-management and batch features across the full lifecycle — "
            "requirements definition, basic and detailed design, build, and unit through "
            "operational testing — on ToolSite, a three-and-a-half-year catalogue engagement.",
            "Promoted after 18 months and ultimately to Team Leader; took on schedule "
            "management, task allocation and code review for teams of five to seven, and "
            "proposed the technology choices for new modules.",
            "Recovered a slipping delivery date by proposing a re-sequenced task plan to the "
            "project lead and redistributing work across the team.",
            "Coordinated specifications directly with Japan's Ministry of Health, Labour and "
            "Welfare on Spider, a construction management system, then designed, built and "
            "tested the agreed features and ran the customer helpdesk.",
            "Built capacity search, consumption calculation and chart dashboards for Axis, an "
            "energy management system spanning municipal and prefectural bodies.",
            "Integrated AWS S3, SNS and CloudWatch for asset storage, notifications and "
            "monitoring.",
        ],
    },
    {
        "role": "Intern Developer",
        "company": "OK Dollar Co., Ltd. (OK$)",
        "location": "Yangon, Myanmar",
        "dates": "Oct 2017 – Apr 2018",
        "from": "2017", "to": "2018",
        "projects": "OK$ Financial Business System",
        "stack": "C#, ASP.NET, .NET Framework, MVC, Bootstrap, jQuery, MSSQL",
        "bullets": [
            "Developed contract-management batch processing and new application features for an "
            "internal financial services platform, tested through unit, integration and "
            "operational phases.",
            "Built RESTful APIs and designed, implemented and tested the web interfaces "
            "consuming them.",
            "Gathered requirements directly from clients to clarify complex specifications "
            "before build.",
        ],
    },
]

EDUCATION = {
    "degree": "Bachelor of Computer Science (B.C.Sc.)",
    "school": "University of Computer Studies, Magway",
    "location": "Magway, Myanmar",
    "dates": "Dec 2012 – Feb 2018",
    "from": "2012", "to": "2018",
}

PROJECT = {
    "name": "spring-boot-todolist",
    "url": "github.com/NweNweWinThan-X/spring-boot-todolist",
    "blurb": "REST API and React SPA built as a Spring Boot modular monolith, written to "
             "practise the patterns enterprise projects rarely leave room for.",
    "points": [
        "Java 21, Spring Boot 4, Spring Security 7, Spring Data JPA, Flyway, PostgreSQL. "
        "Stateless JWT (HS384) with role-based access control and per-account data isolation.",
        "React 19, TypeScript, Vite, Tailwind CSS.",
        "GitHub Actions running four parallel jobs: Maven verify over 32 unit and slice tests, "
        "a TypeScript check and build, 22 Playwright end-to-end tests against a "
        "postgres:17-alpine service, and a Docker build of both images. Tagged releases publish "
        "to GitHub Container Registry.",
        "ER diagram, request flow, design rationale, test strategy and CI/CD documented in-repo "
        "in English and Japanese.",
    ],
    "stats": [("32", "backend tests"), ("22", "E2E tests"), ("4", "CI jobs")],
}

# Ratings reflect the self-assessment in the 職務経歴書 technical-skills table,
# scaled to five points. Nothing here is inflated beyond that source.
SKILL_RATINGS = [
    ("Java / Spring Boot", 4),
    ("REST API &amp; backend design", 5),
    ("SQL &amp; database design", 5),
    ("JavaScript / React / Vue", 4),
    ("C# / .NET MVC", 4),
    ("PHP / Laravel", 4),
    ("Testing &amp; code review", 5),
    ("Docker &amp; CI/CD", 3),
    ("AWS", 3),
]

SKILL_TAGS = ["Java 21", "Spring Boot", "Spring Security", "REST APIs", "React", "TypeScript",
              "PostgreSQL", "MySQL", "Oracle", "Docker", "AWS", "CI/CD", "JUnit", "Agile",
              "System design"]

LEARNING = ["Kubernetes", "Redis", "AWS", "Terraform"]

STRENGTHS = [
    ("Fintech domain depth",
     "Three financial systems across eight years — a securities CRM, a banking platform and a "
     "financial business system — in a field where correctness and auditability are the job."),
    ("Full lifecycle ownership",
     "Requirements definition, basic and detailed design, build, and unit through operational "
     "testing, with the design documents and test specifications to match."),
    ("Production migration safety",
     "Took a live brokerage CRM through an Oracle version upgrade using full-screen "
     "new-versus-current comparison and regression testing."),
    ("Team leadership",
     "Team leader on three projects: schedule management, task allocation, resource planning "
     "and code review for teams of five to seven."),
    ("Bilingual delivery",
     "Four years in Japanese-language engineering teams in Tokyo, including specification "
     "coordination with a Japanese government ministry."),
]

CERTIFICATIONS = [
    ("AWS AI Practitioner", "Jun 2026"),
    ("TOEIC Listening &amp; Reading — 710", "May 2026"),
    ("TOPJ Japanese — Intermediate C", "Mar 2022"),
    ("IELTS 6.5", "Aug 2020"),
]

LANGUAGES = [
    ("Burmese", "Native", 5),
    ("English", "Business — TOEIC 710, IELTS 6.5", 4),
    ("Japanese", "Business — 4 yrs in Japanese-language teams", 4),
    ("Chinese (Mandarin)", "Elementary", 2),
]

PHOTO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'profile.jpg')


def _photo_data_uri():
    """profile.jpg as a data URI so every rendered PDF is self-contained."""
    with open(PHOTO_PATH, 'rb') as fh:
        return 'data:image/jpeg;base64,' + base64.b64encode(fh.read()).decode('ascii')


PHOTO = _photo_data_uri()
