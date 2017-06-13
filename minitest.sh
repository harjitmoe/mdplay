python -3 pymdplay.py -o out.html -f html test.md
python -3 pymdplay.py -o out.repr -f debug test.md
python -3 pymdplay.py -o roundtrip.md -f md test.md
python -3 pymdplay.py -o roundtrip2.md -f md roundtrip.md
