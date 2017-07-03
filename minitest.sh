python -3 -m cProfile -o test_out/pstats.dat pymdplay.py -o test_out/out.html -f html test.md
python -3 pymdplay.py -o test_out/out.repr -f debug test.md
python -3 pymdplay.py -o test_out/out.nml -f html -F nml test.md
python -3 pymdplay.py -o test_out/out.xhtml2 -f html -F xhtml2 test.md
python -3 pymdplay.py -o test_out/out_5.xhtml2 -f html -F xhtml2 -5 test.md
python -3 pymdplay.py -o test_out/roundtrip.md -f md test.md
python -3 pymdplay.py -o test_out/roundtrip.repr -f debug test_out/roundtrip.md
python -3 pymdplay.py -o test_out/roundtrip2.md -f md test_out/roundtrip.md
