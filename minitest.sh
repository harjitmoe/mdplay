python3 -m cProfile -o test_out/pstats.dat pymdplay.py -o test_out/out.html -f html -P extradirective -W insecuredirective test.md
python3 pymdplay.py -o test_out/out.repr -f debug -P extradirective test.md
python3 pymdplay.py -o test_out/out.nml -f html -F nml test.md
python3 pymdplay.py -o test_out/out.xhtml2 -f html -F xhtml2 test.md
python3 pymdplay.py -o test_out/out_5.xhtml2 -f html -F xhtml2 -5 test.md
python3 pymdplay.py -o test_out/roundtrip.md -f md test.md
python3 pymdplay.py -o test_out/roundtrip.repr -f debug test_out/roundtrip.md
python3 pymdplay.py -o test_out/roundtrip2.md -f md test_out/roundtrip.md
