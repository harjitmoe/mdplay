python -3 -m cProfile -o pstats.dat pymdplay.py -o out.html -f html test.md
python -3 pymdplay.py -o out.repr -f debug test.md
python -3 pymdplay.py -o roundtrip.md -f md test.md
python -3 pymdplay.py -o roundtrip.repr -f debug roundtrip.md
python -3 pymdplay.py -o roundtrip2.md -f md roundtrip.md
