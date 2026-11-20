from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os
import re

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# SKILLS DATABASE
# -----------------------------
SKILLS = [
    "python",
    "java",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "flask",
    "django",
    "machine learning",
    "deep learning",
    "data science",
    "data analytics",
    "power bi",
    "tableau",
    "excel",
    "statistics",
    "numpy",
    "pandas",
    "matplotlib",
    "tensorflow",
    "pytorch",
    "git",
    "github",
    "communication",
    "leadership"
]


# -----------------------------
# JOB ROLES
# -----------------------------
ROLE_SKILLS = {

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "statistics",
        "pandas"
    ],

    "Data Scientist": [
        "python",
        "sql",
        "machine learning",
        "statistics",
        "pandas",
        "numpy"
    ],

    "Python Developer": [
        "python",
        "flask",
        "django",
        "sql",
        "git",
        "github"
    ],

    "Web Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "python"
    ],

    "Machine Learning Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "numpy",
        "pandas"
    ]
}


# -----------------------------
# FIND SKILLS
# -----------------------------
def find_skills(text):

    text = text.lower()

    detected = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            detected.append(skill)

    return detected


# -----------------------------
# RESUME SCORE
# -----------------------------
def calculate_resume_score(detected_skills):

    if not detected_skills:
        return 0

    score = int((len(detected_skills) / len(SKILLS)) * 100)

    # Keep score between 0 and 100
    score = min(score, 100)

    return score


# -----------------------------
# ROLE MATCHING
# -----------------------------
def calculate_role_matches(detected_skills):

    role_matches = {}

    detected_set = set(detected_skills)

    for role, required_skills in ROLE_SKILLS.items():

        matched = [
            skill
            for skill in required_skills
            if skill in detected_set
        ]

        score = int(
            (len(matched) / len(required_skills)) * 100
        )

        missing = [
            skill
            for skill in required_skills
            if skill not in detected_set
        ]

        role_matches[role] = {
            "score": score,
            "matched": matched,
            "missing": missing
        }

    return role_matches


# -----------------------------
# UPLOAD RESUME
# -----------------------------
@app.route("/upload", methods=["POST"])
def upload_resume():

    if "resume" not in request.files:
        return "No resume selected"

    resume = request.files["resume"]

    if resume.filename == "":
        return "No resume selected"

    if not resume.filename.lower().endswith(".pdf"):
        return "Please upload a PDF file"

    # Save PDF
    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        resume.filename
    )

    resume.save(file_path)

    # -------------------------
    # READ PDF
    # -------------------------
    try:

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

    except Exception as e:

        return f"Unable to read PDF: {e}"


    # -------------------------
    # FIND SKILLS
    # -------------------------
    detected_skills = find_skills(text)


    # -------------------------
    # SCORE
    # -------------------------
    resume_score = calculate_resume_score(
        detected_skills
    )


    # -------------------------
    # ROLE MATCHING
    # -------------------------
    role_matches = calculate_role_matches(
        detected_skills
    )


    # -------------------------
    # HTML FOR SKILLS
    # -------------------------
    skills_html = ""

    if detected_skills:

        for skill in detected_skills:

            skills_html += f"""
            <span class="skill">
                {skill.title()}
            </span>
            """

    else:

        skills_html = """
        <p class="empty">
            No skills detected.
        </p>
        """


    # -------------------------
    # HTML FOR ROLES
    # -------------------------
    roles_html = ""

    for role, data in role_matches.items():

        matched_text = ", ".join(data["matched"]) \
            if data["matched"] else "None"

        missing_text = ", ".join(data["missing"]) \
            if data["missing"] else "None"

        roles_html += f"""

        <div class="role-card">

            <div class="role-info">

                <h3>{role}</h3>

                <p>
                    Matched:
                    <span>{matched_text}</span>
                </p>

                <p>
                    Missing:
                    <span>{missing_text}</span>
                </p>

            </div>

            <div class="role-score">
                {data["score"]}%
            </div>

        </div>

        """


    # -------------------------
    # RESULT PAGE
    # -------------------------
    return f"""

<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>Resume Analysis</title>

<link rel="preconnect"
href="https://fonts.googleapis.com">

<link rel="preconnect"
href="https://fonts.gstatic.com" crossorigin>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap"
rel="stylesheet">


<style>

* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{

    font-family: 'Poppins', sans-serif;

    background:
    radial-gradient(
        circle at top left,
        #30206b,
        #0b1024 55%,
        #070b18
    );

    color: white;

    min-height: 100vh;

}}

.container {{

    width: 92%;

    max-width: 1100px;

    margin: auto;

    padding: 50px 0;

}}

.header {{

    text-align: center;

    margin-bottom: 35px;

}}

.header h1 {{

    font-size: 40px;

    font-weight: 800;

}}

.header p {{

    color: #c7c9e8;

    margin-top: 8px;

}}


/* SCORE */

.score-section {{

    text-align: center;

    margin: 30px auto 50px;

}}

.score-title {{

    font-size: 22px;

    color: #c7c9e8;

    font-weight: 600;

}}

.score {{

    font-size: 110px;

    line-height: 1;

    font-weight: 800;

    background:
    linear-gradient(
        90deg,
        #c084fc,
        #6366f1
    );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    margin: 10px 0;

}}

.score-out-of {{

    color: #aeb3d9;

    font-size: 17px;

}}


/* CARDS */

.card {{

    background:
    linear-gradient(
        135deg,
        rgba(38,54,150,0.95),
        rgba(39,49,130,0.85)
    );

    border:
    1px solid
    rgba(130,140,255,0.55);

    border-radius: 22px;

    padding: 30px;

    margin-bottom: 25px;

    box-shadow:
    0 15px 50px
    rgba(0,0,0,0.35);

}}

.card h2 {{

    font-size: 25px;

    margin-bottom: 20px;

}}


/* SKILLS */

.skills {{

    display: flex;

    flex-wrap: wrap;

    gap: 10px;

}}

.skill {{

    padding: 9px 15px;

    background:
    rgba(139,92,246,0.25);

    border:
    1px solid
    rgba(167,139,250,0.5);

    border-radius: 25px;

    font-size: 14px;

    font-weight: 600;

}}


/* ROLE */

.role-card {{

    display: flex;

    align-items: center;

    justify-content: space-between;

    background:
    rgba(8,13,45,0.55);

    border:
    1px solid
    rgba(120,130,255,0.3);

    border-radius: 16px;

    padding: 22px;

    margin-bottom: 15px;

}}

.role-info h3 {{

    font-size: 21px;

    margin-bottom: 8px;

}}

.role-info p {{

    color: #c9cdf2;

    font-size: 14px;

    margin-top: 5px;

}}

.role-info span {{

    color: white;

    font-weight: 600;

}}

.role-score {{

    font-size: 32px;

    font-weight: 800;

    color: #c084fc;

    min-width: 100px;

    text-align: right;

}}


/* BUTTON */

.home-btn {{

    display: block;

    width: 300px;

    margin: 35px auto 0;

    padding: 15px;

    text-align: center;

    text-decoration: none;

    color: white;

    font-weight: 700;

    border-radius: 12px;

    background:
    linear-gradient(
        90deg,
        #a855f7,
        #6366f1
    );

    box-shadow:
    0 0 25px
    rgba(139,92,246,0.6);

}}

.empty {{

    color: #c7c9e8;

}}

@media(max-width:700px) {{

    .score {{

        font-size: 80px;

    }}

    .header h1 {{

        font-size: 30px;

    }}

    .role-card {{

        flex-direction: column;

        align-items: flex-start;

        gap: 15px;

    }}

    .role-score {{

        text-align: left;

    }}

}}

</style>

</head>


<body>

<div class="container">


<div class="header">

    <h1>Your Resume Analysis</h1>

    <p>
        Smart Resume Analyzer
    </p>

</div>


<!-- BIG SCORE -->

<div class="score-section">

    <div class="score-title">
        Resume Score
    </div>

    <div class="score">
        {resume_score}
    </div>

    <div class="score-out-of">
        out of 100
    </div>

</div>


<!-- SKILLS -->

<div class="card">

    <h2>Skills Detected</h2>

    <div class="skills">

        {skills_html}

    </div>

</div>


<!-- JOB ROLES -->

<div class="card">

    <h2>Job Role Matching</h2>

    {roles_html}

</div>


<a href="/" class="home-btn">
    Analyze Another Resume
</a>


</div>

</body>

</html>

"""


# -----------------------------
# START APPLICATION
# -----------------------------
if __name__ == "__main__":

    app.run(
        debug=True
    )