def evaluate_resume():
    import re

    # Preprocess text
    resume_text = resume_text.lower()
    query = query.lower()

    # Extract individual keywords from the query
    keywords = re.findall(r'\b\w+\b', query)

    matched_keywords = []
    missing_keywords = []

    for keyword in keywords:
        if keyword in resume_text:
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    total_keywords = len(keywords)
    matched_count = len(matched_keywords)
    match_score = (matched_count / total_keywords) * 10 if total_keywords > 0 else 0

    # Determine status
    if match_score >= 8:
        status = "Pass"
    elif match_score >= 5:
        status = "Review"
    else:
        status = "Reject"

    # Build the result dictionary
    result = {
        "score": round(match_score, 2),
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "status": status,
        "explanation": f"{matched_count} out of {total_keywords} keywords matched."
    }

    return result
