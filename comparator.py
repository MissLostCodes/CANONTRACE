def compare(results):
    matches, contradictions, neutral = 0, 0, 0

    for r in results:
        if r["answer"] == "unknown":
            neutral += 1
        elif r["answer"] == "yes":
            matches += 1
        else:
            contradictions += 1

    effective = max(1, len(results) - neutral)
    score = matches / effective

    return {
        "label": "CONSISTENT" if score >= 0.6 else "CONTRADICTORY",
        "consistency_score": round(score * 100, 2),
        "contradictions": contradictions
    }
