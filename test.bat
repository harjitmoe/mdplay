set PYTHON=..\python.exe
rem set PYTHON=Z:\mnt\c\Python27\python.exe

%PYTHON% pymdplay.py -o out.txt -f bbcode test.md
%PYTHON% pymdplay.py -o out_noemo.txt -f bbcode -W nouseemoji,notwemoji,asciimotes test.md
%PYTHON% pymdplay.py -o out_shortc.txt -f bbcode -W shortcodes test.md
%PYTHON% pymdplay.py -o out_new.txt -f html -W fragment,ipsspoilers test.md
%PYTHON% pymdplay.py -o out_newalt.txt -f htmlalt -W fragment,ipsspoilers test.md
%PYTHON% pymdplay.py -o out_htl.txt -f bbcode -W htmllists test.md
%PYTHON% pymdplay.py -o out_shtl.txt -f bbcode -W semihtmllists,autonumberonly test.md
%PYTHON% pymdplay.py -o out_nouicode.txt -P nouicode -f bbcode test.md
%PYTHON% pymdplay.py -o out.html -f html test.md
%PYTHON% pymdplay.py -o out_nouicode.html -P nouicode -f html test.md
%PYTHON% pymdplay.py -o out_5.html -5 -f html test.md
%PYTHON% pymdplay.py -o out_5tropes.html -f html -W showtropes,html5 test.md
%PYTHON% pymdplay.py -o out_alt.html -f htmlalt test.md
%PYTHON% pymdplay.py -o out_mw.txt -f mwiki test.md
%PYTHON% pymdplay.py -o out_tv.txt -f tvwiki test.md
rem %PYTHON% pymdplay.py -o json.txt -f json test.md
%PYTHON% pymdplay.py -o roundtrip.md -f md test.md
%PYTHON% pymdplay.py -o roundtrip2.md -f md roundtrip.md
%PYTHON% pymdplay.py -o roundtrip.html -f html roundtrip2.md
%PYTHON% pymdplay.py -o input_cmark.md -W nobackslashspace -f md test.md
%PYTHON% pymdplay.py -o my_output_cmark.html -P strict -W nobackslashspace -f html input_cmark.md
%PYTHON% pymdplay.py -o my_output_cmark_alt.html -P strict -W nobackslashspace -f htmlalt input_cmark.md
rem %PYTHON% c:/%PYTHON%27/Scripts/cmark.py input_cmark.md > output_cmark.html

%PYTHON% pymdplay.py -o readme.html -f htmlalt README.md

@echo Over.
:a
@goto a
