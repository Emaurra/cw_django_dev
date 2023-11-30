import pytest

from survey.views.question import calculate_ranking


def test_ranking_yesterday() -> None:
    """
    - Cada respuesta suma 10 puntos al ranking
    - Cada like suma 5 puntos al ranking
    - Cada dislike resta 3 puntos al ranking
    - Las preguntas del día de hoy, tienen un extra de 10 puntos
    """
    answers = 6
    liked = 2
    not_liked = 1
    is_today = 0
    ranking = calculate_ranking(answers, liked, not_liked, is_today)
    assert (
        ranking == 67
    ), f"Error calculando ranking para una pregunta creada ayer. Esperado: 67. Calculado: {ranking}."


def test_ranking_question_day() -> None:
    answers = 6
    liked = 2
    not_liked = 1
    is_today = 1
    ranking = calculate_ranking(answers, liked, not_liked, is_today)
    assert (
        ranking == 77
    ), f"Error calculando ranking para una pregunta creada hoy. Esperado: 77. Calculado: {ranking}."
