"""Milestone 5: command-line interface."""
import argparse

from app.generate import DEFAULT_CORPUS, build_model, complete_step


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="app.cli",
                                description="Autocomplete partial recipe steps.")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("hello", help="check the tool runs")

    for name, help_ in (("complete", "complete one partial step"),
                        ("interactive", "type partial steps repeatedly")):
        s = sub.add_parser(name, help=help_)
        if name == "complete":
            s.add_argument("text", help='partial step, e.g. "Heat the oil in a"')
        s.add_argument("--corpus", default=str(DEFAULT_CORPUS))
        s.add_argument("-n", type=int, default=3, help="n-gram order (default 3)")
        s.add_argument("--max-words", type=int, default=15)
        s.add_argument("--top", type=int, default=0,
                       help="also show the top N next-word suggestions")
        s.add_argument("--sample", action="store_true",
                       help="sample randomly instead of picking the likeliest word")
        s.add_argument("--seed", type=int, default=None)

    args = p.parse_args(argv)

    if args.command == "hello":
        print("Recipe step autocompleter is ready. Try: complete \"Heat the oil in a\"")
        return 0

    model = build_model(args.corpus, n=args.n)

    def run(text: str) -> None:
        print(complete_step(model, text, max_words=args.max_words,
                            sample=args.sample, seed=args.seed))
        if args.top:
            from app.preprocess import tokenize
            options = model.top_next(tokenize(text), args.top)
            print("  next word options: " + ", ".join(f"{w} ({p:.2f})" for w, p in options))

    if args.command == "complete":
        run(args.text)
        return 0

    print("Type a partial recipe step (empty line or Ctrl-D to quit).")
    while True:
        try:
            text = input("> ").strip()
        except EOFError:
            break
        if not text:
            break
        run(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
