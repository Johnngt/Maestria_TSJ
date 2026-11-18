# Reporte de simulación de circuito

- **Fuente:** filtro_pasa_altas_rlc.cir
- **Método:** TABLEAU
- **Ejecución:** filtro_pasa_altas_RLC_normalizado_20261116_1901
- **Estado:** PASS

## Netlist original

```spice
* Filtro pasa-altas RLC serie (nodos en mayusculas para parser educativo)
V1 IN 0 AC 1 0
C1 IN N1 1u
L1 N1 OUT 10m
R1 OUT 0 1k
.AC LIN 400 10 100k
.END

```

## Componentes normalizados

| Componente | Tipo | Desde | Hacia | Valor SI | Unidad | Rama | L?nea |
| ---------- | ---- | ----- | ----- | -------: | ------ | ---- | ----: |
| V1         | V    | IN    | 0     |        1 | volt   | B1   |     2 |
| C1         | C    | IN    | N1    |    1e-06 | farad  | B2   |     3 |
| L1         | L    | N1    | OUT   |     0.01 | henry  | B3   |     4 |
| R1         | R    | OUT   | 0     |     1000 | ohm    | B4   |     5 |

## Nodos

| Nodo | Referencia | Índice completo | Índice reducido |
| ---- | :--------: | --------------: | --------------: |
| 0    |     sí     |               0 |            None |
| IN   |     no     |               1 |               0 |
| N1   |     no     |               2 |               1 |
| OUT  |     no     |               3 |               2 |

## Topología

Conectado: **True**

| Desde | Hacia | Rama | Componente |
| ----- | ----- | ---- | ---------- |
| IN    | 0     | B1   | V1         |
| IN    | N1    | B2   | C1         |
| N1    | OUT   | B3   | L1         |
| OUT   | 0     | B4   | R1         |

## Matriz de incidencia reducida

|     | B1  | B2  | B3  | B4  |
| --- | --- | --- | --- | --- |
| IN  | 1   | 1   | 0   | 0   |
| N1  | 0   | -1  | 1   | 0   |
| OUT | 0   | 0   | -1  | 1   |

## Ecuaciones constitutivas

| Rama | Componente | Ecuación      | Línea de origen |
| ---- | ---------- | ------------- | --------------: |
| B1   | V1         | V = E         |               2 |
| B2   | C1         | s*C*V - I = 0 |               3 |
| B3   | L1         | V - s*L*I = 0 |               4 |
| B4   | R1         | V - R*I = 0   |               5 |

### Matriz Y

|     | B1  | B2                 | B3  | B4  |
| --- | --- | ------------------ | --- | --- |
| B1  | 1   | 0                  | 0   | 0   |
| B2  | 0   | 0 + j6.2831853e-05 | 0   | 0   |
| B3  | 0   | 0                  | 1   | 0   |
| B4  | 0   | 0                  | 0   | 1   |

### Matriz Z

|     | B1  | B2  | B3              | B4    |
| --- | --- | --- | --------------- | ----- |
| B1  | 0   | 0   | 0               | 0     |
| B2  | 0   | -1  | 0               | 0     |
| B3  | 0   | 0   | 0 - j0.62831853 | 0     |
| B4  | 0   | 0   | 0               | -1000 |

### Vector W

| Label | Value |
| ----- | ----- |
| B1    | 1     |
| B2    | 0     |
| B3    | 0     |
| B4    | 0     |

## Sistema ensamblado

Formulación: `TABLEAU`; dimensiones: `11 × 11`.

|                  | V(B1) | V(B2)              | V(B3) | V(B4) | I(B1) | I(B2) | I(B3)           | I(B4) | V(NIN) | V(NN1) | V(NOUT) |
| ---------------- | ----- | ------------------ | ----- | ----- | ----- | ----- | --------------- | ----- | ------ | ------ | ------- |
| KVL(B1)          | 1     | 0                  | 0     | 0     | 0     | 0     | 0               | 0     | -1     | -0     | -0      |
| KVL(B2)          | 0     | 1                  | 0     | 0     | 0     | 0     | 0               | 0     | -1     | 1      | -0      |
| KVL(B3)          | 0     | 0                  | 1     | 0     | 0     | 0     | 0               | 0     | -0     | -1     | 1       |
| KVL(B4)          | 0     | 0                  | 0     | 1     | 0     | 0     | 0               | 0     | -0     | -0     | -1      |
| CONSTITUTIVE(B1) | 1     | 0                  | 0     | 0     | 0     | 0     | 0               | 0     | 0      | 0      | 0       |
| CONSTITUTIVE(B2) | 0     | 0 + j6.2831853e-05 | 0     | 0     | 0     | -1    | 0               | 0     | 0      | 0      | 0       |
| CONSTITUTIVE(B3) | 0     | 0                  | 1     | 0     | 0     | 0     | 0 - j0.62831853 | 0     | 0      | 0      | 0       |
| CONSTITUTIVE(B4) | 0     | 0                  | 0     | 1     | 0     | 0     | 0               | -1000 | 0      | 0      | 0       |
| KCL(NIN)         | 0     | 0                  | 0     | 0     | 1     | 1     | 0               | 0     | 0      | 0      | 0       |
| KCL(NN1)         | 0     | 0                  | 0     | 0     | 0     | -1    | 1               | 0     | 0      | 0      | 0       |
| KCL(NOUT)        | 0     | 0                  | 0     | 0     | 0     | 0     | -1              | 1     | 0      | 0      | 0       |

### Vector del lado derecho

| Label            | Value |
| ---------------- | ----- |
| KVL(B1)          | 0     |
| KVL(B2)          | 0     |
| KVL(B3)          | 0     |
| KVL(B4)          | 0     |
| CONSTITUTIVE(B1) | 1     |
| CONSTITUTIVE(B2) | 0     |
| CONSTITUTIVE(B3) | 0     |
| CONSTITUTIVE(B4) | 0     |
| KCL(NIN)         | 0     |
| KCL(NN1)         | 0     |
| KCL(NOUT)        | 0     |

## Resultados AC

Barrido `LIN`; estado global: **PASS**.

| Frecuencia (Hz) | Estado | Transferencias calculadas                                                    |
| --------------: | ------ | ---------------------------------------------------------------------------- |
|              10 | PASS   | V(OUT)/V(IN): magnitud=0.06271066, fase=86.404585 grados, dB=-24.053173      |
|        260.6015 | PASS   | V(OUT)/V(IN): magnitud=0.85962921, fase=30.725024 grados, dB=-1.3137767      |
|       511.20301 | PASS   | V(OUT)/V(IN): magnitud=0.96316025, fase=15.600493 grados, dB=-0.32602897     |
|       761.80451 | PASS   | V(OUT)/V(IN): magnitud=0.98727796, fase=9.1490805 grados, dB=-0.11121113     |
|        1012.406 | PASS   | V(OUT)/V(IN): magnitud=0.99564871, fase=5.3469257 grados, dB=-0.037877274    |
|       1263.0075 | PASS   | V(OUT)/V(IN): magnitud=0.9989134, fase=2.6712297 grados, dB=-0.0094431941    |
|        1513.609 | PASS   | V(OUT)/V(IN): magnitud=0.99994954, fase=0.57559979 grados, dB=-0.00043831628 |
|       1764.2105 | PASS   | V(OUT)/V(IN): magnitud=0.99978716, fase=-1.1821589 grados, dB=-0.0018489346  |
|        2014.812 | PASS   | V(OUT)/V(IN): magnitud=0.99886895, fase=-2.7253319 grados, dB=-0.0098297324  |
|       2265.4135 | PASS   | V(OUT)/V(IN): magnitud=0.9974119, fase=-4.1230845 grados, dB=-0.02250913     |
|        2516.015 | PASS   | V(OUT)/V(IN): magnitud=0.99553382, fase=-5.41711 grados, dB=-0.038879659     |
|       2766.6165 | PASS   | V(OUT)/V(IN): magnitud=0.99330446, fase=-6.6339646 grados, dB=-0.058352316   |
|        3017.218 | PASS   | V(OUT)/V(IN): magnitud=0.99076841, fase=-7.7913127 grados, dB=-0.080557012   |
|       3267.8195 | PASS   | V(OUT)/V(IN): magnitud=0.9879563, fase=-8.9013212 grados, dB=-0.10524532     |
|       3518.4211 | PASS   | V(OUT)/V(IN): magnitud=0.98489065, fase=-9.9726121 grados, dB=-0.13223975    |
|       3769.0226 | PASS   | V(OUT)/V(IN): magnitud=0.98158906, fase=-11.011442 grados, dB=-0.16140581    |
|       4019.6241 | PASS   | V(OUT)/V(IN): magnitud=0.9780661, fase=-12.02244 grados, dB=-0.1926359       |
|       4270.2256 | PASS   | V(OUT)/V(IN): magnitud=0.97433436, fase=-13.009092 grados, dB=-0.22583966    |
|       4520.8271 | PASS   | V(OUT)/V(IN): magnitud=0.97040517, fase=-13.974057 grados, dB=-0.26093798    |
|       4771.4286 | PASS   | V(OUT)/V(IN): magnitud=0.966289, fase=-14.919392 grados, dB=-0.29785931      |
|       5022.0301 | PASS   | V(OUT)/V(IN): magnitud=0.96199573, fase=-15.846705 grados, dB=-0.33653716    |
|       5272.6316 | PASS   | V(OUT)/V(IN): magnitud=0.95753482, fase=-16.757264 grados, dB=-0.37690852    |
|       5523.2331 | PASS   | V(OUT)/V(IN): magnitud=0.95291542, fase=-17.652081 grados, dB=-0.41891287    |
|       5773.8346 | PASS   | V(OUT)/V(IN): magnitud=0.94814646, fase=-18.531969 grados, dB=-0.46249142    |
|       6024.4361 | PASS   | V(OUT)/V(IN): magnitud=0.94323665, fase=-19.397587 grados, dB=-0.50758669    |
|       6275.0376 | PASS   | V(OUT)/V(IN): magnitud=0.93819451, fase=-20.249474 grados, dB=-0.55414224    |
|       6525.6391 | PASS   | V(OUT)/V(IN): magnitud=0.93302843, fase=-21.088077 grados, dB=-0.60210247    |
|       6776.2406 | PASS   | V(OUT)/V(IN): magnitud=0.92774661, fase=-21.913767 grados, dB=-0.65141249    |
|       7026.8421 | PASS   | V(OUT)/V(IN): magnitud=0.92235709, fase=-22.726857 grados, dB=-0.70201815    |
|       7277.4436 | PASS   | V(OUT)/V(IN): magnitud=0.91686776, fase=-23.527618 grados, dB=-0.75386593    |
|       7528.0451 | PASS   | V(OUT)/V(IN): magnitud=0.91128631, fase=-24.31628 grados, dB=-0.80690305     |
|       7778.6466 | PASS   | V(OUT)/V(IN): magnitud=0.90562026, fase=-25.093048 grados, dB=-0.86107741    |
|       8029.2481 | PASS   | V(OUT)/V(IN): magnitud=0.89987692, fase=-25.858106 grados, dB=-0.9163377     |
|       8279.8496 | PASS   | V(OUT)/V(IN): magnitud=0.89406343, fase=-26.611618 grados, dB=-0.97263339    |
|       8530.4511 | PASS   | V(OUT)/V(IN): magnitud=0.88818669, fase=-27.353736 grados, dB=-1.0299148     |
|       8781.0526 | PASS   | V(OUT)/V(IN): magnitud=0.8822534, fase=-28.084604 grados, dB=-1.0881332      |
|       9031.6541 | PASS   | V(OUT)/V(IN): magnitud=0.87627005, fase=-28.804356 grados, dB=-1.1472406     |
|       9282.2556 | PASS   | V(OUT)/V(IN): magnitud=0.87024289, fase=-29.513123 grados, dB=-1.2071903     |
|       9532.8571 | PASS   | V(OUT)/V(IN): magnitud=0.86417794, fase=-30.211031 grados, dB=-1.2679365     |
|       9783.4586 | PASS   | V(OUT)/V(IN): magnitud=0.858081, fase=-30.898204 grados, dB=-1.3294342       |
|        10034.06 | PASS   | V(OUT)/V(IN): magnitud=0.85195764, fase=-31.574764 grados, dB=-1.39164       |
|       10284.662 | PASS   | V(OUT)/V(IN): magnitud=0.84581318, fase=-32.240834 grados, dB=-1.4545111     |
|       10535.263 | PASS   | V(OUT)/V(IN): magnitud=0.83965271, fase=-32.896535 grados, dB=-1.5180061     |
|       10785.865 | PASS   | V(OUT)/V(IN): magnitud=0.83348111, fase=-33.541989 grados, dB=-1.5820848     |
|       11036.466 | PASS   | V(OUT)/V(IN): magnitud=0.827303, fase=-34.17732 grados, dB=-1.646708         |
|       11287.068 | PASS   | V(OUT)/V(IN): magnitud=0.8211228, fase=-34.802651 grados, dB=-1.7118378      |
|       11537.669 | PASS   | V(OUT)/V(IN): magnitud=0.81494468, fase=-35.418107 grados, dB=-1.7774374     |
|       11788.271 | PASS   | V(OUT)/V(IN): magnitud=0.80877262, fase=-36.023815 grados, dB=-1.8434712     |
|       12038.872 | PASS   | V(OUT)/V(IN): magnitud=0.80261035, fase=-36.6199 grados, dB=-1.9099049       |
|       12289.474 | PASS   | V(OUT)/V(IN): magnitud=0.79646142, fase=-37.206491 grados, dB=-1.9767052     |
|       12540.075 | PASS   | V(OUT)/V(IN): magnitud=0.79032915, fase=-37.783718 grados, dB=-2.04384       |
|       12790.677 | PASS   | V(OUT)/V(IN): magnitud=0.78421669, fase=-38.35171 grados, dB=-2.1112784      |
|       13041.278 | PASS   | V(OUT)/V(IN): magnitud=0.77812698, fase=-38.910598 grados, dB=-2.1789906     |
|        13291.88 | PASS   | V(OUT)/V(IN): magnitud=0.77206276, fase=-39.460514 grados, dB=-2.2469479     |
|       13542.481 | PASS   | V(OUT)/V(IN): magnitud=0.76602661, fase=-40.00159 grados, dB=-2.3151229      |
|       13793.083 | PASS   | V(OUT)/V(IN): magnitud=0.76002093, fase=-40.533957 grados, dB=-2.383489      |
|       14043.684 | PASS   | V(OUT)/V(IN): magnitud=0.75404794, fase=-41.05775 grados, dB=-2.4520208      |
|       14294.286 | PASS   | V(OUT)/V(IN): magnitud=0.74810973, fase=-41.573099 grados, dB=-2.520694      |
|       14544.887 | PASS   | V(OUT)/V(IN): magnitud=0.74220819, fase=-42.080139 grados, dB=-2.5894851     |
|       14795.489 | PASS   | V(OUT)/V(IN): magnitud=0.73634511, fase=-42.579002 grados, dB=-2.6583719     |
|        15046.09 | PASS   | V(OUT)/V(IN): magnitud=0.73052209, fase=-43.069819 grados, dB=-2.7273329     |
|       15296.692 | PASS   | V(OUT)/V(IN): magnitud=0.72474064, fase=-43.552723 grados, dB=-2.7963476     |
|       15547.293 | PASS   | V(OUT)/V(IN): magnitud=0.71900212, fase=-44.027845 grados, dB=-2.8653966     |
|       15797.895 | PASS   | V(OUT)/V(IN): magnitud=0.71330775, fase=-44.495315 grados, dB=-2.9344611     |
|       16048.496 | PASS   | V(OUT)/V(IN): magnitud=0.70765867, fase=-44.955264 grados, dB=-3.0035234     |
|       16299.098 | PASS   | V(OUT)/V(IN): magnitud=0.70205588, fase=-45.407819 grados, dB=-3.0725664     |
|       16549.699 | PASS   | V(OUT)/V(IN): magnitud=0.69650028, fase=-45.853109 grados, dB=-3.1415741     |
|       16800.301 | PASS   | V(OUT)/V(IN): magnitud=0.69099269, fase=-46.29126 grados, dB=-3.210531       |
|       17050.902 | PASS   | V(OUT)/V(IN): magnitud=0.68553381, fase=-46.722398 grados, dB=-3.2794225     |
|       17301.504 | PASS   | V(OUT)/V(IN): magnitud=0.68012426, fase=-47.146646 grados, dB=-3.3482347     |
|       17552.105 | PASS   | V(OUT)/V(IN): magnitud=0.67476459, fase=-47.564128 grados, dB=-3.4169544     |
|       17802.707 | PASS   | V(OUT)/V(IN): magnitud=0.66945524, fase=-47.974966 grados, dB=-3.4855691     |
|       18053.308 | PASS   | V(OUT)/V(IN): magnitud=0.66419662, fase=-48.379279 grados, dB=-3.5540668     |
|        18303.91 | PASS   | V(OUT)/V(IN): magnitud=0.65898902, fase=-48.777185 grados, dB=-3.6224365     |
|       18554.511 | PASS   | V(OUT)/V(IN): magnitud=0.6538327, fase=-49.168802 grados, dB=-3.6906673      |
|       18805.113 | PASS   | V(OUT)/V(IN): magnitud=0.64872784, fase=-49.554245 grados, dB=-3.7587492     |
|       19055.714 | PASS   | V(OUT)/V(IN): magnitud=0.64367458, fase=-49.933627 grados, dB=-3.8266728     |
|       19306.316 | PASS   | V(OUT)/V(IN): magnitud=0.63867299, fase=-50.307062 grados, dB=-3.894429      |
|       19556.917 | PASS   | V(OUT)/V(IN): magnitud=0.63372308, fase=-50.674658 grados, dB=-3.9620095     |
|       19807.519 | PASS   | V(OUT)/V(IN): magnitud=0.62882485, fase=-51.036525 grados, dB=-4.0294061     |
|        20058.12 | PASS   | V(OUT)/V(IN): magnitud=0.62397822, fase=-51.392769 grados, dB=-4.0966114     |
|       20308.722 | PASS   | V(OUT)/V(IN): magnitud=0.61918308, fase=-51.743497 grados, dB=-4.1636183     |
|       20559.323 | PASS   | V(OUT)/V(IN): magnitud=0.6144393, fase=-52.08881 grados, dB=-4.2304203       |
|       20809.925 | PASS   | V(OUT)/V(IN): magnitud=0.60974668, fase=-52.428812 grados, dB=-4.2970111     |
|       21060.526 | PASS   | V(OUT)/V(IN): magnitud=0.60510501, fase=-52.763601 grados, dB=-4.363385      |
|       21311.128 | PASS   | V(OUT)/V(IN): magnitud=0.60051406, fase=-53.093276 grados, dB=-4.4295364     |
|       21561.729 | PASS   | V(OUT)/V(IN): magnitud=0.59597355, fase=-53.417934 grados, dB=-4.4954603     |
|       21812.331 | PASS   | V(OUT)/V(IN): magnitud=0.59148318, fase=-53.73767 grados, dB=-4.561152       |
|       22062.932 | PASS   | V(OUT)/V(IN): magnitud=0.58704264, fase=-54.052575 grados, dB=-4.626607      |
|       22313.534 | PASS   | V(OUT)/V(IN): magnitud=0.58265158, fase=-54.362742 grados, dB=-4.6918214     |
|       22564.135 | PASS   | V(OUT)/V(IN): magnitud=0.57830964, fase=-54.668261 grados, dB=-4.7567913     |
|       22814.737 | PASS   | V(OUT)/V(IN): magnitud=0.57401645, fase=-54.969218 grados, dB=-4.8215133     |
|       23065.338 | PASS   | V(OUT)/V(IN): magnitud=0.5697716, fase=-55.2657 grados, dB=-4.8859841        |
|        23315.94 | PASS   | V(OUT)/V(IN): magnitud=0.56557469, fase=-55.557792 grados, dB=-4.9502007     |
|       23566.541 | PASS   | V(OUT)/V(IN): magnitud=0.56142529, fase=-55.845576 grados, dB=-5.0141605     |
|       23817.143 | PASS   | V(OUT)/V(IN): magnitud=0.55732298, fase=-56.129135 grados, dB=-5.077861      |
|       24067.744 | PASS   | V(OUT)/V(IN): magnitud=0.5532673, fase=-56.408546 grados, dB=-5.1412999      |
|       24318.346 | PASS   | V(OUT)/V(IN): magnitud=0.5492578, fase=-56.68389 grados, dB=-5.2044753       |
|       24568.947 | PASS   | V(OUT)/V(IN): magnitud=0.54529403, fase=-56.955241 grados, dB=-5.2673852     |
|       24819.549 | PASS   | V(OUT)/V(IN): magnitud=0.5413755, fase=-57.222676 grados, dB=-5.330028       |
|        25070.15 | PASS   | V(OUT)/V(IN): magnitud=0.53750175, fase=-57.486267 grados, dB=-5.3924024     |
|       25320.752 | PASS   | V(OUT)/V(IN): magnitud=0.53367229, fase=-57.746086 grados, dB=-5.454507      |
|       25571.353 | PASS   | V(OUT)/V(IN): magnitud=0.52988663, fase=-58.002205 grados, dB=-5.5163407     |
|       25821.955 | PASS   | V(OUT)/V(IN): magnitud=0.5261443, fase=-58.254691 grados, dB=-5.5779027      |
|       26072.556 | PASS   | V(OUT)/V(IN): magnitud=0.52244479, fase=-58.503613 grados, dB=-5.639192      |
|       26323.158 | PASS   | V(OUT)/V(IN): magnitud=0.51878762, fase=-58.749038 grados, dB=-5.700208      |
|       26573.759 | PASS   | V(OUT)/V(IN): magnitud=0.51517228, fase=-58.991029 grados, dB=-5.7609502     |
|       26824.361 | PASS   | V(OUT)/V(IN): magnitud=0.51159829, fase=-59.22965 grados, dB=-5.8214183      |
|       27074.962 | PASS   | V(OUT)/V(IN): magnitud=0.50806514, fase=-59.464964 grados, dB=-5.881612      |
|       27325.564 | PASS   | V(OUT)/V(IN): magnitud=0.50457235, fase=-59.697032 grados, dB=-5.9415311     |
|       27576.165 | PASS   | V(OUT)/V(IN): magnitud=0.50111941, fase=-59.925913 grados, dB=-6.0011755     |
|       27826.767 | PASS   | V(OUT)/V(IN): magnitud=0.49770583, fase=-60.151665 grados, dB=-6.0605454     |
|       28077.368 | PASS   | V(OUT)/V(IN): magnitud=0.49433112, fase=-60.374347 grados, dB=-6.1196409     |
|        28327.97 | PASS   | V(OUT)/V(IN): magnitud=0.49099479, fase=-60.594013 grados, dB=-6.1784623     |
|       28578.571 | PASS   | V(OUT)/V(IN): magnitud=0.48769635, fase=-60.810718 grados, dB=-6.2370099     |
|       28829.173 | PASS   | V(OUT)/V(IN): magnitud=0.48443532, fase=-61.024517 grados, dB=-6.295284      |
|       29079.774 | PASS   | V(OUT)/V(IN): magnitud=0.48121121, fase=-61.235462 grados, dB=-6.3532853     |
|       29330.376 | PASS   | V(OUT)/V(IN): magnitud=0.47802354, fase=-61.443604 grados, dB=-6.4110143     |
|       29580.977 | PASS   | V(OUT)/V(IN): magnitud=0.47487184, fase=-61.648994 grados, dB=-6.4684717     |
|       29831.579 | PASS   | V(OUT)/V(IN): magnitud=0.47175563, fase=-61.851681 grados, dB=-6.5256581     |
|        30082.18 | PASS   | V(OUT)/V(IN): magnitud=0.46867446, fase=-62.051713 grados, dB=-6.5825743     |
|       30332.782 | PASS   | V(OUT)/V(IN): magnitud=0.46562784, fase=-62.249138 grados, dB=-6.6392212     |
|       30583.383 | PASS   | V(OUT)/V(IN): magnitud=0.46261533, fase=-62.444001 grados, dB=-6.6955996     |
|       30833.985 | PASS   | V(OUT)/V(IN): magnitud=0.45963646, fase=-62.636348 grados, dB=-6.7517105     |
|       31084.586 | PASS   | V(OUT)/V(IN): magnitud=0.45669079, fase=-62.826224 grados, dB=-6.8075549     |
|       31335.188 | PASS   | V(OUT)/V(IN): magnitud=0.45377787, fase=-63.013672 grados, dB=-6.8631337     |
|       31585.789 | PASS   | V(OUT)/V(IN): magnitud=0.45089726, fase=-63.198734 grados, dB=-6.9184481     |
|       31836.391 | PASS   | V(OUT)/V(IN): magnitud=0.44804851, fase=-63.381453 grados, dB=-6.9734992     |
|       32086.992 | PASS   | V(OUT)/V(IN): magnitud=0.4452312, fase=-63.561868 grados, dB=-7.0282881      |
|       32337.594 | PASS   | V(OUT)/V(IN): magnitud=0.44244491, fase=-63.74002 grados, dB=-7.082816       |
|       32588.195 | PASS   | V(OUT)/V(IN): magnitud=0.4396892, fase=-63.915948 grados, dB=-7.1370841      |
|       32838.797 | PASS   | V(OUT)/V(IN): magnitud=0.43696366, fase=-64.08969 grados, dB=-7.1910937      |
|       33089.398 | PASS   | V(OUT)/V(IN): magnitud=0.43426787, fase=-64.261283 grados, dB=-7.2448459     |
|           33340 | PASS   | V(OUT)/V(IN): magnitud=0.43160144, fase=-64.430765 grados, dB=-7.2983422     |
|       33590.602 | PASS   | V(OUT)/V(IN): magnitud=0.42896396, fase=-64.598171 grados, dB=-7.3515838     |
|       33841.203 | PASS   | V(OUT)/V(IN): magnitud=0.42635503, fase=-64.763537 grados, dB=-7.4045721     |
|       34091.805 | PASS   | V(OUT)/V(IN): magnitud=0.42377426, fase=-64.926897 grados, dB=-7.4573084     |
|       34342.406 | PASS   | V(OUT)/V(IN): magnitud=0.42122127, fase=-65.088285 grados, dB=-7.5097942     |
|       34593.008 | PASS   | V(OUT)/V(IN): magnitud=0.41869567, fase=-65.247733 grados, dB=-7.5620307     |
|       34843.609 | PASS   | V(OUT)/V(IN): magnitud=0.41619708, fase=-65.405275 grados, dB=-7.6140194     |
|       35094.211 | PASS   | V(OUT)/V(IN): magnitud=0.41372514, fase=-65.560942 grados, dB=-7.6657618     |
|       35344.812 | PASS   | V(OUT)/V(IN): magnitud=0.41127948, fase=-65.714765 grados, dB=-7.7172592     |
|       35595.414 | PASS   | V(OUT)/V(IN): magnitud=0.40885973, fase=-65.866775 grados, dB=-7.7685132     |
|       35846.015 | PASS   | V(OUT)/V(IN): magnitud=0.40646555, fase=-66.017001 grados, dB=-7.8195251     |
|       36096.617 | PASS   | V(OUT)/V(IN): magnitud=0.40409658, fase=-66.165473 grados, dB=-7.8702965     |
|       36347.218 | PASS   | V(OUT)/V(IN): magnitud=0.40175248, fase=-66.31222 grados, dB=-7.9208287      |
|        36597.82 | PASS   | V(OUT)/V(IN): magnitud=0.3994329, fase=-66.457269 grados, dB=-7.9711234      |
|       36848.421 | PASS   | V(OUT)/V(IN): magnitud=0.39713751, fase=-66.600648 grados, dB=-8.0211819     |
|       37099.023 | PASS   | V(OUT)/V(IN): magnitud=0.39486597, fase=-66.742385 grados, dB=-8.0710058     |
|       37349.624 | PASS   | V(OUT)/V(IN): magnitud=0.39261797, fase=-66.882505 grados, dB=-8.1205966     |
|       37600.226 | PASS   | V(OUT)/V(IN): magnitud=0.39039318, fase=-67.021034 grados, dB=-8.1699556     |
|       37850.827 | PASS   | V(OUT)/V(IN): magnitud=0.38819128, fase=-67.157998 grados, dB=-8.2190846     |
|       38101.429 | PASS   | V(OUT)/V(IN): magnitud=0.38601196, fase=-67.293422 grados, dB=-8.2679848     |
|        38352.03 | PASS   | V(OUT)/V(IN): magnitud=0.38385491, fase=-67.42733 grados, dB=-8.316658       |
|       38602.632 | PASS   | V(OUT)/V(IN): magnitud=0.38171984, fase=-67.559746 grados, dB=-8.3651054     |
|       38853.233 | PASS   | V(OUT)/V(IN): magnitud=0.37960643, fase=-67.690694 grados, dB=-8.4133287     |
|       39103.835 | PASS   | V(OUT)/V(IN): magnitud=0.37751441, fase=-67.820196 grados, dB=-8.4613293     |
|       39354.436 | PASS   | V(OUT)/V(IN): magnitud=0.37544347, fase=-67.948275 grados, dB=-8.5091088     |
|       39605.038 | PASS   | V(OUT)/V(IN): magnitud=0.37339334, fase=-68.074954 grados, dB=-8.5566686     |
|       39855.639 | PASS   | V(OUT)/V(IN): magnitud=0.37136374, fase=-68.200253 grados, dB=-8.6040101     |
|       40106.241 | PASS   | V(OUT)/V(IN): magnitud=0.36935438, fase=-68.324195 grados, dB=-8.651135      |
|       40356.842 | PASS   | V(OUT)/V(IN): magnitud=0.36736499, fase=-68.446799 grados, dB=-8.6980447     |
|       40607.444 | PASS   | V(OUT)/V(IN): magnitud=0.36539531, fase=-68.568087 grados, dB=-8.7447406     |
|       40858.045 | PASS   | V(OUT)/V(IN): magnitud=0.36344508, fase=-68.688079 grados, dB=-8.7912242     |
|       41108.647 | PASS   | V(OUT)/V(IN): magnitud=0.36151402, fase=-68.806794 grados, dB=-8.837497      |
|       41359.248 | PASS   | V(OUT)/V(IN): magnitud=0.3596019, fase=-68.924251 grados, dB=-8.8835605      |
|        41609.85 | PASS   | V(OUT)/V(IN): magnitud=0.35770845, fase=-69.04047 grados, dB=-8.9294161      |
|       41860.451 | PASS   | V(OUT)/V(IN): magnitud=0.35583342, fase=-69.155468 grados, dB=-8.9750653     |
|       42111.053 | PASS   | V(OUT)/V(IN): magnitud=0.35397658, fase=-69.269266 grados, dB=-9.0205094     |
|       42361.654 | PASS   | V(OUT)/V(IN): magnitud=0.35213768, fase=-69.381879 grados, dB=-9.06575       |
|       42612.256 | PASS   | V(OUT)/V(IN): magnitud=0.35031649, fase=-69.493326 grados, dB=-9.1107885     |
|       42862.857 | PASS   | V(OUT)/V(IN): magnitud=0.34851276, fase=-69.603624 grados, dB=-9.1556262     |
|       43113.459 | PASS   | V(OUT)/V(IN): magnitud=0.34672628, fase=-69.71279 grados, dB=-9.2002647      |
|        43364.06 | PASS   | V(OUT)/V(IN): magnitud=0.34495682, fase=-69.82084 grados, dB=-9.2447053      |
|       43614.662 | PASS   | V(OUT)/V(IN): magnitud=0.34320415, fase=-69.927791 grados, dB=-9.2889494     |
|       43865.263 | PASS   | V(OUT)/V(IN): magnitud=0.34146805, fase=-70.033659 grados, dB=-9.3329984     |
|       44115.865 | PASS   | V(OUT)/V(IN): magnitud=0.33974832, fase=-70.138459 grados, dB=-9.3768537     |
|       44366.466 | PASS   | V(OUT)/V(IN): magnitud=0.33804473, fase=-70.242207 grados, dB=-9.4205167     |
|       44617.068 | PASS   | V(OUT)/V(IN): magnitud=0.33635708, fase=-70.344918 grados, dB=-9.4639887     |
|       44867.669 | PASS   | V(OUT)/V(IN): magnitud=0.33468515, fase=-70.446607 grados, dB=-9.507271      |
|       45118.271 | PASS   | V(OUT)/V(IN): magnitud=0.33302876, fase=-70.547288 grados, dB=-9.5503652     |
|       45368.872 | PASS   | V(OUT)/V(IN): magnitud=0.3313877, fase=-70.646975 grados, dB=-9.5932724      |
|       45619.474 | PASS   | V(OUT)/V(IN): magnitud=0.32976177, fase=-70.745684 grados, dB=-9.635994      |
|       45870.075 | PASS   | V(OUT)/V(IN): magnitud=0.32815077, fase=-70.843427 grados, dB=-9.6785314     |
|       46120.677 | PASS   | V(OUT)/V(IN): magnitud=0.32655453, fase=-70.940218 grados, dB=-9.7208858     |
|       46371.278 | PASS   | V(OUT)/V(IN): magnitud=0.32497284, fase=-71.03607 grados, dB=-9.7630586      |
|        46621.88 | PASS   | V(OUT)/V(IN): magnitud=0.32340554, fase=-71.130997 grados, dB=-9.805051      |
|       46872.481 | PASS   | V(OUT)/V(IN): magnitud=0.32185242, fase=-71.225011 grados, dB=-9.8468643     |
|       47123.083 | PASS   | V(OUT)/V(IN): magnitud=0.32031332, fase=-71.318126 grados, dB=-9.8884999     |
|       47373.684 | PASS   | V(OUT)/V(IN): magnitud=0.31878806, fase=-71.410352 grados, dB=-9.929959      |
|       47624.286 | PASS   | V(OUT)/V(IN): magnitud=0.31727647, fase=-71.501703 grados, dB=-9.9712428     |
|       47874.887 | PASS   | V(OUT)/V(IN): magnitud=0.31577836, fase=-71.592191 grados, dB=-10.012353     |
|       48125.489 | PASS   | V(OUT)/V(IN): magnitud=0.31429359, fase=-71.681827 grados, dB=-10.05329      |
|        48376.09 | PASS   | V(OUT)/V(IN): magnitud=0.31282197, fase=-71.770622 grados, dB=-10.094055     |
|       48626.692 | PASS   | V(OUT)/V(IN): magnitud=0.31136334, fase=-71.858589 grados, dB=-10.13465      |
|       48877.293 | PASS   | V(OUT)/V(IN): magnitud=0.30991756, fase=-71.945738 grados, dB=-10.175076     |
|       49127.895 | PASS   | V(OUT)/V(IN): magnitud=0.30848444, fase=-72.03208 grados, dB=-10.215335      |
|       49378.496 | PASS   | V(OUT)/V(IN): magnitud=0.30706385, fase=-72.117627 grados, dB=-10.255426     |
|       49629.098 | PASS   | V(OUT)/V(IN): magnitud=0.30565563, fase=-72.202388 grados, dB=-10.295352     |
|       49879.699 | PASS   | V(OUT)/V(IN): magnitud=0.30425962, fase=-72.286374 grados, dB=-10.335114     |
|       50130.301 | PASS   | V(OUT)/V(IN): magnitud=0.30287568, fase=-72.369595 grados, dB=-10.374712     |
|       50380.902 | PASS   | V(OUT)/V(IN): magnitud=0.30150365, fase=-72.452062 grados, dB=-10.414148     |
|       50631.504 | PASS   | V(OUT)/V(IN): magnitud=0.3001434, fase=-72.533784 grados, dB=-10.453424      |
|       50882.105 | PASS   | V(OUT)/V(IN): magnitud=0.29879478, fase=-72.614771 grados, dB=-10.49254      |
|       51132.707 | PASS   | V(OUT)/V(IN): magnitud=0.29745766, fase=-72.695032 grados, dB=-10.531497     |
|       51383.308 | PASS   | V(OUT)/V(IN): magnitud=0.29613189, fase=-72.774577 grados, dB=-10.570297     |
|        51633.91 | PASS   | V(OUT)/V(IN): magnitud=0.29481733, fase=-72.853416 grados, dB=-10.60894      |
|       51884.511 | PASS   | V(OUT)/V(IN): magnitud=0.29351386, fase=-72.931557 grados, dB=-10.647428     |
|       52135.113 | PASS   | V(OUT)/V(IN): magnitud=0.29222133, fase=-73.009009 grados, dB=-10.685762     |
|       52385.714 | PASS   | V(OUT)/V(IN): magnitud=0.29093963, fase=-73.085781 grados, dB=-10.723942     |
|       52636.316 | PASS   | V(OUT)/V(IN): magnitud=0.28966862, fase=-73.161882 grados, dB=-10.761971     |
|       52886.917 | PASS   | V(OUT)/V(IN): magnitud=0.28840818, fase=-73.23732 grados, dB=-10.799849      |
|       53137.519 | PASS   | V(OUT)/V(IN): magnitud=0.28715817, fase=-73.312104 grados, dB=-10.837576     |
|        53388.12 | PASS   | V(OUT)/V(IN): magnitud=0.28591849, fase=-73.386241 grados, dB=-10.875155     |
|       53638.722 | PASS   | V(OUT)/V(IN): magnitud=0.284689, fase=-73.45974 grados, dB=-10.912586        |
|       53889.323 | PASS   | V(OUT)/V(IN): magnitud=0.28346959, fase=-73.53261 grados, dB=-10.94987       |
|       54139.925 | PASS   | V(OUT)/V(IN): magnitud=0.28226014, fase=-73.604856 grados, dB=-10.987009     |
|       54390.526 | PASS   | V(OUT)/V(IN): magnitud=0.28106054, fase=-73.676489 grados, dB=-11.024002     |
|       54641.128 | PASS   | V(OUT)/V(IN): magnitud=0.27987067, fase=-73.747514 grados, dB=-11.060852     |
|       54891.729 | PASS   | V(OUT)/V(IN): magnitud=0.27869041, fase=-73.81794 grados, dB=-11.097559      |
|       55142.331 | PASS   | V(OUT)/V(IN): magnitud=0.27751967, fase=-73.887774 grados, dB=-11.134125     |
|       55392.932 | PASS   | V(OUT)/V(IN): magnitud=0.27635832, fase=-73.957023 grados, dB=-11.170549     |
|       55643.534 | PASS   | V(OUT)/V(IN): magnitud=0.27520626, fase=-74.025694 grados, dB=-11.206834     |
|       55894.135 | PASS   | V(OUT)/V(IN): magnitud=0.27406339, fase=-74.093794 grados, dB=-11.24298      |
|       56144.737 | PASS   | V(OUT)/V(IN): magnitud=0.2729296, fase=-74.161331 grados, dB=-11.278987      |
|       56395.338 | PASS   | V(OUT)/V(IN): magnitud=0.27180478, fase=-74.22831 grados, dB=-11.314858      |
|        56645.94 | PASS   | V(OUT)/V(IN): magnitud=0.27068884, fase=-74.294739 grados, dB=-11.350593     |
|       56896.541 | PASS   | V(OUT)/V(IN): magnitud=0.26958168, fase=-74.360624 grados, dB=-11.386193     |
|       57147.143 | PASS   | V(OUT)/V(IN): magnitud=0.26848319, fase=-74.425972 grados, dB=-11.421658     |
|       57397.744 | PASS   | V(OUT)/V(IN): magnitud=0.26739329, fase=-74.490789 grados, dB=-11.45699      |
|       57648.346 | PASS   | V(OUT)/V(IN): magnitud=0.26631186, fase=-74.555082 grados, dB=-11.49219      |
|       57898.947 | PASS   | V(OUT)/V(IN): magnitud=0.26523883, fase=-74.618856 grados, dB=-11.527258     |
|       58149.549 | PASS   | V(OUT)/V(IN): magnitud=0.26417409, fase=-74.682117 grados, dB=-11.562196     |
|        58400.15 | PASS   | V(OUT)/V(IN): magnitud=0.26311756, fase=-74.744872 grados, dB=-11.597003     |
|       58650.752 | PASS   | V(OUT)/V(IN): magnitud=0.26206914, fase=-74.807127 grados, dB=-11.631682     |
|       58901.353 | PASS   | V(OUT)/V(IN): magnitud=0.26102874, fase=-74.868887 grados, dB=-11.666234     |
|       59151.955 | PASS   | V(OUT)/V(IN): magnitud=0.25999628, fase=-74.930159 grados, dB=-11.700657     |
|       59402.556 | PASS   | V(OUT)/V(IN): magnitud=0.25897167, fase=-74.990947 grados, dB=-11.734955     |
|       59653.158 | PASS   | V(OUT)/V(IN): magnitud=0.25795482, fase=-75.051257 grados, dB=-11.769127     |
|       59903.759 | PASS   | V(OUT)/V(IN): magnitud=0.25694565, fase=-75.111096 grados, dB=-11.803175     |
|       60154.361 | PASS   | V(OUT)/V(IN): magnitud=0.25594407, fase=-75.170467 grados, dB=-11.837099     |
|       60404.962 | PASS   | V(OUT)/V(IN): magnitud=0.25495001, fase=-75.229377 grados, dB=-11.870899     |
|       60655.564 | PASS   | V(OUT)/V(IN): magnitud=0.25396338, fase=-75.287831 grados, dB=-11.904578     |
|       60906.165 | PASS   | V(OUT)/V(IN): magnitud=0.2529841, fase=-75.345833 grados, dB=-11.938135      |
|       61156.767 | PASS   | V(OUT)/V(IN): magnitud=0.2520121, fase=-75.40339 grados, dB=-11.971572       |
|       61407.368 | PASS   | V(OUT)/V(IN): magnitud=0.25104729, fase=-75.460506 grados, dB=-12.004889     |
|        61657.97 | PASS   | V(OUT)/V(IN): magnitud=0.2500896, fase=-75.517186 grados, dB=-12.038087      |
|       61908.571 | PASS   | V(OUT)/V(IN): magnitud=0.24913895, fase=-75.573434 grados, dB=-12.071167     |
|       62159.173 | PASS   | V(OUT)/V(IN): magnitud=0.24819527, fase=-75.629257 grados, dB=-12.10413      |
|       62409.774 | PASS   | V(OUT)/V(IN): magnitud=0.24725849, fase=-75.684657 grados, dB=-12.136976     |
|       62660.376 | PASS   | V(OUT)/V(IN): magnitud=0.24632853, fase=-75.739641 grados, dB=-12.169706     |
|       62910.977 | PASS   | V(OUT)/V(IN): magnitud=0.24540532, fase=-75.794212 grados, dB=-12.202321     |
|       63161.579 | PASS   | V(OUT)/V(IN): magnitud=0.24448879, fase=-75.848375 grados, dB=-12.234821     |
|        63412.18 | PASS   | V(OUT)/V(IN): magnitud=0.24357886, fase=-75.902135 grados, dB=-12.267208     |
|       63662.782 | PASS   | V(OUT)/V(IN): magnitud=0.24267548, fase=-75.955496 grados, dB=-12.299482     |
|       63913.383 | PASS   | V(OUT)/V(IN): magnitud=0.24177858, fase=-76.008463 grados, dB=-12.331644     |
|       64163.985 | PASS   | V(OUT)/V(IN): magnitud=0.24088808, fase=-76.061039 grados, dB=-12.363694     |
|       64414.586 | PASS   | V(OUT)/V(IN): magnitud=0.24000391, fase=-76.113229 grados, dB=-12.395634     |
|       64665.188 | PASS   | V(OUT)/V(IN): magnitud=0.23912603, fase=-76.165036 grados, dB=-12.427463     |
|       64915.789 | PASS   | V(OUT)/V(IN): magnitud=0.23825435, fase=-76.216466 grados, dB=-12.459183     |
|       65166.391 | PASS   | V(OUT)/V(IN): magnitud=0.23738882, fase=-76.267522 grados, dB=-12.490795     |
|       65416.992 | PASS   | V(OUT)/V(IN): magnitud=0.23652938, fase=-76.318209 grados, dB=-12.522298     |
|       65667.594 | PASS   | V(OUT)/V(IN): magnitud=0.23567595, fase=-76.368529 grados, dB=-12.553695     |
|       65918.195 | PASS   | V(OUT)/V(IN): magnitud=0.23482849, fase=-76.418487 grados, dB=-12.584984     |
|       66168.797 | PASS   | V(OUT)/V(IN): magnitud=0.23398693, fase=-76.468087 grados, dB=-12.616168     |
|       66419.398 | PASS   | V(OUT)/V(IN): magnitud=0.23315121, fase=-76.517332 grados, dB=-12.647247     |
|           66670 | PASS   | V(OUT)/V(IN): magnitud=0.23232127, fase=-76.566227 grados, dB=-12.678221     |
|       66920.602 | PASS   | V(OUT)/V(IN): magnitud=0.23149705, fase=-76.614774 grados, dB=-12.709091     |
|       67171.203 | PASS   | V(OUT)/V(IN): magnitud=0.23067851, fase=-76.662979 grados, dB=-12.739857     |
|       67421.805 | PASS   | V(OUT)/V(IN): magnitud=0.22986557, fase=-76.710843 grados, dB=-12.770522     |
|       67672.406 | PASS   | V(OUT)/V(IN): magnitud=0.22905819, fase=-76.75837 grados, dB=-12.801084      |
|       67923.008 | PASS   | V(OUT)/V(IN): magnitud=0.2282563, fase=-76.805565 grados, dB=-12.831544      |
|       68173.609 | PASS   | V(OUT)/V(IN): magnitud=0.22745987, fase=-76.85243 grados, dB=-12.861904      |
|       68424.211 | PASS   | V(OUT)/V(IN): magnitud=0.22666882, fase=-76.89897 grados, dB=-12.892164      |
|       68674.812 | PASS   | V(OUT)/V(IN): magnitud=0.22588312, fase=-76.945186 grados, dB=-12.922325     |
|       68925.414 | PASS   | V(OUT)/V(IN): magnitud=0.2251027, fase=-76.991083 grados, dB=-12.952386      |
|       69176.015 | PASS   | V(OUT)/V(IN): magnitud=0.22432751, fase=-77.036663 grados, dB=-12.982349     |
|       69426.617 | PASS   | V(OUT)/V(IN): magnitud=0.22355751, fase=-77.081931 grados, dB=-13.012215     |
|       69677.218 | PASS   | V(OUT)/V(IN): magnitud=0.22279264, fase=-77.126889 grados, dB=-13.041983     |
|        69927.82 | PASS   | V(OUT)/V(IN): magnitud=0.22203285, fase=-77.17154 grados, dB=-13.071655      |
|       70178.421 | PASS   | V(OUT)/V(IN): magnitud=0.2212781, fase=-77.215887 grados, dB=-13.101231      |
|       70429.023 | PASS   | V(OUT)/V(IN): magnitud=0.22052834, fase=-77.259933 grados, dB=-13.130712     |
|       70679.624 | PASS   | V(OUT)/V(IN): magnitud=0.21978351, fase=-77.303682 grados, dB=-13.160098     |
|       70930.226 | PASS   | V(OUT)/V(IN): magnitud=0.21904357, fase=-77.347136 grados, dB=-13.18939      |
|       71180.827 | PASS   | V(OUT)/V(IN): magnitud=0.21830848, fase=-77.390299 grados, dB=-13.218588     |
|       71431.429 | PASS   | V(OUT)/V(IN): magnitud=0.21757819, fase=-77.433172 grados, dB=-13.247693     |
|        71682.03 | PASS   | V(OUT)/V(IN): magnitud=0.21685264, fase=-77.475759 grados, dB=-13.276706     |
|       71932.632 | PASS   | V(OUT)/V(IN): magnitud=0.21613181, fase=-77.518064 grados, dB=-13.305626     |
|       72183.233 | PASS   | V(OUT)/V(IN): magnitud=0.21541563, fase=-77.560087 grados, dB=-13.334456     |
|       72433.835 | PASS   | V(OUT)/V(IN): magnitud=0.21470408, fase=-77.601833 grados, dB=-13.363194     |
|       72684.436 | PASS   | V(OUT)/V(IN): magnitud=0.2139971, fase=-77.643304 grados, dB=-13.391842      |
|       72935.038 | PASS   | V(OUT)/V(IN): magnitud=0.21329465, fase=-77.684503 grados, dB=-13.420401     |
|       73185.639 | PASS   | V(OUT)/V(IN): magnitud=0.21259669, fase=-77.725431 grados, dB=-13.44887      |
|       73436.241 | PASS   | V(OUT)/V(IN): magnitud=0.21190318, fase=-77.766093 grados, dB=-13.47725      |
|       73686.842 | PASS   | V(OUT)/V(IN): magnitud=0.21121408, fase=-77.80649 grados, dB=-13.505543      |
|       73937.444 | PASS   | V(OUT)/V(IN): magnitud=0.21052934, fase=-77.846625 grados, dB=-13.533747     |
|       74188.045 | PASS   | V(OUT)/V(IN): magnitud=0.20984893, fase=-77.886501 grados, dB=-13.561865     |
|       74438.647 | PASS   | V(OUT)/V(IN): magnitud=0.20917281, fase=-77.926119 grados, dB=-13.589896     |
|       74689.248 | PASS   | V(OUT)/V(IN): magnitud=0.20850093, fase=-77.965483 grados, dB=-13.61784      |
|        74939.85 | PASS   | V(OUT)/V(IN): magnitud=0.20783325, fase=-78.004594 grados, dB=-13.645699     |
|       75190.451 | PASS   | V(OUT)/V(IN): magnitud=0.20716975, fase=-78.043456 grados, dB=-13.673473     |
|       75441.053 | PASS   | V(OUT)/V(IN): magnitud=0.20651038, fase=-78.082071 grados, dB=-13.701162     |
|       75691.654 | PASS   | V(OUT)/V(IN): magnitud=0.2058551, fase=-78.12044 grados, dB=-13.728767       |
|       75942.256 | PASS   | V(OUT)/V(IN): magnitud=0.20520388, fase=-78.158566 grados, dB=-13.756289     |
|       76192.857 | PASS   | V(OUT)/V(IN): magnitud=0.20455667, fase=-78.196452 grados, dB=-13.783727     |
|       76443.459 | PASS   | V(OUT)/V(IN): magnitud=0.20391345, fase=-78.234099 grados, dB=-13.811083     |
|        76694.06 | PASS   | V(OUT)/V(IN): magnitud=0.20327418, fase=-78.27151 grados, dB=-13.838356      |
|       76944.662 | PASS   | V(OUT)/V(IN): magnitud=0.20263882, fase=-78.308688 grados, dB=-13.865547     |
|       77195.263 | PASS   | V(OUT)/V(IN): magnitud=0.20200733, fase=-78.345633 grados, dB=-13.892657     |
|       77445.865 | PASS   | V(OUT)/V(IN): magnitud=0.20137969, fase=-78.382349 grados, dB=-13.919687     |
|       77696.466 | PASS   | V(OUT)/V(IN): magnitud=0.20075586, fase=-78.418837 grados, dB=-13.946636     |
|       77947.068 | PASS   | V(OUT)/V(IN): magnitud=0.2001358, fase=-78.4551 grados, dB=-13.973505        |
|       78197.669 | PASS   | V(OUT)/V(IN): magnitud=0.19951948, fase=-78.491139 grados, dB=-14.000294     |
|       78448.271 | PASS   | V(OUT)/V(IN): magnitud=0.19890687, fase=-78.526957 grados, dB=-14.027004     |
|       78698.872 | PASS   | V(OUT)/V(IN): magnitud=0.19829793, fase=-78.562556 grados, dB=-14.053636     |
|       78949.474 | PASS   | V(OUT)/V(IN): magnitud=0.19769264, fase=-78.597937 grados, dB=-14.08019      |
|       79200.075 | PASS   | V(OUT)/V(IN): magnitud=0.19709096, fase=-78.633103 grados, dB=-14.106666     |
|       79450.677 | PASS   | V(OUT)/V(IN): magnitud=0.19649286, fase=-78.668055 grados, dB=-14.133065     |
|       79701.278 | PASS   | V(OUT)/V(IN): magnitud=0.1958983, fase=-78.702795 grados, dB=-14.159387      |
|        79951.88 | PASS   | V(OUT)/V(IN): magnitud=0.19530727, fase=-78.737326 grados, dB=-14.185632     |
|       80202.481 | PASS   | V(OUT)/V(IN): magnitud=0.19471972, fase=-78.771649 grados, dB=-14.211801     |
|       80453.083 | PASS   | V(OUT)/V(IN): magnitud=0.19413563, fase=-78.805766 grados, dB=-14.237895     |
|       80703.684 | PASS   | V(OUT)/V(IN): magnitud=0.19355496, fase=-78.839679 grados, dB=-14.263914     |
|       80954.286 | PASS   | V(OUT)/V(IN): magnitud=0.19297769, fase=-78.87339 grados, dB=-14.289858      |
|       81204.887 | PASS   | V(OUT)/V(IN): magnitud=0.19240379, fase=-78.9069 grados, dB=-14.315727       |
|       81455.489 | PASS   | V(OUT)/V(IN): magnitud=0.19183323, fase=-78.940211 grados, dB=-14.341523     |
|        81706.09 | PASS   | V(OUT)/V(IN): magnitud=0.19126599, fase=-78.973325 grados, dB=-14.367245     |
|       81956.692 | PASS   | V(OUT)/V(IN): magnitud=0.19070202, fase=-79.006244 grados, dB=-14.392894     |
|       82207.293 | PASS   | V(OUT)/V(IN): magnitud=0.19014131, fase=-79.038969 grados, dB=-14.41847      |
|       82457.895 | PASS   | V(OUT)/V(IN): magnitud=0.18958383, fase=-79.071502 grados, dB=-14.443974     |
|       82708.496 | PASS   | V(OUT)/V(IN): magnitud=0.18902955, fase=-79.103845 grados, dB=-14.469406     |
|       82959.098 | PASS   | V(OUT)/V(IN): magnitud=0.18847844, fase=-79.135999 grados, dB=-14.494767     |
|       83209.699 | PASS   | V(OUT)/V(IN): magnitud=0.18793047, fase=-79.167966 grados, dB=-14.520056     |
|       83460.301 | PASS   | V(OUT)/V(IN): magnitud=0.18738563, fase=-79.199748 grados, dB=-14.545274     |
|       83710.902 | PASS   | V(OUT)/V(IN): magnitud=0.18684388, fase=-79.231346 grados, dB=-14.570422     |
|       83961.504 | PASS   | V(OUT)/V(IN): magnitud=0.18630521, fase=-79.262762 grados, dB=-14.5955       |
|       84212.105 | PASS   | V(OUT)/V(IN): magnitud=0.18576957, fase=-79.293997 grados, dB=-14.620509     |
|       84462.707 | PASS   | V(OUT)/V(IN): magnitud=0.18523695, fase=-79.325053 grados, dB=-14.645448     |
|       84713.308 | PASS   | V(OUT)/V(IN): magnitud=0.18470732, fase=-79.355931 grados, dB=-14.670318     |
|        84963.91 | PASS   | V(OUT)/V(IN): magnitud=0.18418067, fase=-79.386633 grados, dB=-14.695119     |
|       85214.511 | PASS   | V(OUT)/V(IN): magnitud=0.18365695, fase=-79.41716 grados, dB=-14.719853      |
|       85465.113 | PASS   | V(OUT)/V(IN): magnitud=0.18313616, fase=-79.447514 grados, dB=-14.744518     |
|       85715.714 | PASS   | V(OUT)/V(IN): magnitud=0.18261826, fase=-79.477697 grados, dB=-14.769116     |
|       85966.316 | PASS   | V(OUT)/V(IN): magnitud=0.18210323, fase=-79.507709 grados, dB=-14.793647     |
|       86216.917 | PASS   | V(OUT)/V(IN): magnitud=0.18159105, fase=-79.537552 grados, dB=-14.818111     |
|       86467.519 | PASS   | V(OUT)/V(IN): magnitud=0.1810817, fase=-79.567228 grados, dB=-14.842509      |
|        86718.12 | PASS   | V(OUT)/V(IN): magnitud=0.18057514, fase=-79.596738 grados, dB=-14.866841     |
|       86968.722 | PASS   | V(OUT)/V(IN): magnitud=0.18007137, fase=-79.626083 grados, dB=-14.891106     |
|       87219.323 | PASS   | V(OUT)/V(IN): magnitud=0.17957036, fase=-79.655265 grados, dB=-14.915307     |
|       87469.925 | PASS   | V(OUT)/V(IN): magnitud=0.17907208, fase=-79.684284 grados, dB=-14.939442     |
|       87720.526 | PASS   | V(OUT)/V(IN): magnitud=0.17857651, fase=-79.713143 grados, dB=-14.963513     |
|       87971.128 | PASS   | V(OUT)/V(IN): magnitud=0.17808364, fase=-79.741843 grados, dB=-14.98752      |
|       88221.729 | PASS   | V(OUT)/V(IN): magnitud=0.17759343, fase=-79.770385 grados, dB=-15.011462     |
|       88472.331 | PASS   | V(OUT)/V(IN): magnitud=0.17710588, fase=-79.79877 grados, dB=-15.035341      |
|       88722.932 | PASS   | V(OUT)/V(IN): magnitud=0.17662095, fase=-79.826999 grados, dB=-15.059156     |
|       88973.534 | PASS   | V(OUT)/V(IN): magnitud=0.17613863, fase=-79.855074 grados, dB=-15.082908     |
|       89224.135 | PASS   | V(OUT)/V(IN): magnitud=0.17565889, fase=-79.882996 grados, dB=-15.106597     |
|       89474.737 | PASS   | V(OUT)/V(IN): magnitud=0.17518172, fase=-79.910767 grados, dB=-15.130224     |
|       89725.338 | PASS   | V(OUT)/V(IN): magnitud=0.1747071, fase=-79.938387 grados, dB=-15.153789      |
|        89975.94 | PASS   | V(OUT)/V(IN): magnitud=0.174235, fase=-79.965857 grados, dB=-15.177292       |
|       90226.541 | PASS   | V(OUT)/V(IN): magnitud=0.1737654, fase=-79.99318 grados, dB=-15.200734       |
|       90477.143 | PASS   | V(OUT)/V(IN): magnitud=0.1732983, fase=-80.020355 grados, dB=-15.224114      |
|       90727.744 | PASS   | V(OUT)/V(IN): magnitud=0.17283366, fase=-80.047385 grados, dB=-15.247434     |
|       90978.346 | PASS   | V(OUT)/V(IN): magnitud=0.17237146, fase=-80.07427 grados, dB=-15.270693      |
|       91228.947 | PASS   | V(OUT)/V(IN): magnitud=0.1719117, fase=-80.101012 grados, dB=-15.293891      |
|       91479.549 | PASS   | V(OUT)/V(IN): magnitud=0.17145435, fase=-80.127611 grados, dB=-15.31703      |
|        91730.15 | PASS   | V(OUT)/V(IN): magnitud=0.17099938, fase=-80.15407 grados, dB=-15.340109      |
|       91980.752 | PASS   | V(OUT)/V(IN): magnitud=0.17054679, fase=-80.180388 grados, dB=-15.363129     |
|       92231.353 | PASS   | V(OUT)/V(IN): magnitud=0.17009656, fase=-80.206567 grados, dB=-15.38609      |
|       92481.955 | PASS   | V(OUT)/V(IN): magnitud=0.16964866, fase=-80.232608 grados, dB=-15.408991     |
|       92732.556 | PASS   | V(OUT)/V(IN): magnitud=0.16920308, fase=-80.258512 grados, dB=-15.431835     |
|       92983.158 | PASS   | V(OUT)/V(IN): magnitud=0.1687598, fase=-80.284281 grados, dB=-15.45462       |
|       93233.759 | PASS   | V(OUT)/V(IN): magnitud=0.1683188, fase=-80.309915 grados, dB=-15.477347      |
|       93484.361 | PASS   | V(OUT)/V(IN): magnitud=0.16788007, fase=-80.335415 grados, dB=-15.500017     |
|       93734.962 | PASS   | V(OUT)/V(IN): magnitud=0.16744359, fase=-80.360783 grados, dB=-15.522629     |
|       93985.564 | PASS   | V(OUT)/V(IN): magnitud=0.16700934, fase=-80.386019 grados, dB=-15.545185     |
|       94236.165 | PASS   | V(OUT)/V(IN): magnitud=0.16657731, fase=-80.411124 grados, dB=-15.567683     |
|       94486.767 | PASS   | V(OUT)/V(IN): magnitud=0.16614747, fase=-80.4361 grados, dB=-15.590125       |
|       94737.368 | PASS   | V(OUT)/V(IN): magnitud=0.16571982, fase=-80.460947 grados, dB=-15.612511     |
|        94987.97 | PASS   | V(OUT)/V(IN): magnitud=0.16529433, fase=-80.485667 grados, dB=-15.634841     |
|       95238.571 | PASS   | V(OUT)/V(IN): magnitud=0.16487099, fase=-80.51026 grados, dB=-15.657115      |
|       95489.173 | PASS   | V(OUT)/V(IN): magnitud=0.16444979, fase=-80.534727 grados, dB=-15.679334     |
|       95739.774 | PASS   | V(OUT)/V(IN): magnitud=0.1640307, fase=-80.559069 grados, dB=-15.701497      |
|       95990.376 | PASS   | V(OUT)/V(IN): magnitud=0.16361372, fase=-80.583288 grados, dB=-15.723606     |
|       96240.977 | PASS   | V(OUT)/V(IN): magnitud=0.16319882, fase=-80.607384 grados, dB=-15.74566      |
|       96491.579 | PASS   | V(OUT)/V(IN): magnitud=0.16278599, fase=-80.631358 grados, dB=-15.767659     |
|        96742.18 | PASS   | V(OUT)/V(IN): magnitud=0.16237522, fase=-80.655211 grados, dB=-15.789605     |
|       96992.782 | PASS   | V(OUT)/V(IN): magnitud=0.16196649, fase=-80.678943 grados, dB=-15.811497     |
|       97243.383 | PASS   | V(OUT)/V(IN): magnitud=0.16155978, fase=-80.702557 grados, dB=-15.833335     |
|       97493.985 | PASS   | V(OUT)/V(IN): magnitud=0.16115508, fase=-80.726052 grados, dB=-15.85512      |
|       97744.586 | PASS   | V(OUT)/V(IN): magnitud=0.16075239, fase=-80.74943 grados, dB=-15.876851      |
|       97995.188 | PASS   | V(OUT)/V(IN): magnitud=0.16035167, fase=-80.772691 grados, dB=-15.89853      |
|       98245.789 | PASS   | V(OUT)/V(IN): magnitud=0.15995292, fase=-80.795837 grados, dB=-15.920157     |
|       98496.391 | PASS   | V(OUT)/V(IN): magnitud=0.15955612, fase=-80.818867 grados, dB=-15.941731     |
|       98746.992 | PASS   | V(OUT)/V(IN): magnitud=0.15916126, fase=-80.841784 grados, dB=-15.963253     |
|       98997.594 | PASS   | V(OUT)/V(IN): magnitud=0.15876833, fase=-80.864587 grados, dB=-15.984723     |
|       99248.195 | PASS   | V(OUT)/V(IN): magnitud=0.1583773, fase=-80.887278 grados, dB=-16.006141      |
|       99498.797 | PASS   | V(OUT)/V(IN): magnitud=0.15798818, fase=-80.909858 grados, dB=-16.027508     |
|       99749.398 | PASS   | V(OUT)/V(IN): magnitud=0.15760094, fase=-80.932327 grados, dB=-16.048824     |
|          100000 | PASS   | V(OUT)/V(IN): magnitud=0.15721556, fase=-80.954686 grados, dB=-16.070089     |

## Validación

**Estado: PASS**

| Métrica               |         Norma |        Umbral | Resultado |
| --------------------- | ------------: | ------------: | --------- |
| linear_residual       | 4.1989977e-18 | 1.7353702e-05 | PASS      |
| full_rank             |               |               | PASS      |
| KCL                   | 1.3657996e-20 | 1.0307218e-10 | PASS      |
| branch_node_voltage   |             0 | 2.8384827e-08 | PASS      |
| constitutive_residual | 3.5090695e-18 | 3.5849593e-08 | PASS      |

Número de condición: `3457402.9`.

## Advertencias y limitaciones

- La entrada original mezclaba IN/in y N1/n1. El parser educativo conserva mayusculas/minusculas; se uso esta copia con los nodos uniformados en mayusculas para mantener la conectividad SPICE pretendida. El netlist fuente del usuario no se modifico.
- La salida se toma en OUT sobre R1; la respuesta calculada presenta una banda resonante, no una respuesta pasa-altas monotona.
- No se proporciono referencia externa compatible; no se ejecuto comparacion contra SPICE.

## Artefactos y reproducibilidad

- `filtro_pasa_altas_rlc.cir`
- `netlist_validation.json`
- `parsed.json`
- `circuit.json`
- `topology.json`
- `graph.png`
- `esquematico_filtro_pasa_altas.png`
- `incidence.json`
- `incidence.md`
- `incidence.npz`
- `tableau_constitutive_10Hz.json`
- `tableau_system_10Hz.json`
- `tableau_solution_10Hz.json`
- `tableau_validation_10Hz.json`
- `tableau_T_10Hz.png`
- `transfers.json`
- `ac_results.json`
- `plots/magnitude.png`
- `plots/magnitude_voltage.png`
- `plots/phase.png`
- `valores_graficados.csv`
- `netlist_validation_final.json`
## Valores completos de las graficas

La magnitud de voltaje se toma del campo `magnitude` del fasor `V(NOUT)` reportado por el solver. La magnitud en dB y la fase se toman de la transferencia `V(OUT)/V(IN)` reportada por `solve_ac_sweep.py`. Los estados se conservan por punto.

| Frecuencia (Hz) | Magnitud (dB) | |V(OUT)| (V) | Fase (grados) | Estado |
|---:|---:|---:|---:|---|
| 10 | -24.053173 | 0.06271066 | 86.404585 | PASS |
| 260.6015 | -1.3137767 | 0.85962921 | 30.725024 | PASS |
| 511.20301 | -0.32602897 | 0.96316025 | 15.600493 | PASS |
| 761.80451 | -0.11121113 | 0.98727796 | 9.1490805 | PASS |
| 1012.406 | -0.037877274 | 0.99564871 | 5.3469257 | PASS |
| 1263.0075 | -0.0094431941 | 0.9989134 | 2.6712297 | PASS |
| 1513.609 | -0.00043831628 | 0.99994954 | 0.57559979 | PASS |
| 1764.2105 | -0.0018489346 | 0.99978716 | -1.1821589 | PASS |
| 2014.812 | -0.0098297324 | 0.99886895 | -2.7253319 | PASS |
| 2265.4135 | -0.02250913 | 0.9974119 | -4.1230845 | PASS |
| 2516.015 | -0.038879659 | 0.99553382 | -5.41711 | PASS |
| 2766.6165 | -0.058352316 | 0.99330446 | -6.6339646 | PASS |
| 3017.218 | -0.080557012 | 0.99076841 | -7.7913127 | PASS |
| 3267.8195 | -0.10524532 | 0.9879563 | -8.9013212 | PASS |
| 3518.4211 | -0.13223975 | 0.98489065 | -9.9726121 | PASS |
| 3769.0226 | -0.16140581 | 0.98158906 | -11.011442 | PASS |
| 4019.6241 | -0.1926359 | 0.9780661 | -12.02244 | PASS |
| 4270.2256 | -0.22583966 | 0.97433436 | -13.009092 | PASS |
| 4520.8271 | -0.26093798 | 0.97040517 | -13.974057 | PASS |
| 4771.4286 | -0.29785931 | 0.966289 | -14.919392 | PASS |
| 5022.0301 | -0.33653716 | 0.96199573 | -15.846705 | PASS |
| 5272.6316 | -0.37690852 | 0.95753482 | -16.757264 | PASS |
| 5523.2331 | -0.41891287 | 0.95291542 | -17.652081 | PASS |
| 5773.8346 | -0.46249142 | 0.94814646 | -18.531969 | PASS |
| 6024.4361 | -0.50758669 | 0.94323665 | -19.397587 | PASS |
| 6275.0376 | -0.55414224 | 0.93819451 | -20.249474 | PASS |
| 6525.6391 | -0.60210247 | 0.93302843 | -21.088077 | PASS |
| 6776.2406 | -0.65141249 | 0.92774661 | -21.913767 | PASS |
| 7026.8421 | -0.70201815 | 0.92235709 | -22.726857 | PASS |
| 7277.4436 | -0.75386593 | 0.91686776 | -23.527618 | PASS |
| 7528.0451 | -0.80690305 | 0.91128631 | -24.31628 | PASS |
| 7778.6466 | -0.86107741 | 0.90562026 | -25.093048 | PASS |
| 8029.2481 | -0.9163377 | 0.89987692 | -25.858106 | PASS |
| 8279.8496 | -0.97263339 | 0.89406343 | -26.611618 | PASS |
| 8530.4511 | -1.0299148 | 0.88818669 | -27.353736 | PASS |
| 8781.0526 | -1.0881332 | 0.8822534 | -28.084604 | PASS |
| 9031.6541 | -1.1472406 | 0.87627005 | -28.804356 | PASS |
| 9282.2556 | -1.2071903 | 0.87024289 | -29.513123 | PASS |
| 9532.8571 | -1.2679365 | 0.86417794 | -30.211031 | PASS |
| 9783.4586 | -1.3294342 | 0.858081 | -30.898204 | PASS |
| 10034.06 | -1.39164 | 0.85195764 | -31.574764 | PASS |
| 10284.662 | -1.4545111 | 0.84581318 | -32.240834 | PASS |
| 10535.263 | -1.5180061 | 0.83965271 | -32.896535 | PASS |
| 10785.865 | -1.5820848 | 0.83348111 | -33.541989 | PASS |
| 11036.466 | -1.646708 | 0.827303 | -34.17732 | PASS |
| 11287.068 | -1.7118378 | 0.8211228 | -34.802651 | PASS |
| 11537.669 | -1.7774374 | 0.81494468 | -35.418107 | PASS |
| 11788.271 | -1.8434712 | 0.80877262 | -36.023815 | PASS |
| 12038.872 | -1.9099049 | 0.80261035 | -36.6199 | PASS |
| 12289.474 | -1.9767052 | 0.79646142 | -37.206491 | PASS |
| 12540.075 | -2.04384 | 0.79032915 | -37.783718 | PASS |
| 12790.677 | -2.1112784 | 0.78421669 | -38.35171 | PASS |
| 13041.278 | -2.1789906 | 0.77812698 | -38.910598 | PASS |
| 13291.88 | -2.2469479 | 0.77206276 | -39.460514 | PASS |
| 13542.481 | -2.3151229 | 0.76602661 | -40.00159 | PASS |
| 13793.083 | -2.383489 | 0.76002093 | -40.533957 | PASS |
| 14043.684 | -2.4520208 | 0.75404794 | -41.05775 | PASS |
| 14294.286 | -2.520694 | 0.74810973 | -41.573099 | PASS |
| 14544.887 | -2.5894851 | 0.74220819 | -42.080139 | PASS |
| 14795.489 | -2.6583719 | 0.73634511 | -42.579002 | PASS |
| 15046.09 | -2.7273329 | 0.73052209 | -43.069819 | PASS |
| 15296.692 | -2.7963476 | 0.72474064 | -43.552723 | PASS |
| 15547.293 | -2.8653966 | 0.71900212 | -44.027845 | PASS |
| 15797.895 | -2.9344611 | 0.71330775 | -44.495315 | PASS |
| 16048.496 | -3.0035234 | 0.70765867 | -44.955264 | PASS |
| 16299.098 | -3.0725664 | 0.70205588 | -45.407819 | PASS |
| 16549.699 | -3.1415741 | 0.69650028 | -45.853109 | PASS |
| 16800.301 | -3.210531 | 0.69099269 | -46.29126 | PASS |
| 17050.902 | -3.2794225 | 0.68553381 | -46.722398 | PASS |
| 17301.504 | -3.3482347 | 0.68012426 | -47.146646 | PASS |
| 17552.105 | -3.4169544 | 0.67476459 | -47.564128 | PASS |
| 17802.707 | -3.4855691 | 0.66945524 | -47.974966 | PASS |
| 18053.308 | -3.5540668 | 0.66419662 | -48.379279 | PASS |
| 18303.91 | -3.6224365 | 0.65898902 | -48.777185 | PASS |
| 18554.511 | -3.6906673 | 0.6538327 | -49.168802 | PASS |
| 18805.113 | -3.7587492 | 0.64872784 | -49.554245 | PASS |
| 19055.714 | -3.8266728 | 0.64367458 | -49.933627 | PASS |
| 19306.316 | -3.894429 | 0.63867299 | -50.307062 | PASS |
| 19556.917 | -3.9620095 | 0.63372308 | -50.674658 | PASS |
| 19807.519 | -4.0294061 | 0.62882485 | -51.036525 | PASS |
| 20058.12 | -4.0966114 | 0.62397822 | -51.392769 | PASS |
| 20308.722 | -4.1636183 | 0.61918308 | -51.743497 | PASS |
| 20559.323 | -4.2304203 | 0.6144393 | -52.08881 | PASS |
| 20809.925 | -4.2970111 | 0.60974668 | -52.428812 | PASS |
| 21060.526 | -4.363385 | 0.60510501 | -52.763601 | PASS |
| 21311.128 | -4.4295364 | 0.60051406 | -53.093276 | PASS |
| 21561.729 | -4.4954603 | 0.59597355 | -53.417934 | PASS |
| 21812.331 | -4.561152 | 0.59148318 | -53.73767 | PASS |
| 22062.932 | -4.626607 | 0.58704264 | -54.052575 | PASS |
| 22313.534 | -4.6918214 | 0.58265158 | -54.362742 | PASS |
| 22564.135 | -4.7567913 | 0.57830964 | -54.668261 | PASS |
| 22814.737 | -4.8215133 | 0.57401645 | -54.969218 | PASS |
| 23065.338 | -4.8859841 | 0.5697716 | -55.2657 | PASS |
| 23315.94 | -4.9502007 | 0.56557469 | -55.557792 | PASS |
| 23566.541 | -5.0141605 | 0.56142529 | -55.845576 | PASS |
| 23817.143 | -5.077861 | 0.55732298 | -56.129135 | PASS |
| 24067.744 | -5.1412999 | 0.5532673 | -56.408546 | PASS |
| 24318.346 | -5.2044753 | 0.5492578 | -56.68389 | PASS |
| 24568.947 | -5.2673852 | 0.54529403 | -56.955241 | PASS |
| 24819.549 | -5.330028 | 0.5413755 | -57.222676 | PASS |
| 25070.15 | -5.3924024 | 0.53750175 | -57.486267 | PASS |
| 25320.752 | -5.454507 | 0.53367229 | -57.746086 | PASS |
| 25571.353 | -5.5163407 | 0.52988663 | -58.002205 | PASS |
| 25821.955 | -5.5779027 | 0.5261443 | -58.254691 | PASS |
| 26072.556 | -5.639192 | 0.52244479 | -58.503613 | PASS |
| 26323.158 | -5.700208 | 0.51878762 | -58.749038 | PASS |
| 26573.759 | -5.7609502 | 0.51517228 | -58.991029 | PASS |
| 26824.361 | -5.8214183 | 0.51159829 | -59.22965 | PASS |
| 27074.962 | -5.881612 | 0.50806514 | -59.464964 | PASS |
| 27325.564 | -5.9415311 | 0.50457235 | -59.697032 | PASS |
| 27576.165 | -6.0011755 | 0.50111941 | -59.925913 | PASS |
| 27826.767 | -6.0605454 | 0.49770583 | -60.151665 | PASS |
| 28077.368 | -6.1196409 | 0.49433112 | -60.374347 | PASS |
| 28327.97 | -6.1784623 | 0.49099479 | -60.594013 | PASS |
| 28578.571 | -6.2370099 | 0.48769635 | -60.810718 | PASS |
| 28829.173 | -6.295284 | 0.48443532 | -61.024517 | PASS |
| 29079.774 | -6.3532853 | 0.48121121 | -61.235462 | PASS |
| 29330.376 | -6.4110143 | 0.47802354 | -61.443604 | PASS |
| 29580.977 | -6.4684717 | 0.47487184 | -61.648994 | PASS |
| 29831.579 | -6.5256581 | 0.47175563 | -61.851681 | PASS |
| 30082.18 | -6.5825743 | 0.46867446 | -62.051713 | PASS |
| 30332.782 | -6.6392212 | 0.46562784 | -62.249138 | PASS |
| 30583.383 | -6.6955996 | 0.46261533 | -62.444001 | PASS |
| 30833.985 | -6.7517105 | 0.45963646 | -62.636348 | PASS |
| 31084.586 | -6.8075549 | 0.45669079 | -62.826224 | PASS |
| 31335.188 | -6.8631337 | 0.45377787 | -63.013672 | PASS |
| 31585.789 | -6.9184481 | 0.45089726 | -63.198734 | PASS |
| 31836.391 | -6.9734992 | 0.44804851 | -63.381453 | PASS |
| 32086.992 | -7.0282881 | 0.4452312 | -63.561868 | PASS |
| 32337.594 | -7.082816 | 0.44244491 | -63.74002 | PASS |
| 32588.195 | -7.1370841 | 0.4396892 | -63.915948 | PASS |
| 32838.797 | -7.1910937 | 0.43696366 | -64.08969 | PASS |
| 33089.398 | -7.2448459 | 0.43426787 | -64.261283 | PASS |
| 33340 | -7.2983422 | 0.43160144 | -64.430765 | PASS |
| 33590.602 | -7.3515838 | 0.42896396 | -64.598171 | PASS |
| 33841.203 | -7.4045721 | 0.42635503 | -64.763537 | PASS |
| 34091.805 | -7.4573084 | 0.42377426 | -64.926897 | PASS |
| 34342.406 | -7.5097942 | 0.42122127 | -65.088285 | PASS |
| 34593.008 | -7.5620307 | 0.41869567 | -65.247733 | PASS |
| 34843.609 | -7.6140194 | 0.41619708 | -65.405275 | PASS |
| 35094.211 | -7.6657618 | 0.41372514 | -65.560942 | PASS |
| 35344.812 | -7.7172592 | 0.41127948 | -65.714765 | PASS |
| 35595.414 | -7.7685132 | 0.40885973 | -65.866775 | PASS |
| 35846.015 | -7.8195251 | 0.40646555 | -66.017001 | PASS |
| 36096.617 | -7.8702965 | 0.40409658 | -66.165473 | PASS |
| 36347.218 | -7.9208287 | 0.40175248 | -66.31222 | PASS |
| 36597.82 | -7.9711234 | 0.3994329 | -66.457269 | PASS |
| 36848.421 | -8.0211819 | 0.39713751 | -66.600648 | PASS |
| 37099.023 | -8.0710058 | 0.39486597 | -66.742385 | PASS |
| 37349.624 | -8.1205966 | 0.39261797 | -66.882505 | PASS |
| 37600.226 | -8.1699556 | 0.39039318 | -67.021034 | PASS |
| 37850.827 | -8.2190846 | 0.38819128 | -67.157998 | PASS |
| 38101.429 | -8.2679848 | 0.38601196 | -67.293422 | PASS |
| 38352.03 | -8.316658 | 0.38385491 | -67.42733 | PASS |
| 38602.632 | -8.3651054 | 0.38171984 | -67.559746 | PASS |
| 38853.233 | -8.4133287 | 0.37960643 | -67.690694 | PASS |
| 39103.835 | -8.4613293 | 0.37751441 | -67.820196 | PASS |
| 39354.436 | -8.5091088 | 0.37544347 | -67.948275 | PASS |
| 39605.038 | -8.5566686 | 0.37339334 | -68.074954 | PASS |
| 39855.639 | -8.6040101 | 0.37136374 | -68.200253 | PASS |
| 40106.241 | -8.651135 | 0.36935438 | -68.324195 | PASS |
| 40356.842 | -8.6980447 | 0.36736499 | -68.446799 | PASS |
| 40607.444 | -8.7447406 | 0.36539531 | -68.568087 | PASS |
| 40858.045 | -8.7912242 | 0.36344508 | -68.688079 | PASS |
| 41108.647 | -8.837497 | 0.36151402 | -68.806794 | PASS |
| 41359.248 | -8.8835605 | 0.3596019 | -68.924251 | PASS |
| 41609.85 | -8.9294161 | 0.35770845 | -69.04047 | PASS |
| 41860.451 | -8.9750653 | 0.35583342 | -69.155468 | PASS |
| 42111.053 | -9.0205094 | 0.35397658 | -69.269266 | PASS |
| 42361.654 | -9.06575 | 0.35213768 | -69.381879 | PASS |
| 42612.256 | -9.1107885 | 0.35031649 | -69.493326 | PASS |
| 42862.857 | -9.1556262 | 0.34851276 | -69.603624 | PASS |
| 43113.459 | -9.2002647 | 0.34672628 | -69.71279 | PASS |
| 43364.06 | -9.2447053 | 0.34495682 | -69.82084 | PASS |
| 43614.662 | -9.2889494 | 0.34320415 | -69.927791 | PASS |
| 43865.263 | -9.3329984 | 0.34146805 | -70.033659 | PASS |
| 44115.865 | -9.3768537 | 0.33974832 | -70.138459 | PASS |
| 44366.466 | -9.4205167 | 0.33804473 | -70.242207 | PASS |
| 44617.068 | -9.4639887 | 0.33635708 | -70.344918 | PASS |
| 44867.669 | -9.507271 | 0.33468515 | -70.446607 | PASS |
| 45118.271 | -9.5503652 | 0.33302876 | -70.547288 | PASS |
| 45368.872 | -9.5932724 | 0.3313877 | -70.646975 | PASS |
| 45619.474 | -9.635994 | 0.32976177 | -70.745684 | PASS |
| 45870.075 | -9.6785314 | 0.32815077 | -70.843427 | PASS |
| 46120.677 | -9.7208858 | 0.32655453 | -70.940218 | PASS |
| 46371.278 | -9.7630586 | 0.32497284 | -71.03607 | PASS |
| 46621.88 | -9.805051 | 0.32340554 | -71.130997 | PASS |
| 46872.481 | -9.8468643 | 0.32185242 | -71.225011 | PASS |
| 47123.083 | -9.8884999 | 0.32031332 | -71.318126 | PASS |
| 47373.684 | -9.929959 | 0.31878806 | -71.410352 | PASS |
| 47624.286 | -9.9712428 | 0.31727647 | -71.501703 | PASS |
| 47874.887 | -10.012353 | 0.31577836 | -71.592191 | PASS |
| 48125.489 | -10.05329 | 0.31429359 | -71.681827 | PASS |
| 48376.09 | -10.094055 | 0.31282197 | -71.770622 | PASS |
| 48626.692 | -10.13465 | 0.31136334 | -71.858589 | PASS |
| 48877.293 | -10.175076 | 0.30991756 | -71.945738 | PASS |
| 49127.895 | -10.215335 | 0.30848444 | -72.03208 | PASS |
| 49378.496 | -10.255426 | 0.30706385 | -72.117627 | PASS |
| 49629.098 | -10.295352 | 0.30565563 | -72.202388 | PASS |
| 49879.699 | -10.335114 | 0.30425962 | -72.286374 | PASS |
| 50130.301 | -10.374712 | 0.30287568 | -72.369595 | PASS |
| 50380.902 | -10.414148 | 0.30150365 | -72.452062 | PASS |
| 50631.504 | -10.453424 | 0.3001434 | -72.533784 | PASS |
| 50882.105 | -10.49254 | 0.29879478 | -72.614771 | PASS |
| 51132.707 | -10.531497 | 0.29745766 | -72.695032 | PASS |
| 51383.308 | -10.570297 | 0.29613189 | -72.774577 | PASS |
| 51633.91 | -10.60894 | 0.29481733 | -72.853416 | PASS |
| 51884.511 | -10.647428 | 0.29351386 | -72.931557 | PASS |
| 52135.113 | -10.685762 | 0.29222133 | -73.009009 | PASS |
| 52385.714 | -10.723942 | 0.29093963 | -73.085781 | PASS |
| 52636.316 | -10.761971 | 0.28966862 | -73.161882 | PASS |
| 52886.917 | -10.799849 | 0.28840818 | -73.23732 | PASS |
| 53137.519 | -10.837576 | 0.28715817 | -73.312104 | PASS |
| 53388.12 | -10.875155 | 0.28591849 | -73.386241 | PASS |
| 53638.722 | -10.912586 | 0.284689 | -73.45974 | PASS |
| 53889.323 | -10.94987 | 0.28346959 | -73.53261 | PASS |
| 54139.925 | -10.987009 | 0.28226014 | -73.604856 | PASS |
| 54390.526 | -11.024002 | 0.28106054 | -73.676489 | PASS |
| 54641.128 | -11.060852 | 0.27987067 | -73.747514 | PASS |
| 54891.729 | -11.097559 | 0.27869041 | -73.81794 | PASS |
| 55142.331 | -11.134125 | 0.27751967 | -73.887774 | PASS |
| 55392.932 | -11.170549 | 0.27635832 | -73.957023 | PASS |
| 55643.534 | -11.206834 | 0.27520626 | -74.025694 | PASS |
| 55894.135 | -11.24298 | 0.27406339 | -74.093794 | PASS |
| 56144.737 | -11.278987 | 0.2729296 | -74.161331 | PASS |
| 56395.338 | -11.314858 | 0.27180478 | -74.22831 | PASS |
| 56645.94 | -11.350593 | 0.27068884 | -74.294739 | PASS |
| 56896.541 | -11.386193 | 0.26958168 | -74.360624 | PASS |
| 57147.143 | -11.421658 | 0.26848319 | -74.425972 | PASS |
| 57397.744 | -11.45699 | 0.26739329 | -74.490789 | PASS |
| 57648.346 | -11.49219 | 0.26631186 | -74.555082 | PASS |
| 57898.947 | -11.527258 | 0.26523883 | -74.618856 | PASS |
| 58149.549 | -11.562196 | 0.26417409 | -74.682117 | PASS |
| 58400.15 | -11.597003 | 0.26311756 | -74.744872 | PASS |
| 58650.752 | -11.631682 | 0.26206914 | -74.807127 | PASS |
| 58901.353 | -11.666234 | 0.26102874 | -74.868887 | PASS |
| 59151.955 | -11.700657 | 0.25999628 | -74.930159 | PASS |
| 59402.556 | -11.734955 | 0.25897167 | -74.990947 | PASS |
| 59653.158 | -11.769127 | 0.25795482 | -75.051257 | PASS |
| 59903.759 | -11.803175 | 0.25694565 | -75.111096 | PASS |
| 60154.361 | -11.837099 | 0.25594407 | -75.170467 | PASS |
| 60404.962 | -11.870899 | 0.25495001 | -75.229377 | PASS |
| 60655.564 | -11.904578 | 0.25396338 | -75.287831 | PASS |
| 60906.165 | -11.938135 | 0.2529841 | -75.345833 | PASS |
| 61156.767 | -11.971572 | 0.2520121 | -75.40339 | PASS |
| 61407.368 | -12.004889 | 0.25104729 | -75.460506 | PASS |
| 61657.97 | -12.038087 | 0.2500896 | -75.517186 | PASS |
| 61908.571 | -12.071167 | 0.24913895 | -75.573434 | PASS |
| 62159.173 | -12.10413 | 0.24819527 | -75.629257 | PASS |
| 62409.774 | -12.136976 | 0.24725849 | -75.684657 | PASS |
| 62660.376 | -12.169706 | 0.24632853 | -75.739641 | PASS |
| 62910.977 | -12.202321 | 0.24540532 | -75.794212 | PASS |
| 63161.579 | -12.234821 | 0.24448879 | -75.848375 | PASS |
| 63412.18 | -12.267208 | 0.24357886 | -75.902135 | PASS |
| 63662.782 | -12.299482 | 0.24267548 | -75.955496 | PASS |
| 63913.383 | -12.331644 | 0.24177858 | -76.008463 | PASS |
| 64163.985 | -12.363694 | 0.24088808 | -76.061039 | PASS |
| 64414.586 | -12.395634 | 0.24000391 | -76.113229 | PASS |
| 64665.188 | -12.427463 | 0.23912603 | -76.165036 | PASS |
| 64915.789 | -12.459183 | 0.23825435 | -76.216466 | PASS |
| 65166.391 | -12.490795 | 0.23738882 | -76.267522 | PASS |
| 65416.992 | -12.522298 | 0.23652938 | -76.318209 | PASS |
| 65667.594 | -12.553695 | 0.23567595 | -76.368529 | PASS |
| 65918.195 | -12.584984 | 0.23482849 | -76.418487 | PASS |
| 66168.797 | -12.616168 | 0.23398693 | -76.468087 | PASS |
| 66419.398 | -12.647247 | 0.23315121 | -76.517332 | PASS |
| 66670 | -12.678221 | 0.23232127 | -76.566227 | PASS |
| 66920.602 | -12.709091 | 0.23149705 | -76.614774 | PASS |
| 67171.203 | -12.739857 | 0.23067851 | -76.662979 | PASS |
| 67421.805 | -12.770522 | 0.22986557 | -76.710843 | PASS |
| 67672.406 | -12.801084 | 0.22905819 | -76.75837 | PASS |
| 67923.008 | -12.831544 | 0.2282563 | -76.805565 | PASS |
| 68173.609 | -12.861904 | 0.22745987 | -76.85243 | PASS |
| 68424.211 | -12.892164 | 0.22666882 | -76.89897 | PASS |
| 68674.812 | -12.922325 | 0.22588312 | -76.945186 | PASS |
| 68925.414 | -12.952386 | 0.2251027 | -76.991083 | PASS |
| 69176.015 | -12.982349 | 0.22432751 | -77.036663 | PASS |
| 69426.617 | -13.012215 | 0.22355751 | -77.081931 | PASS |
| 69677.218 | -13.041983 | 0.22279264 | -77.126889 | PASS |
| 69927.82 | -13.071655 | 0.22203285 | -77.17154 | PASS |
| 70178.421 | -13.101231 | 0.2212781 | -77.215887 | PASS |
| 70429.023 | -13.130712 | 0.22052834 | -77.259933 | PASS |
| 70679.624 | -13.160098 | 0.21978351 | -77.303682 | PASS |
| 70930.226 | -13.18939 | 0.21904357 | -77.347136 | PASS |
| 71180.827 | -13.218588 | 0.21830848 | -77.390299 | PASS |
| 71431.429 | -13.247693 | 0.21757819 | -77.433172 | PASS |
| 71682.03 | -13.276706 | 0.21685264 | -77.475759 | PASS |
| 71932.632 | -13.305626 | 0.21613181 | -77.518064 | PASS |
| 72183.233 | -13.334456 | 0.21541563 | -77.560087 | PASS |
| 72433.835 | -13.363194 | 0.21470408 | -77.601833 | PASS |
| 72684.436 | -13.391842 | 0.2139971 | -77.643304 | PASS |
| 72935.038 | -13.420401 | 0.21329465 | -77.684503 | PASS |
| 73185.639 | -13.44887 | 0.21259669 | -77.725431 | PASS |
| 73436.241 | -13.47725 | 0.21190318 | -77.766093 | PASS |
| 73686.842 | -13.505543 | 0.21121408 | -77.80649 | PASS |
| 73937.444 | -13.533747 | 0.21052934 | -77.846625 | PASS |
| 74188.045 | -13.561865 | 0.20984893 | -77.886501 | PASS |
| 74438.647 | -13.589896 | 0.20917281 | -77.926119 | PASS |
| 74689.248 | -13.61784 | 0.20850093 | -77.965483 | PASS |
| 74939.85 | -13.645699 | 0.20783325 | -78.004594 | PASS |
| 75190.451 | -13.673473 | 0.20716975 | -78.043456 | PASS |
| 75441.053 | -13.701162 | 0.20651038 | -78.082071 | PASS |
| 75691.654 | -13.728767 | 0.2058551 | -78.12044 | PASS |
| 75942.256 | -13.756289 | 0.20520388 | -78.158566 | PASS |
| 76192.857 | -13.783727 | 0.20455667 | -78.196452 | PASS |
| 76443.459 | -13.811083 | 0.20391345 | -78.234099 | PASS |
| 76694.06 | -13.838356 | 0.20327418 | -78.27151 | PASS |
| 76944.662 | -13.865547 | 0.20263882 | -78.308688 | PASS |
| 77195.263 | -13.892657 | 0.20200733 | -78.345633 | PASS |
| 77445.865 | -13.919687 | 0.20137969 | -78.382349 | PASS |
| 77696.466 | -13.946636 | 0.20075586 | -78.418837 | PASS |
| 77947.068 | -13.973505 | 0.2001358 | -78.4551 | PASS |
| 78197.669 | -14.000294 | 0.19951948 | -78.491139 | PASS |
| 78448.271 | -14.027004 | 0.19890687 | -78.526957 | PASS |
| 78698.872 | -14.053636 | 0.19829793 | -78.562556 | PASS |
| 78949.474 | -14.08019 | 0.19769264 | -78.597937 | PASS |
| 79200.075 | -14.106666 | 0.19709096 | -78.633103 | PASS |
| 79450.677 | -14.133065 | 0.19649286 | -78.668055 | PASS |
| 79701.278 | -14.159387 | 0.1958983 | -78.702795 | PASS |
| 79951.88 | -14.185632 | 0.19530727 | -78.737326 | PASS |
| 80202.481 | -14.211801 | 0.19471972 | -78.771649 | PASS |
| 80453.083 | -14.237895 | 0.19413563 | -78.805766 | PASS |
| 80703.684 | -14.263914 | 0.19355496 | -78.839679 | PASS |
| 80954.286 | -14.289858 | 0.19297769 | -78.87339 | PASS |
| 81204.887 | -14.315727 | 0.19240379 | -78.9069 | PASS |
| 81455.489 | -14.341523 | 0.19183323 | -78.940211 | PASS |
| 81706.09 | -14.367245 | 0.19126599 | -78.973325 | PASS |
| 81956.692 | -14.392894 | 0.19070202 | -79.006244 | PASS |
| 82207.293 | -14.41847 | 0.19014131 | -79.038969 | PASS |
| 82457.895 | -14.443974 | 0.18958383 | -79.071502 | PASS |
| 82708.496 | -14.469406 | 0.18902955 | -79.103845 | PASS |
| 82959.098 | -14.494767 | 0.18847844 | -79.135999 | PASS |
| 83209.699 | -14.520056 | 0.18793047 | -79.167966 | PASS |
| 83460.301 | -14.545274 | 0.18738563 | -79.199748 | PASS |
| 83710.902 | -14.570422 | 0.18684388 | -79.231346 | PASS |
| 83961.504 | -14.5955 | 0.18630521 | -79.262762 | PASS |
| 84212.105 | -14.620509 | 0.18576957 | -79.293997 | PASS |
| 84462.707 | -14.645448 | 0.18523695 | -79.325053 | PASS |
| 84713.308 | -14.670318 | 0.18470732 | -79.355931 | PASS |
| 84963.91 | -14.695119 | 0.18418067 | -79.386633 | PASS |
| 85214.511 | -14.719853 | 0.18365695 | -79.41716 | PASS |
| 85465.113 | -14.744518 | 0.18313616 | -79.447514 | PASS |
| 85715.714 | -14.769116 | 0.18261826 | -79.477697 | PASS |
| 85966.316 | -14.793647 | 0.18210323 | -79.507709 | PASS |
| 86216.917 | -14.818111 | 0.18159105 | -79.537552 | PASS |
| 86467.519 | -14.842509 | 0.1810817 | -79.567228 | PASS |
| 86718.12 | -14.866841 | 0.18057514 | -79.596738 | PASS |
| 86968.722 | -14.891106 | 0.18007137 | -79.626083 | PASS |
| 87219.323 | -14.915307 | 0.17957036 | -79.655265 | PASS |
| 87469.925 | -14.939442 | 0.17907208 | -79.684284 | PASS |
| 87720.526 | -14.963513 | 0.17857651 | -79.713143 | PASS |
| 87971.128 | -14.98752 | 0.17808364 | -79.741843 | PASS |
| 88221.729 | -15.011462 | 0.17759343 | -79.770385 | PASS |
| 88472.331 | -15.035341 | 0.17710588 | -79.79877 | PASS |
| 88722.932 | -15.059156 | 0.17662095 | -79.826999 | PASS |
| 88973.534 | -15.082908 | 0.17613863 | -79.855074 | PASS |
| 89224.135 | -15.106597 | 0.17565889 | -79.882996 | PASS |
| 89474.737 | -15.130224 | 0.17518172 | -79.910767 | PASS |
| 89725.338 | -15.153789 | 0.1747071 | -79.938387 | PASS |
| 89975.94 | -15.177292 | 0.174235 | -79.965857 | PASS |
| 90226.541 | -15.200734 | 0.1737654 | -79.99318 | PASS |
| 90477.143 | -15.224114 | 0.1732983 | -80.020355 | PASS |
| 90727.744 | -15.247434 | 0.17283366 | -80.047385 | PASS |
| 90978.346 | -15.270693 | 0.17237146 | -80.07427 | PASS |
| 91228.947 | -15.293891 | 0.1719117 | -80.101012 | PASS |
| 91479.549 | -15.31703 | 0.17145435 | -80.127611 | PASS |
| 91730.15 | -15.340109 | 0.17099938 | -80.15407 | PASS |
| 91980.752 | -15.363129 | 0.17054679 | -80.180388 | PASS |
| 92231.353 | -15.38609 | 0.17009656 | -80.206567 | PASS |
| 92481.955 | -15.408991 | 0.16964866 | -80.232608 | PASS |
| 92732.556 | -15.431835 | 0.16920308 | -80.258512 | PASS |
| 92983.158 | -15.45462 | 0.1687598 | -80.284281 | PASS |
| 93233.759 | -15.477347 | 0.1683188 | -80.309915 | PASS |
| 93484.361 | -15.500017 | 0.16788007 | -80.335415 | PASS |
| 93734.962 | -15.522629 | 0.16744359 | -80.360783 | PASS |
| 93985.564 | -15.545185 | 0.16700934 | -80.386019 | PASS |
| 94236.165 | -15.567683 | 0.16657731 | -80.411124 | PASS |
| 94486.767 | -15.590125 | 0.16614747 | -80.4361 | PASS |
| 94737.368 | -15.612511 | 0.16571982 | -80.460947 | PASS |
| 94987.97 | -15.634841 | 0.16529433 | -80.485667 | PASS |
| 95238.571 | -15.657115 | 0.16487099 | -80.51026 | PASS |
| 95489.173 | -15.679334 | 0.16444979 | -80.534727 | PASS |
| 95739.774 | -15.701497 | 0.1640307 | -80.559069 | PASS |
| 95990.376 | -15.723606 | 0.16361372 | -80.583288 | PASS |
| 96240.977 | -15.74566 | 0.16319882 | -80.607384 | PASS |
| 96491.579 | -15.767659 | 0.16278599 | -80.631358 | PASS |
| 96742.18 | -15.789605 | 0.16237522 | -80.655211 | PASS |
| 96992.782 | -15.811497 | 0.16196649 | -80.678943 | PASS |
| 97243.383 | -15.833335 | 0.16155978 | -80.702557 | PASS |
| 97493.985 | -15.85512 | 0.16115508 | -80.726052 | PASS |
| 97744.586 | -15.876851 | 0.16075239 | -80.74943 | PASS |
| 97995.188 | -15.89853 | 0.16035167 | -80.772691 | PASS |
| 98245.789 | -15.920157 | 0.15995292 | -80.795837 | PASS |
| 98496.391 | -15.941731 | 0.15955612 | -80.818867 | PASS |
| 98746.992 | -15.963253 | 0.15916126 | -80.841784 | PASS |
| 98997.594 | -15.984723 | 0.15876833 | -80.864587 | PASS |
| 99248.195 | -16.006141 | 0.1583773 | -80.887278 | PASS |
| 99498.797 | -16.027508 | 0.15798818 | -80.909858 | PASS |
| 99749.398 | -16.048824 | 0.15760094 | -80.932327 | PASS |
| 100000 | -16.070089 | 0.15721556 | -80.954686 | PASS |
