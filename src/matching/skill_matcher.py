class SkillMatcher:

    @staticmethod
    def match(resume_skills: list, jd_text: str) -> dict:

        jd_lower = jd_text.lower()

        matched = [s for s in resume_skills if s.lower() in jd_lower]
        missing = [s for s in resume_skills if s.lower() not in jd_lower]

        return {
            "matched": matched,
            "missing": missing,
            "match_rate": round(
                len(matched) / len(resume_skills) * 100
            ) if resume_skills else 0
        }