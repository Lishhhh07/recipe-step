from app.generate import build_model, complete_step, continue_step


def test_continuation_is_sensible():
    m = build_model()
    out = continue_step(m, "Preheat the oven to")
    assert out and "degrees" in out


def test_complete_keeps_prefix():
    m = build_model()
    assert complete_step(m, "Bring a large pot of").startswith("Bring a large pot of")


def test_sampling_seeded_is_deterministic():
    m = build_model()
    a = continue_step(m, "Add the", sample=True, seed=1)
    b = continue_step(m, "Add the", sample=True, seed=1)
    assert a == b


def test_empty_input_still_works():
    assert isinstance(continue_step(build_model(), ""), str)
