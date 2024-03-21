#variable for program intended to create
FILE = FuncStack4_ex6_19

OBJS = ${FILE}.o

#type make DEBUG=1 then DEBUGFLGS variable is -g else no debug flags
ifdef DEBUG
DEBUGFLGS = -g

else
DEBUGFLGS = 
endif

#create .o for all .s files
%.o : %.s
		as $(DEBUGFLGS) $< -o $@
${FILE}: $(OBJS)
		ld -o ${FILE} $(OBJS)

#type make clean to remover all .o files
clean: $(OBJS)
	rm *.o ${FILE}
