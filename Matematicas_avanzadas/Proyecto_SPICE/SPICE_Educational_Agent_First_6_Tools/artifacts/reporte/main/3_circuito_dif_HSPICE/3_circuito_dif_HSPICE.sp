* HSPICE conversion of the educational active-filter netlist
V1 IN 0 AC 1 0
C1 IN N1 1u
L1 N1 OUT 10m
R1 OUT 0 1k
.OP
.OPTIONS POST=2
.AC DEC 100 10 100k
.PRINT AC VM(OUT) VDB(OUT) VP(OUT)
.END
