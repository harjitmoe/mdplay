set PYTHON=python

%PYTHON% pymdplay.py -o out.txt -f bbcode test.md
%PYTHON% pymdplay.py -o out_uicode.txt -P uicode -f bbcode test.md
%PYTHON% pymdplay.py -o out.html -f html test.md
%PYTHON% pymdplay.py -o out_uicode.html -P uicode -f html test.md
%PYTHON% pymdplay.py -o out_5.html -5 -f html test.md
%PYTHON% pymdplay.py -o out_alt.html -f htmlalt test.md
%PYTHON% pymdplay.py -o out_mw.txt -f mwiki test.md
