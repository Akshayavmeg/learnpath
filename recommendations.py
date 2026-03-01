COURSES = {
    "Mathematics": [
        {"title": "Algebra Fundamentals",      "duration": "4 weeks", "level": "Beginner"},
        {"title": "Geometry & Trigonometry",   "duration": "5 weeks", "level": "Intermediate"},
        {"title": "Calculus Basics",           "duration": "6 weeks", "level": "Advanced"},
        {"title": "Statistics & Probability",  "duration": "4 weeks", "level": "Intermediate"},
    ],
    "Science": [
        {"title": "Physics Mechanics",         "duration": "5 weeks", "level": "Intermediate"},
        {"title": "Chemistry Basics",          "duration": "4 weeks", "level": "Beginner"},
        {"title": "Biology Cell Theory",       "duration": "3 weeks", "level": "Beginner"},
        {"title": "Earth & Space Science",     "duration": "4 weeks", "level": "Intermediate"},
    ],
    "English": [
        {"title": "Grammar Essentials",        "duration": "3 weeks", "level": "Beginner"},
        {"title": "Essay Writing Mastery",     "duration": "4 weeks", "level": "Intermediate"},
        {"title": "Literature Analysis",       "duration": "5 weeks", "level": "Advanced"},
        {"title": "Reading Comprehension",     "duration": "3 weeks", "level": "Beginner"},
    ],
    "History": [
        {"title": "World History Overview",    "duration": "5 weeks", "level": "Beginner"},
        {"title": "Modern History Deep Dive",  "duration": "4 weeks", "level": "Intermediate"},
        {"title": "Historical Research Skills","duration": "3 weeks", "level": "Advanced"},
    ],
    "Geography": [
        {"title": "Physical Geography",        "duration": "4 weeks", "level": "Beginner"},
        {"title": "Human Geography",           "duration": "4 weeks", "level": "Intermediate"},
        {"title": "Map Reading & GIS",         "duration": "3 weeks", "level": "Intermediate"},
    ],
    "Computer Science": [
        {"title": "Programming Fundamentals",  "duration": "5 weeks", "level": "Beginner"},
        {"title": "Data Structures",           "duration": "6 weeks", "level": "Intermediate"},
        {"title": "Web Development Basics",    "duration": "5 weeks", "level": "Beginner"},
        {"title": "Algorithms & Problem Solving","duration":"6 weeks","level": "Advanced"},
    ],
}

STYLE_TIPS = {
    "Visual": {
        "tip":   "Use diagrams, charts, color-coded notes, and mind maps.",
        "tools": ["YouTube tutorials", "Infographics", "Flashcard apps", "Concept maps"],
        "icon":  "👁️",
    },
    "Auditory": {
        "tip":   "Listen to recorded lectures, read aloud, and join study groups.",
        "tools": ["Podcasts", "Audiobooks", "Discussion forums", "Voice memos"],
        "icon":  "🎧",
    },
    "Reading/Writing": {
        "tip":   "Take detailed notes, summarise chapters, and write practice essays.",
        "tools": ["Textbooks", "Note-taking apps", "Flashcards", "Study guides"],
        "icon":  "📖",
    },
    "Kinesthetic": {
        "tip":   "Use hands-on experiments, practice problems, and real-world projects.",
        "tools": ["Lab simulations", "Practice exercises", "Projects", "Interactive quizzes"],
        "icon":  "🖐️",
    },
}

WEEKLY_PLANS = {
    "Improve grades": [
        "Week 1 – Diagnostic test & identify knowledge gaps",
        "Week 2-3 – Core concept revision with daily practice",
        "Week 4 – Mock tests & timed exercises",
        "Week 5 – Error analysis & targeted re-study",
        "Week 6 – Full syllabus revision + past papers",
    ],
    "Exam preparation": [
        "Week 1 – Syllabus overview & priority topics",
        "Week 2 – Intensive topic-by-topic study",
        "Week 3 – Formula/concept sheets & memorisation",
        "Week 4 – Practice papers under exam conditions",
        "Week 5 – Review weak areas from practice tests",
        "Week 6 – Final revision & stress-management routine",
    ],
    "Build strong foundation": [
        "Week 1 – Master basic vocabulary & core definitions",
        "Week 2 – Work through foundational examples step-by-step",
        "Week 3 – Solve beginner problems independently",
        "Week 4 – Connect concepts across topics",
        "Week 5 – Apply knowledge to real-world scenarios",
        "Week 6 – Self-assessment quiz & celebration!",
    ],
    "Explore advanced topics": [
        "Week 1 – Review prerequisites & confirm readiness",
        "Week 2 – Dive into advanced theory & proofs",
        "Week 3 – Tackle complex problems & case studies",
        "Week 4 – Research projects & independent reading",
        "Week 5 – Peer teaching or blog/essay on topic",
        "Week 6 – Competitive problem sets or olympiad prep",
    ],
}


def get_recommendations(name, grade, subject, goal, style):
    courses    = COURSES.get(subject, COURSES["Mathematics"])[:3]
    style_info = STYLE_TIPS.get(style, STYLE_TIPS["Visual"])
    plan       = WEEKLY_PLANS.get(goal, WEEKLY_PLANS["Improve grades"])
    return dict(name=name, grade=grade, subject=subject, goal=goal,
                style=style, courses=courses, style_info=style_info, weekly_plan=plan)