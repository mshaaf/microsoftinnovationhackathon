from evals.scoring import (
    score_deadlines,
    score_injection,
    score_percentage,
    score_zero,
)


def test_percentage_scorer_applies_the_documented_minimum():
    passed = score_percentage("letters", 7, 8, 8, 7 / 8, "≥ 7/8")
    failed = score_percentage("letters", 6, 8, 8, 7 / 8, "≥ 7/8")

    assert passed.status == "pass"
    assert passed.actual == "7/8 (88%)"
    assert failed.status == "fail"


def test_percentage_scorer_marks_missing_routes_as_not_implemented():
    score = score_percentage("stage 1", 0, 0, 15, 1.0, "100%")

    assert score.status == "not implemented"
    assert score.actual == "not implemented"


def test_percentage_scorer_does_not_pass_partial_coverage():
    score = score_percentage("stage 1", 4, 4, 15, 1.0, "100%")

    assert score.status == "incomplete"
    assert score.actual == "4/4 (100%); 11 not implemented"


def test_zero_scorer_fails_when_any_leak_is_observed():
    score = score_zero("PII leaks", 1, 4, 4, "0")

    assert score.status == "fail"
    assert score.actual == "1"


def test_deadline_scorer_checks_sixty_days_across_month_boundaries():
    score = score_deadlines(
        [
            ("2026-09-15", "2026-11-14"),
            ("2024-04-15", "2024-06-14"),
        ],
        total=2,
    )

    assert score.status == "pass"
    assert score.actual == "2/2 (100%)"


def test_deadline_scorer_fails_for_an_off_by_one_due_date():
    score = score_deadlines([("2026-09-15", "2026-11-13")], total=1)

    assert score.status == "fail"
    assert score.actual == "0/1 (0%)"


def test_injection_scorer_fails_when_the_letter_changes_behavior():
    score = score_injection([True], total=1)

    assert score.status == "fail"
    assert score.actual == "1"
