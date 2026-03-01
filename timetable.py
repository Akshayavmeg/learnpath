DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

SLOTS = {
    "Visual": [
        ("06:30 – 07:30", "Watch video lecture & draw concept map"),
        ("15:00 – 16:30", "Colour-coded notes & diagram revision"),
        ("19:00 – 20:00", "Flashcard review with images"),
    ],
    "Auditory": [
        ("06:30 – 07:30", "Listen to podcast / recorded lecture"),
        ("15:00 – 16:30", "Read notes aloud & summarise verbally"),
        ("19:00 – 20:00", "Group discussion or study-buddy session"),
    ],
    "Reading/Writing": [
        ("06:30 – 07:30", "Textbook reading & detailed note-taking"),
        ("15:00 – 16:30", "Summarise chapter in own words"),
        ("19:00 – 20:00", "Write practice questions & answers"),
    ],
    "Kinesthetic": [
        ("06:30 – 07:30", "Hands-on exercise / interactive simulation"),
        ("15:00 – 16:30", "Solve practice problems independently"),
        ("19:00 – 20:00", "Mini project or real-world application"),
    ],
}

GOAL_EXTRAS = {
    "Improve grades":         ("17:00 – 17:30", "Past paper Q&A sprint (10 questions)"),
    "Exam preparation":       ("17:00 – 17:30", "Timed mock test section"),
    "Build strong foundation":("17:00 – 17:30", "Concept review quiz (self-assessed)"),
    "Explore advanced topics":("17:00 – 17:30", "Research / extension reading"),
}

WEEKEND_SLOT = ("10:00 – 12:00", "Weekly revision & weak-area focus")


def generate_timetable(subject, style, goal):
    base_slots  = SLOTS.get(style, SLOTS["Visual"])
    extra_time, extra_act = GOAL_EXTRAS.get(goal, ("17:00 – 17:30", "Review"))
    timetable   = []

    for i, day in enumerate(DAYS):
        if day in ("Saturday", "Sunday"):
            timetable.append({"day": day, "time": WEEKEND_SLOT[0],
                               "activity": WEEKEND_SLOT[1], "subject": subject})
            timetable.append({"day": day, "time": "14:00 – 15:00",
                               "activity": "Rest & light reading", "subject": "General"})
        else:
            slot_idx = i % len(base_slots)
            time_s, act = base_slots[slot_idx]
            timetable.append({"day": day, "time": time_s,
                               "activity": act, "subject": subject})
            timetable.append({"day": day, "time": extra_time,
                               "activity": extra_act, "subject": subject})
            timetable.append({"day": day, "time": "20:30 – 21:00",
                               "activity": "Plan tomorrow / journal progress", "subject": "General"})
    return timetable