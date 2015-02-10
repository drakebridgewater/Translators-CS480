APPLICATION_NAME = tree
TARGET=example
HTML=main_html
SRC=tree.py

default: compile pdf clean stutest.out

both: pdf html

dvi: ${TARGET}.tex 
#	pygmentize the input source file -- THIS NAME SHOULD BE SAFE
#	echo entered pygmentize
#	pygmentize -f latex -o __${SRC}.tex ${SRC}

	rm -rf log_latex
#	run latex twice to get references correct
	latex ${TARGET}.tex >> log_latex

#	you can also have a bibtex line here
#	bibtex $(TARGET).tex
	latex $(TARGET).tex >> log_latex

#	remove the pygmentized output to avoid cluttering up the directory
#	rm __${SRC}.tex

ps: dvi
	echo entered ps
	dvips -R -Poutline -t letter ${TARGET}.dvi -o ${TARGET}.ps >> log_latex

pdf: ps
	echo entered pdf
	ps2pdf ${TARGET}.ps >> log_latex


html:
	echo entered html 
	cp ${TARGET}.tex ${HTML}.tex
	latex ${HTML}.tex >> log_latex
	latex2html -split 0 -noshow_section_numbers -local_icons -no_navigation -noinfo -noaddress ${HTML} >> log_latex

	sed 's/<BR><HR>//g' < ${HTML}/index.html > ${HTML}/index2.html
	mv ${HTML}/index2.html ${TARGET}.html
	rm ${HTML}.*
	rm -rf ${HTML}
	
##=============================================================================
# Compile
##=============================================================================
compile:
	echo python code does not need compiled
##=============================================================================
# Clean
##=============================================================================

clean:
	rm -rf *.out *.exe *.aux *.log *.dvi

##=============================================================================
# Stutest.out
##=============================================================================

stutest.out:
	echo 'Running stutest.in and storing int stutest.out'
	python main.py test > stutest.out

	
##=============================================================================
# Proftest.out
##=============================================================================

proftest.out:
	echo 'Running proftest.in and storing in proftest.out'
	python3.4 main.py proftest.in > proftest.out

