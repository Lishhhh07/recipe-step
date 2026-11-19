from app.cli import main


def test_hello(capsys):
    assert main(["hello"]) == 0
    assert "ready" in capsys.readouterr().out


def test_complete(capsys):
    assert main(["complete", "Preheat the oven to", "--top", "3"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("Preheat the oven to") and "next word options" in out
