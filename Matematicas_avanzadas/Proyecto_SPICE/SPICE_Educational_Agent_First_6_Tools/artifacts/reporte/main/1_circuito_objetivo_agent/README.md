# HSPICE conversion notes

## Files

- `circuito_objetivo_hspice.sp`: HSPICE-oriented deck for the 300-point AC sweep.

## Mapping and assumptions

- `G1 N1 OUT 0.00078740157480315` and `G2 NP 0 0.000434782608695652` mean explicit conductances in the educational project. In HSPICE, a `G`-prefixed element is a voltage-controlled current source, not a two-terminal conductance. They are therefore represented by `RG1=1/G1=1.27 kOhm` and `RG2=1/G2=2.3 kOhm`; these passive replacements preserve the conductances.
- `.OPAMP U1 NP NM OUT IDEAL` is a project-specific MNA extension, not portable HSPICE syntax. `EOP OUT 0 NP NM 1e9` is a voltage-controlled voltage source with finite open-loop gain 1e9. It has zero input current and zero modeled output resistance, but the constraint `V(NP)=V(NM)` is no longer exact. This deck is an approximation to the ideal-op-amp response. HSPICE's finite-gain result may differ slightly or encounter conditioning/convergence limitations; inspect its run log and consider a gain-convergence study before treating it as equivalent.
- The AC source is set to 1 V rather than 1 mV. Because this is a linear circuit, the transfer function is unchanged; with `V(IN)=1 V at 0 degrees`, `V(OUT)` equals `Vo/Vi`. Thus `VM(OUT)` is the linear gain, `VDB(OUT)` its dB value, and `VP(OUT)` its phase. `V(IN)` is printed as an input/reference check.
- `.AC LIN 300 10 100k` preserves the requested sweep range and point count.
- Initial conditions are not used in small-signal AC analysis; no transient analysis is included.

## Run and verification

A typical invocation is `hspice circuito_objetivo_hspice.sp`. HSPICE was not installed in the current environment, so this deck has not been run or syntax-validated by HSPICE here. The educational MNA artifacts remain the validated results for the exact ideal model; this conversion is not an external validation of them.
