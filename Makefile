APPLICATION_NAME = test
TARGET=ProjectPDF
HTML=main_html
SRC=template.tex

default: compile pdf clean

both: pdf html

dvi: ${TARGET}.tex 
#	pygmentize the input source file -- THIS NAME SHOULD BE SAFE
	pygmentize -f latex -o __${SRC}.tex ${SRC}

#	run latex twice to get references correct
	latex ${TARGET}.tex

#	you can also have a bibtex line here
#	bibtex $(TARGET).tex
	latex $(TARGET).tex

#	remove the pygmentized output to avoid cluttering up the directory
	rm __${SRC}.tex

ps: dvi
	dvips -R -Poutline -t letter ${TARGET}.dvi -o ${TARGET}.ps

pdf: ps
	ps2pdf ${TARGET}.ps


html:
	cp ${TARGET}.tex ${HTML}.tex
	latex ${HTML}.tex
	latex2html -split 0 -noshow_section_numbers -local_icons -no_navigation -noinfo -noaddress ${HTML}

	sed 's/<BR><HR>//g' < ${HTML}/index.html > ${HTML}/index2.html
	mv ${HTML}/index2.html ${TARGET}.html
	rm ${HTML}.*
	rm -rf ${HTML}
	
##=============================================================================
# Compile
##=============================================================================

#Compiler (icc or gcc)
CC = icc

#overkill on the flags, but that doesn't hurt anything
CFLAGS = -Wall -std=c99 -openmp -O3 -g -I.
CXXFLAGS = -Wall -openmp -O3 -g
LDFLAGS = -lrt -lpthread 

#replace this if you want to change the output name
CCTARGET = ${APPLICATION_NAME}

#any headers go here
C_INCLUDES = 

#any .c or .cpp files go here
C_SOURCE = 

#depends on all of you source and header files
compile: 
	${C_SOURCE} ${C_INCLUDES}
	#this assumes you actually are linking all of the source files together
	${CC} ${CFLAGS} ${C_SOURCE} -o ${CCTARGET} ${LDFLAGS}
	
##=============================================================================
# Clean
##=============================================================================

clean:
	rm -rf *.out *.exe

	
##=============================================================================
# Stutest.out
##=============================================================================

stutest.out:
	echo 'running stutest.out'

	
##=============================================================================
# Proftest.out
##=============================================================================

proftest.out:
	echo 'running proftest.out'


