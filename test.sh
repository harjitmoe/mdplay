python pymdplay.py -o test_out/out.txt -f bbcode test.md
python pymdplay.py -o test_out/out.repr -f debug test.md
python pymdplay.py -o test_out/out_noemo.txt -f bbcode -W nouseemoji,notwemoji,asciimotes test.md
python pymdplay.py -o test_out/out_shortc.txt -f bbcode -W shortcodes test.md
python pymdplay.py -o test_out/out_new.txt -f html -W fragment,ipsspoilers,nounicodeemoji test.md
python pymdplay.py -o test_out/out_htl.txt -f bbcode -W htmllists test.md
python pymdplay.py -o test_out/out_shtl.txt -f bbcode -W semihtmllists,autonumberonly test.md
python pymdplay.py -o test_out/out_nouicode.txt -P nouicode -f bbcode test.md
python pymdplay.py -o test_out/out.html -f html test.md
python pymdplay.py -o test_out/out_nouicode.html -P nouicode -f html test.md
python pymdplay.py -o test_out/out_5.html -5 -f html test.md
python pymdplay.py -o test_out/out_5tropes.html -f html -W showtropes,html5 test.md
python pymdplay.py -o test_out/out_mw.txt -f mwiki test.md
python pymdplay.py -o test_out/out_tv.txt -f tvwiki test.md
python pymdplay.py -o test_out/out.nml -f html -F nml test.md
python pymdplay.py -o test_out/out.xhtml2 -f html -F xhtml2 test.md
python pymdplay.py -o test_out/out_5.xhtml2 -f html -F xhtml2 -5 test.md
python pymdplay.py -o test_out/roundtrip.md -f md test.md
python pymdplay.py -o test_out/roundtrip2.md -f md test_out/roundtrip.md
python pymdplay.py -o test_out/roundtrip.html -f html test_out/roundtrip2.md
python pymdplay.py -o test_out/input_cmark.md -W nobackslashspace -f md test.md
python pymdplay.py -o test_out/my_output_cmark.html -P strict -W nobackslashspace -f html test_out/input_cmark.md
#python3 /mnt/c/Python27/Scripts/cmark.py test_out/input_cmark.md > output_cmark.html

python pymdplay.py -o readme.html -f html README.md
