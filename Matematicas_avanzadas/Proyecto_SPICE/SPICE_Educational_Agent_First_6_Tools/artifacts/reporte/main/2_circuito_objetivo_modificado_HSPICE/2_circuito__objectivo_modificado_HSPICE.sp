* HSPICE conversion of the educational active-filter netlist
* Linear AC transfer: Vi=1 V, so V(OUT) is numerically equal to Vo/Vi.
* U1 is approximated by a finite open-loop-gain VCVS; it is not an ideal op-amp.
V1 IN 0 AC 10 0
C1 IN N1 0.50u
C2 N1 NP 0.50u
* Project G elements are conductances, not HSPICE VCCS devices.
* Equivalent resistances: 1/G1=1.27k, 1/G2=2.3k.
RG1 N1 OUT 3k
RG2 NP 0 1.5k
RB OUT NM 1.5k
RA NM 0 3k
* Finite-gain voltage-controlled voltage source approximation of U1.
* HSPICE E syntax: Ename N+ N- NC+ NC- gain.
EOP OUT 0 NP NM 1e9
.OP
.OPTIONS POST=2
.AC DEC 100 10 100k
.PRINT AC VM(OUT) VDB(OUT) VP(OUT)
.END
