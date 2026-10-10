%Simulation Methods for Electronic Circuits 
%Systematic Analysis of Linear and non-Linear Circuits 
%Problem #1
 
%Sinusoidal Input
VL = 10e-3;
%Circuit Component Values
R1 = 1e3;
R5 = R1;
R2 = 3.3e3;
R3 = R2;
C4 = 1e-6;
%Frequency Analysis
points = 100;
F_start = 10;
F_stop = 1e3;
freq = linspace(F_start,F_stop,points);
%INCIDENCE MATRIX
A = [1  0  0  0  1  0  0  0  0  1;
     0  0  0  1 -1  1  0  0  0  0;
    -1  0  1  0  0 -1  1  0  0  0;
     0  1  0  0  0  0 -1  1  0  0;
     0  0 -1  0  0  0  0 -1  1  0];
%IMPEDANCE MATRX
 Z = [0   0   0   0   0   0   0   0   0   0;
      1   0   0   0   0   0   0   0   0   0;
      0   0   0   0   0   0   0   0   0   0;
      0   0   1   0   0   0   0   0   0   0;
      0   0   0   0  -R1  0   0   0   0   0;
      0   0   0   0   0  -R2  0   0   0   0;
      0   0   0   0   0   0  -R3  0   0   0;
      0   0   0   0   0   0   0  -1   0   0;
      0   0   0   0   0   0   0   0  -R5  0;
      0   0   0   0   0   0   0   0   0   0];
  %SOURCE VECTOR
  W = [0 0 0 0 0 0 0 0 0 VL]';
 %# of Circuit Nodes
 %# of Circuit Branches
  [nodes,branches] = size(A); 
 %Tableau equation: TX=W'
   Wp= [zeros(branches,1);
       W;
       zeros(nodes,1)]; 
 %Variable Inizilitation
 V_input = zeros(1,points);
 V_output = zeros(1,points);
 IL = zeros(1,points);
 ZL = zeros(1,points);
 ZL2 = zeros(1,points);
 j = sqrt(-1);
   
 for k = 1:points
     w = 2*pi*freq(k);
     Y = [1   0   0   0   0   0   0   0    0   0;
          0   0   0   0   0   0   0   0    0   0;
          0   0   1   0   0   0   0   0    0   0;
          0   0   0   0   0   0   0   0    0   0;
          0   0   0   0   1   0   0   0    0   0;
          0   0   0   0   0   1   0   0    0   0;
          0   0   0   0   0   0   1   0    0   0;
          0   0   0   0   0   0   0 (j*w*C4) 0   0;
          0   0   0   0   0   0   0   0    1   0;
          0   0   0   0   0   0   0   0    0   1];
  %Assemble matrix T
       T = [eye(branches) zeros(branches,branches) (-A');  
           Y       Z     zeros(branches,nodes);
           zeros(nodes,branches) A  zeros(nodes,nodes)];
  %Tableau equation: TX=W'
       X = T\Wp;  
       Vb = X(1:branches);
       I = X(branches+1:2*branches);
       Vn = X(2*branches+1:end);
       %Voltage at Node 1
       V_input(k) = Vn(1);
       IL(k) = I(5)+I(1);
       ZL(k) = V_input(k)/IL(k);
       %Circuit Analysis Equation
       ZL2(k)=j*w*C4*R1*R3*R5/R2;
       Leq2=C4*R1*R3*R5/R2;
 end
    
    figure
    plot(freq/1000,abs(ZL)/1000);
    grid on
    xlabel('Frecuency (KHz)')
    ylabel('ZL Tableau (KOhms)')
    figure
    plot(freq/1000,abs(ZL2)/1000);
    grid on
    xlabel('Frecuency (KHz)')
    ylabel('ZL Circuit Analysis (KOhms)')
    figure
    plot(freq,abs(IL));
    grid on
    xlabel('Frecuency (Hz)')
    ylabel('Ii (Amp)')
 
