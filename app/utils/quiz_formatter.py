def display_quiz(quiz):
    return {
        "id": quiz.id,
        "title": quiz.title,
        "owner": quiz.owner.username if quiz.owner else None,
        "questions": [
            {
                "id": q.id,
                "text": q.text,
                "is_multiple": q.is_multiple,
                "options": [
                    {"id": o.id, "text": o.text}
                    for o in q.options
                ]
            }
            for q in quiz.questions
        ]
    }
