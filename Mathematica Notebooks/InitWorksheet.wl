(* ::Package:: *)

(* ::Package:: *)
(**)


(* Copyright 2026 Robot Squirrel Productions.  All rights reserved. This computer code is proprietary to Robot Squirrel Productions and/or its affiliate(s) and may be covered by patents. It may not be used, disclosed, modified, transferred, or reproduced without prior written consent. *)

BeginPackage["MyUtilities`InitWorksheet`"]

ClearAll[PrintAreaMomentOfInertia, Iprint, 
  PrintLength, hprint, wprint, tprint, 
  PrintAccel, accprint, 
  PrintArea, aprint,
  PrintMagField, mgprint, 
  PrintMagFluxDensity, fdprint,
  PrintMass, maprint, 
  PrintPress, pprint,
  PrintPressSlope, slprint,
  PrintCap, caprint,
  PrintTemp, tmprint,
  PrintVol, volprint,
  PrintPower, pwprint,
  PrintPermeability, pmprint,
  PrintUnitless, puprint,
  PrintFrequency, fqprint,
  PrintResistanceLength, rlprint,
  PrintAngle, angprint,
  PrintCoords, cdprint,
  PrintPhasor, phprint]

PrintAreaMomentOfInertia::usage = "PrintAreaMomentOfInertia[inertia, opts] prints the area moment of inertia in mm\:2074 (in\:2074) or reverse."
Iprint::usage = "Shorthand for PrintAreaMomentOfInertia."

PrintLength::usage = "PrintLength[length, opts] prints a linear dimension in mm (in) or in (mm)."
hprint::usage = "Shorthand for PrintLength (height)."
wprint::usage = "Shorthand for PrintLength with Label \[RightArrow] \"Width (w)\"."
tprint::usage = "Shorthand for PrintLength with Label \[RightArrow] \"Thickness (t)\"."

PrintAccel::usage = "PrintAccel[accceleration, opts] prints acceleration in m/\!\(\*SuperscriptBox[\(s\), \(2\)]\)(in/\!\(\*SuperscriptBox[\(s\), \(2\)]\)) or in/\!\(\*SuperscriptBox[\(s\), \(2\)]\) (m/\!\(\*SuperscriptBox[\(s\), \(2\)]\))."
accprint::usage = "Shorthand for PrintAccel (acceleration)."

PrintArea::usage = "PrintArea[length, opts] prints area in \!\(\*SuperscriptBox[\(mm\), \(2\)]\) (\!\(\*SuperscriptBox[\(in\), \(2\)]\)) or \!\(\*SuperscriptBox[\(in\), \(2\)]\) (\!\(\*SuperscriptBox[\(mm\), \(2\)]\))."
aprint::usage = "Shorthand for PrintArea."

PrintPress::usage = "PrintPress[press, opts] prints pressure in kilopascals (psi) or psi (kilopascals)."
pprint::usage = "Shorthand for PrintPress."

PrintPressSlope::usage = "PrintPressSlope[length, opts] prints transducer sensitivity slope in bar/mV (psi/mV, kgf/\!\(\*SuperscriptBox[\(cm\), \(2\)]\)/mV) or psi/mV (bar/mV, kgf/\!\(\*SuperscriptBox[\(cm\), \(2\)]\)/mV)."
slprint::usage = "Shorthand for PrintPressSlope."

PrintForce::usage = "PrintForce[length, opts] prints force in newtons (lbf) or lbf (newtons)."
fcprint::usage = "Shorthand for PrintForce."

PrintForceKilo::usage = "PrintForce[length, opts] prints force in kilonewtons (kips) or kips (kilonewtons)."
fcprintk::usage = "Shorthand for PrintForce."

PrintModulusElasticity::usage = "PrintModulusElasticity[length, opts] prints modulus of elasticity in GPa (psi) or psi (GPa)."
meprint::usage = "Shorthand for PrintModulusElasticity."

PrintDensity::usage = "PrintDensity[length, opts] prints density in g/cc (lb/\!\(\*SuperscriptBox[\(in\), \(3\)]\)) or lb/\!\(\*SuperscriptBox[\(in\), \(3\)]\) (g/cc)."
dprint::usage = "Shorthand for PrintDensity."

PrintMassPerLength::usage = "PrintMassPerLength[length, opts] prints density in g/mm (lb/in) or lb/in (g/mm)."
mlprint::usage = "Shorthand for PrintMassPerLength."

PrintMagField::usage = "PrintMagField[mass, opts] prints magnetic field in A/m (Oe) or Oe (A/m)."
mgprint::usage = "Shorthand for PrintMagField."

PrintMagFluxDensity::usage = "PrintMagField[magflux, opts] prints magnetic flux density in T (G) or G (T)."
fdprint::usage = "Shorthand for PrintMagFluxDensity."

PrintMass::usage = "PrintMass[mass, opts] prints mass in kg (lb) or lb (kg)."
massprint::usage = "Shorthand for PrintMass."

PrintCap::usage = "PrintCap[cap, opts] prints flow capacity in \!\(\*SuperscriptBox[\(m\), \(3\)]\)/min (MMCFD) or MMCFD (\!\(\*SuperscriptBox[\(m\), \(3\)]\)/min)."
caprint::usage = "Shorthand for PrintMassPerLength."

PrintVol::usage = "PrintVol[vol, opts] prints volumes in \!\(\*SuperscriptBox[\(m\), \(3\)]\) (\!\(\*SuperscriptBox[\(in\), \(3\)]\), \!\(\*SuperscriptBox[\(mm\), \(3\)]\)) or \!\(\*SuperscriptBox[\(in\), \(3\)]\) (\!\(\*SuperscriptBox[\(m\), \(3\)]\), \!\(\*SuperscriptBox[\(mm\), \(3\)]\))."
volprint::usage = "Shorthand for PrintVol."

PrintPower::usage = "PrintPower[pwr, opts] prints power in kW (HP) or HP (kW)."
pwprint::usage = "Shorthand for PrintPower."

PrintPermeability::usage = "PrintPermeability[perm, opts] prints magnetic permeability in henries/meter (henries/in)."
pmprint::usage = "Shorthand for PrintPermeability."

PrintUnitless::usage = "PrintUnitless[value, opts] prints unitless values in - (-)."
puprint::usage = "Shorthand for PrintUnitless."

PrintFrequency::usage = "PrintFrequency[value, opts] prints frequency values in units of RPM (hertz, radians/second) or hertz (RPM, radians/second)."
fqprint::usage = "Shorthand for PrintFrequency."

PrintResistanceLength::usage =
  "PrintResistanceLength[rl, opts] prints electrical resistance\[Dash]length in Ohm-cm (Ohm-in) or Ohm-in (Ohm-cm).";
rlprint::usage =
  "Shorthand for PrintResistanceLength.";

PrintAngle::usage =
  "PrintAngle[theta, opts] prints angle in degrees (radians) or radians (degrees). If theta is numeric, it is assumed to be in radians.";
angprint::usage = "Shorthand for PrintAngle.";

PrintCoords::usage = "PrintCoords[complex, opts] prints real and imaginary components in mm (in) or in (mm)."
cdprint::usage = "Shorthand for PrintCoords."

PrintPhasor::usage = "Prints complex values or complex quantities in phasor form."
phprint::usage = "Shorthand for PrintPhasor" 

Begin["`Private`"]

(* Acceleration *)
AccelToSI[a_?QuantityQ] := UnitConvert[a, "Meters"/("Seconds")^2]
AccelToUSCS[a_?QuantityQ]  := UnitConvert[a, "Inches"/("Seconds")^2]

FormatLengthValue[v_?QuantityQ, prec_:3] := NumberForm[N[v], prec]

Options[PrintAccel] = {"Label" -> "Acceleration", "Precision" -> 3, "SIUnitFirst" -> True};
PrintAccel[Accel_?QuantityQ, OptionsPattern[]] := Module[{
    ms2 = AccelToSI[Accel], ins2 = AccelToUSCS[Accel]},
   Print[StringPadLeft[OptionValue["Label"] <> ": ", 28],
    If[TrueQ[OptionValue["SIUnitFirst"]],
     Row[{FormatLengthValue[ms2, OptionValue["Precision"]], " (", FormatLengthValue[ins2, OptionValue["Precision"]], ")"}],
     Row[{FormatLengthValue[ins2, OptionValue["Precision"]], " (", FormatLengthValue[ms2, OptionValue["Precision"]], ")"}]
    ]]
]

accprint = PrintAccel;

(* Moment of inertia *)
InertiaToMillimeters\:2074[i_?QuantityQ] := UnitConvert[i, ("Millimeters")^4]
InertiaToInches\:2074[i_?QuantityQ]      := UnitConvert[i, ("Inches")^4]

FormatInertiaValue[v_?QuantityQ, prec_:6] := NumberForm[N[v], prec]

Options[PrintAreaMomentOfInertia] = {"Label" -> "Area Moment of Inertia", "Precision" -> 6, "SIUnitFirst" -> True};
PrintAreaMomentOfInertia[inertia_?QuantityQ, OptionsPattern[]] := Module[{
    mm4 = InertiaToMillimeters\:2074[inertia], in4 = InertiaToInches\:2074[inertia]},
   Print[StringPadLeft[OptionValue["Label"] <> ": ", 28],
    If[TrueQ[OptionValue["SIUnitFirst"]],
     Row[{FormatInertiaValue[mm4, OptionValue["Precision"]], " (", FormatInertiaValue[in4, OptionValue["Precision"]], ")"}],
     Row[{FormatInertiaValue[in4, OptionValue["Precision"]], " (", FormatInertiaValue[mm4, OptionValue["Precision"]], ")"}]
    ]]
]

Iprint = PrintAreaMomentOfInertia;

(* Linear dimensions *)
ToMillimeters[l_?QuantityQ] := UnitConvert[l, "Millimeters"]
ToInches[l_?QuantityQ]      := UnitConvert[l, "Inches"]

FormatLengthValue[v_?QuantityQ, prec_:3] := NumberForm[N[v], prec]

Options[PrintLength] = {"Label" -> "Height (h)", 
	"Precision" -> 3, 
	"SIUnitFirst" -> True,
	"LabelWidth" -> 200};
	
PrintLength[Area_?QuantityQ, OptionsPattern[]] := Module[
  {mm = ToMillimeters[Area], inch = ToInches[Area]},
	
  label = OptionValue["Label"];
	
  valueRow =
    If[TrueQ[OptionValue["SIUnitFirst"]],
      Row[{FormatLengthValue[mm, OptionValue["Precision"]],
           " (", FormatLengthValue[inch, OptionValue["Precision"]], ")"}],
      Row[{FormatLengthValue[inch, OptionValue["Precision"]],
           " (", FormatLengthValue[mm, OptionValue["Precision"]], ")"}]
    ];
  Print @ Row[{
    Pane[
      Row[{label, ": "}],
      Alignment -> Right,
      ImageSize -> {OptionValue["LabelWidth"], Automatic}
    ],
    valueRow
  }];
  
];

hprint = PrintLength;
wprint = PrintLength[#, "Label" -> "Width (w)"] &;
tprint = PrintLength[#, "Label" -> "Thickness (t)"] &;

(* Area *)
AreaToMillimeters[l_?QuantityQ] := UnitConvert[l, ("Millimeters")^2]
AreaToInches[l_?QuantityQ]      := UnitConvert[l, ("Inches")^2]

FormatLengthValue[v_?QuantityQ, prec_:3] := NumberForm[N[v], prec]

Options[PrintArea] = {"Label" -> "Area", "Precision" -> 3, "SIUnitFirst" -> True};

PrintArea[len_?QuantityQ, OptionsPattern[]] := Module[{
    mm2 = AreaToMillimeters[len], inch2 = AreaToInches[len]},
   Print[StringPadLeft[OptionValue["Label"] <> ": ", 28],
    If[TrueQ[OptionValue["SIUnitFirst"]],
     Row[{FormatLengthValue[mm2, OptionValue["Precision"]], " (", FormatLengthValue[inch2, OptionValue["Precision"]], ")"}],
     Row[{FormatLengthValue[inch2, OptionValue["Precision"]], " (", FormatLengthValue[mm2, OptionValue["Precision"]], ")"}]
    ]]
]

aprint = PrintArea;

(* Pressure *)
PressureToKilopascals[l_?QuantityQ] := UnitConvert[l, "Kilopascals"]
PressureToPSI[l_?QuantityQ]      := UnitConvert[l,  "PoundsForce"/("Inches" * "Inches")]
PressureToBars[l_?QuantityQ] := UnitConvert[l, "Bars"]

FormatPressValue[v_?QuantityQ, prec_:3] := NumberForm[N[v], prec]

Options[PrintPress] = {
  "Label" -> "Area", 
  "Precision" -> 9, 
  "SIUnitFirst" -> True,
  "LabelWidth" -> 200};

PrintPress[Press_?QuantityQ, OptionsPattern[]] := Module[
  {
    presskpa = PressureToKilopascals[Press],
    presspsi = PressureToPSI[Press],
    pressbar = PressureToBars[Press]
    },

  label = OptionValue["Label"];

  valueRow =
    If[TrueQ[OptionValue["SIUnitFirst"]],
      Row[{
        FormatPressValue[presskpa, OptionValue["Precision"]],
        " (", FormatPressValue[presspsi, OptionValue["Precision"]], FormatPressValue[pressbar, OptionValue["Precision"]], ")"
      }],
      Row[{
        FormatPressValue[presspsi, OptionValue["Precision"]],
        " (", FormatPressValue[presskpa, OptionValue["Precision"]], FormatPressValue[pressbar, OptionValue["Precision"]], ")"
      }]
    ];

  Print @ Row[{
    Pane[
      Row[{label, ": "}],
      Alignment -> Right,
      ImageSize -> {OptionValue["LabelWidth"], Automatic}
    ],
    valueRow
  }];
];

pprint = PrintPress;

(* Pressure Slope *)
PressureSlopeToKilopascals[p_?QuantityQ] := UnitConvert[p, "Kilopascals"/"Millivolts"]
PressureSlopeToKgf[p_?QuantityQ] := UnitConvert[p, ("KilogramsForce"/("Centimeters" * "Centimeters"))/"Millivolts"]
PressureSlopeToBar[p_?QuantityQ] := UnitConvert[p, "Bars"/"Millivolts"]
PressureSlopeToPSI[p_?QuantityQ]      := UnitConvert[p,  ("PoundsForce"/("Inches" * "Inches"))/"Millivolts"]

FormatLengthValue[v_?QuantityQ, prec_:3] := NumberForm[N[v], prec]

Options[PrintPressSlope] = {"Label" -> "Pressure/voltage slope", "Precision" -> 9, "SIUnitFirst" -> True};
PrintPressSlope[Press_?QuantityQ, OptionsPattern[]] := Module[{
    presskpa = PressureSlopeToKilopascals[Press],
    presspsi = PressureSlopeToPSI[Press],
    presskgf = PressureSlopeToKgf[Press],
    pressbar = PressureSlopeToBar[Press]},
   Print[StringPadLeft[OptionValue["Label"] <> ": ", 28],
    If[TrueQ[OptionValue["SIUnitFirst"]],
     Row[{FormatLengthValue[pressbar, OptionValue["Precision"]], " (",
       FormatLengthValue[presspsi, OptionValue["Precision"]], ", ", 
       FormatLengthValue[presskgf, OptionValue["Precision"]], ",",
       FormatLengthValue[presskpa, OptionValue["Precision"]], ")"}],
     Row[{FormatLengthValue[presspsi, OptionValue["Precision"]], " (", 
       FormatLengthValue[pressbar, OptionValue["Precision"]], ", ", 
       FormatLengthValue[presskgf, OptionValue["Precision"]], ",",
       FormatLengthValue[presskpa, OptionValue["Precision"]], ")"}]
    ]]
]

slprint = PrintPressSlope;

(* Force *)
ForceToNewtons[l_?QuantityQ] := UnitConvert[l, "Newtons"]
ForceTolbf[l_?QuantityQ] := UnitConvert[l,  "PoundsForce"]

FormatForceValue[v_?QuantityQ, prec_:3] := NumberForm[N[v], prec]

Options[PrintForce] = {"Label" -> "Force", "Precision" -> 3, "SIUnitFirst" -> True};
PrintForce[Force_?QuantityQ, OptionsPattern[]] := Module[{
    forcenewton = ForceToNewtons[Force], forcelbf = ForceTolbf[Force]},
   Print[StringPadLeft[OptionValue["Label"] <> ": ", 28],
    If[TrueQ[OptionValue["SIUnitFirst"]],
     Row[{FormatForceValue[forcenewton, OptionValue["Precision"]], " (", FormatForceValue[forcelbf, OptionValue["Precision"]], ")"}],
     Row[{FormatForceValue[forcelbf, OptionValue["Precision"]], " (", FormatForceValue[forcenewton, OptionValue["Precision"]], ")"}]
    ]]
]

fcprint = PrintForce;

(* Force, kilo *)
ForceToSI[l_?QuantityQ] := UnitConvert[l, "Kilonewtons"]
ForceToUSCS[l_?QuantityQ] := UnitConvert[l,  "KipsForce"]

FormatForceValue[v_?QuantityQ, prec_:3] := NumberForm[N[v], prec]

Options[PrintForceKilo] = {"Label" -> "Force", "Precision" -> 3, "SIUnitFirst" -> True};
PrintForceKilo[Force_?QuantityQ, OptionsPattern[]] := Module[{
    forcenewton = ForceToSI[Force], forcelbf = ForceToUSCS[Force]},
   Print[StringPadLeft[OptionValue["Label"] <> ": ", 28],
    If[TrueQ[OptionValue["SIUnitFirst"]],
     Row[{FormatForceValue[forcenewton, OptionValue["Precision"]], " (", FormatForceValue[forcelbf, OptionValue["Precision"]], ")"}],
     Row[{FormatForceValue[forcelbf, OptionValue["Precision"]], " (", FormatForceValue[forcenewton, OptionValue["Precision"]], ")"}]
    ]]
]

fcprint = PrintForce;

(* Modulus of elasticity *)
ModEToGPa[l_?QuantityQ] := UnitConvert[l, "Gigapascals"]
ModETolbf[l_?QuantityQ] := UnitConvert[l,  "PoundsForce"/(("Inches")^2)]

FormatModEValue[v_?QuantityQ, prec_:3] := NumberForm[N[v], prec]

Options[PrintModulusElasticity] = {"Label" -> "Modulus of Elasticity", "Precision" -> 3, "SIUnitFirst" -> True};
PrintModulusElasticity[Mod_?QuantityQ, OptionsPattern[]] := Module[{
    modgpa = ModEToGPa[Mod], modpsi = ModETolbf[Mod]},
   Print[StringPadLeft[OptionValue["Label"] <> ": ", 28],
    If[TrueQ[OptionValue["SIUnitFirst"]],
     Row[{FormatModEValue[modgpa, OptionValue["Precision"]], " (", FormatModEValue[modpsi, OptionValue["Precision"]], ")"}],
     Row[{FormatModEValue[modpsi, OptionValue["Precision"]], " (", FormatModEValue[modgpa, OptionValue["Precision"]], ")"}]
    ]]
]

meprint = PrintModulusElasticity;

(* Density *)
DensityToSI[l_?QuantityQ] := UnitConvert[l, ("Grams"/("Centimeters")^3 )]
DensityToUSCS[l_?QuantityQ] := UnitConvert[l,  ("Pounds"/("Inches")^3 )]

FormatDensityValue[v_?QuantityQ, prec_:3] := NumberForm[N[v], prec]

Options[PrintDensity] = {"Label" -> "Density", "Precision" -> 3, "SIUnitFirst" -> True};
PrintDensity[Density_?QuantityQ, OptionsPattern[]] := Module[{
    modgpa = DensityToSI[Density], modpsi = DensityToUSCS[Density]},
   Print[StringPadLeft[OptionValue["Label"] <> ": ", 28],
    If[TrueQ[OptionValue["SIUnitFirst"]],
     Row[{FormatDensityValue[modgpa, OptionValue["Precision"]], " (", FormatDensityValue[modpsi, OptionValue["Precision"]], ")"}],
     Row[{FormatDensityValue[modpsi, OptionValue["Precision"]], " (", FormatDensityValue[modgpa, OptionValue["Precision"]], ")"}]
    ]]
]

dprint = PrintDensity;

(* Mass per Unit Length *)
MassPerLengthToSI[l_?QuantityQ] := UnitConvert[l, "Grams"/"Millimeters"]
MassPerLengthToUSCS[l_?QuantityQ] := UnitConvert[l,  ("Pounds"/("Inches") )]

FormatMassPerLengthValue[v_?QuantityQ, prec_:3] := NumberForm[N[v], prec]

Options[PrintMassPerLength] = {"Label" -> "Mass per Unit Length", "Precision" -> 3, "SIUnitFirst" -> True};
PrintMassPerLength[MassLength_?QuantityQ, OptionsPattern[]] := Module[{
    masslengthsi = MassPerLengthToSI[MassLength], masslengthuscs = MassPerLengthToUSCS[MassLength]},
   Print[StringPadLeft[OptionValue["Label"] <> ": ", 28],
    If[TrueQ[OptionValue["SIUnitFirst"]],
     Row[{FormatMassPerLengthValue[masslengthsi, OptionValue["Precision"]], " (", FormatMassPerLengthValue[masslengthuscs, OptionValue["Precision"]], ")"}],
     Row[{FormatMassPerLengthValue[masslengthuscs, OptionValue["Precision"]], " (", FormatMassPerLengthValue[masslengthsi, OptionValue["Precision"]], ")"}]
    ]]
]

mlprint = PrintMassPerLength;

(* Magnetic field *)
MagToSI[m_?QuantityQ] := UnitConvert[m, "Amperes"/"Meters"]
MagToUSCS[m_?QuantityQ] := UnitConvert[m, "Oersteds"]

FormatMagValue[v_?QuantityQ, prec_:3] := NumberForm[N[v], prec]

Options[PrintMagField] = {
	"Label" -> "Magnetic Field", 
	"Precision" -> 3, 
	"SIUnitFirst" -> True,
	"LabelWidth" -> 200};
PrintMagField[MagField_?QuantityQ, OptionsPattern[]] := Module[
  {magsi = MagToSI[MagField], maguscs = MagToUSCS[MagField], label, valueRow},

  label = OptionValue["Label"];

  valueRow =
    If[TrueQ[OptionValue["SIUnitFirst"]],
      Row[{
        FormatMagValue[magsi, OptionValue["Precision"]],
        " (", FormatMagValue[maguscs, OptionValue["Precision"]], ")"
      }],
      Row[{
        FormatMagValue[maguscs, OptionValue["Precision"]],
        " (", FormatMagValue[magsi, OptionValue["Precision"]], ")"
      }]
    ];

  Print @ Row[{
    Pane[
      Row[{label, ": "}],
      Alignment -> Right,
      ImageSize -> {OptionValue["LabelWidth"], Automatic}
    ],
    valueRow
  }];
];

mgprint = PrintMagField;

(* Magnetic flux density *)
MagFluxToSI[m_?QuantityQ] := UnitConvert[m, "Tesla"]
MagFluxToUSCS[m_?QuantityQ] := UnitConvert[m, "Gauss"]

FormatMagFluxValue[v_?QuantityQ, prec_:3] := NumberForm[N[v], prec]

Options[PrintMagFluxDensity] = {
	"Label" -> "Magnetic Flux", 
	"Precision" -> 3, 
	"SIUnitFirst" -> True,
	"LabelWidth" -> 200};
PrintMagFluxDensity[MagFlux_?QuantityQ, OptionsPattern[]] := Module[
  {magfluxsi = MagFluxToSI[MagFlux], magfluxuscs = MagFluxToUSCS[MagFlux], label, valueRow},

  label = OptionValue["Label"];

  valueRow =
    If[TrueQ[OptionValue["SIUnitFirst"]],
      Row[{
        FormatMagFluxValue[magfluxsi, OptionValue["Precision"]],
        " (", FormatMagFluxValue[magfluxuscs, OptionValue["Precision"]], ")"
      }],
      Row[{
        FormatMagFluxValue[magfluxuscs, OptionValue["Precision"]],
        " (", FormatMagFluxValue[magfluxsi, OptionValue["Precision"]], ")"
      }]
    ];

  Print @ Row[{
    Pane[
      Row[{label, ": "}],
      Alignment -> Right,
      ImageSize -> {OptionValue["LabelWidth"], Automatic}
    ],
    valueRow
  }];
];

fdprint = PrintMagFluxDensity;

(* Mass p *)
MassToSI[m_?QuantityQ] := UnitConvert[m, "Kilograms"]
MassToUSCS[m_?QuantityQ] := UnitConvert[m, "Pounds"]

FormatMassValue[v_?QuantityQ, prec_:3] := NumberForm[N[v], prec]

Options[PrintMass] = {"Label" -> "Mass", "Precision" -> 3, "SIUnitFirst" -> True};
PrintMass[Mass_?QuantityQ, OptionsPattern[]] := Module[{
    masssi = MassToSI[Mass], massuscs = MassToUSCS[Mass]},
   Print[StringPadLeft[OptionValue["Label"] <> ": ", 28],
    If[TrueQ[OptionValue["SIUnitFirst"]],
     Row[{FormatMassPerLengthValue[masssi, OptionValue["Precision"]], " (", FormatMassPerLengthValue[massuscs, OptionValue["Precision"]], ")"}],
     Row[{FormatMassPerLengthValue[massuscs, OptionValue["Precision"]], " (", FormatMassPerLengthValue[masssi, OptionValue["Precision"]], ")"}]
    ]]
]

mlprint = PrintMassPerLength;

(* Flow capacity *)
FlowCapToSI[c_?QuantityQ] := UnitConvert[c, ("Meters")^3/"Minute"]
FlowCapToUSCS[c_?QuantityQ] := UnitConvert[c,  "Million"("Feet")^3/"Days"]

FormatFlowCapValue[v_?QuantityQ, prec_:3] := NumberForm[N[v], prec]

Options[PrintCap] = {"Label" -> "Mass per Unit Length", "Precision" -> 3, "SIUnitFirst" -> True};
PrintCap[FlowCapacity_?QuantityQ, OptionsPattern[]] := Module[{
    capsi = FlowCapToSI[FlowCapacity], capuscs = FlowCapToUSCS[FlowCapacity]},
   Print[StringPadLeft[OptionValue["Label"] <> ": ", 28],
    If[TrueQ[OptionValue["SIUnitFirst"]],
     Row[{FormatFlowCapValue[capsi, OptionValue["Precision"]], " (", FormatFlowCapValue[capuscs, OptionValue["Precision"]], ")"}],
     Row[{FormatFlowCapValue[capuscs, OptionValue["Precision"]], " (", FormatFlowCapValue[capsi, OptionValue["Precision"]], ")"}]
    ]]
]

caprint = PrintCap;

(* Temperature *)
TempToC[t_?QuantityQ] := UnitConvert[t, "DegreesCelsius"]
TempToF[t_?QuantityQ] := UnitConvert[t, "DegreesFahrenheit"]
TempToK[t_?QuantityQ] := UnitConvert[t, "Kelvins"]
TempToR[t_?QuantityQ] := UnitConvert[t, "DegreesRankine"]

FormatTempValue[v_?QuantityQ, prec_:3] := NumberForm[N[v], prec]

Options[PrintTemp] = {"Label" -> "Temperature", "Precision" -> 9, "SIUnitFirst" -> True};
PrintTemp[Temp_?QuantityQ, OptionsPattern[]] := Module[{
    tempc = TempToC[Temp],
    tempf = TempToF[Temp],
    tempk = TempToK[Temp],
    tempr = TempToR[Temp]},
   Print[StringPadLeft[OptionValue["Label"] <> ": ", 28],
    If[TrueQ[OptionValue["SIUnitFirst"]],
     Row[{FormatTempValue[tempc, OptionValue["Precision"]], " (",
       FormatTempValue[tempf, OptionValue["Precision"]], ", ", 
       FormatTempValue[tempk, OptionValue["Precision"]], ", ",
       FormatTempValue[tempr, OptionValue["Precision"]], ")"}],
     Row[{FormatTempValue[tempf, OptionValue["Precision"]], " (", 
       FormatTempValue[tempc, OptionValue["Precision"]], ", ", 
       FormatTempValue[tempk, OptionValue["Precision"]], ", ",
       FormatTempValue[tempr, OptionValue["Precision"]], ")"}]
    ]]
]

tmprint = PrintTemp;

(* Volume *)
VolToM3[v_?QuantityQ] := UnitConvert[v, ("Meters")^3]
VolToIn3[v_?QuantityQ] := UnitConvert[v, ("Inches")^3]
VolToMM3[v_?QuantityQ] := UnitConvert[v, ("Millimeters")^3]

FormatVolValue[v_?QuantityQ, prec_:3] := NumberForm[N[v], prec]

Options[PrintVol] = {"Label" -> "Volume", "Precision" -> 9, "SIUnitFirst" -> True};
PrintVol[Vol_?QuantityQ, OptionsPattern[]] := Module[{
    volm3 = VolToM3[Vol],
    volin3 = VolToIn3[Vol],
    volmm3 = VolToMM3[Vol]},
   Print[StringPadLeft[OptionValue["Label"] <> ": ", 28],
    If[TrueQ[OptionValue["SIUnitFirst"]],
     Row[{FormatVolValue[volm3, OptionValue["Precision"]], " (",
       FormatVolValue[volin3, OptionValue["Precision"]], ", ", 
       FormatVolValue[volmm3, OptionValue["Precision"]], ")"}],
     Row[{FormatVolValue[volin3, OptionValue["Precision"]], " (", 
       FormatVolValue[volm3, OptionValue["Precision"]], ", ", 
       FormatVolValue[volmm3, OptionValue["Precision"]], ")"}]
    ]]
]

volprint = PrintVol;

(* Power *)
PowerTokW[p_?QuantityQ] := UnitConvert[p, "Kilowatts"]
PowerToHP[p_?QuantityQ] := UnitConvert[p, "Horsepower"]

FormatPowerValue[v_?QuantityQ, prec_:6] := NumberForm[N[v], prec]

Options[PrintPower] = {"Label" -> "Power", "Precision" -> 9, "SIUnitFirst" -> True};
PrintPower[pwr_?QuantityQ, OptionsPattern[]] := Module[{
    powkw = PowerTokW[pwr], powhp = PowerToHP[pwr]},
   Print[StringPadLeft[OptionValue["Label"] <> ": ", 28],
    If[TrueQ[OptionValue["SIUnitFirst"]],
     Row[{FormatPowerValue[powkw, OptionValue["Precision"]], " (", FormatPowerValue[powhp, OptionValue["Precision"]], ")"}],
     Row[{FormatPowerValue[powhp, OptionValue["Precision"]], " (", FormatPowerValue[powkw, OptionValue["Precision"]], ")"}]
    ]]
]

pwprint = PrintPower;

(* Magnetic permeability dimensions *)
ToSI[l_?QuantityQ] := UnitConvert[l, "Henries"/"Meters"]
ToUSCS[l_?QuantityQ]      := UnitConvert[l, "Henries"/"Inches"]

FormatPermValue[v_?QuantityQ, prec_:3] := NumberForm[N[v], prec]

Options[PrintPermeability] = {"Label" -> "Permeability", 
	"Precision" -> 3, 
	"SIUnitFirst" -> True,
	"LabelWidth" -> 200};
	
PrintPermeability[Perm_?QuantityQ, OptionsPattern[]] := Module[
  {pmSI = ToSI[Perm], pmUSCS = ToUSCS[Perm]},
	
  label = OptionValue["Label"];
	
  valueRow =
    If[TrueQ[OptionValue["SIUnitFirst"]],
      Row[{FormatPermValue[pmSI, OptionValue["Precision"]],
           " (", FormatPermValue[pmUSCS, OptionValue["Precision"]], ")"}],
      Row[{FormatPermValue[pmUSCS, OptionValue["Precision"]],
           " (", FormatPermValue[pmSI, OptionValue["Precision"]], ")"}]
    ];
  Print @ Row[{
    Pane[
      Row[{label, ": "}],
      Alignment -> Right,
      ImageSize -> {OptionValue["LabelWidth"], Automatic}
    ],
    valueRow
  }];
  
];

pmprint = PrintPermeability;

(* Unitless values *)
FormatUnitlessValue[v_, prec_: 3] := Module[{mag},
  mag = Which[
    QuantityQ[v], QuantityMagnitude[v],   (* strips units *)
    True, v                              (* plain numeric *)
  ];
  NumberForm[N[mag], {Infinity, prec}]
];

Options[PrintUnitless] = {"Label" -> "Height (h)", 
	"Precision" -> 3, 
	"SIUnitFirst" -> True,
	"LabelWidth" -> 200};
	
(* Accept either numeric or a dimensionless Quantity *)
PrintUnitless[value_ /; (NumericQ[value] || QuantityQ[value]), OptionsPattern[]] := Module[
  {pmSI, pmUSCS, label, valueRow},

  (* For unitless, "SI" and "USCS" are the same by definition *)
  pmSI = value;
  pmUSCS = value;		
  label = OptionValue["Label"];
	
  valueRow =
    If[TrueQ[OptionValue["SIUnitFirst"]],
      Row[{FormatUnitlessValue[pmSI, OptionValue["Precision"]],
           " (", FormatUnitlessValue[pmUSCS, OptionValue["Precision"]], ")"}],
      Row[{FormatUnitlessValue[pmUSCS, OptionValue["Precision"]],
           " (", FormatUnitlessValue[pmSI, OptionValue["Precision"]], ")"}]
    ];
  Print @ Row[{
    Pane[
      Row[{label, ": "}],
      Alignment -> Right,
      ImageSize -> {OptionValue["LabelWidth"], Automatic}
    ],
    valueRow
  }];
  
];

puprint = PrintUnitless;


(* Frequency unit conversion helpers *)
(* Angular frequency \[Omega] input (rad/s) -> outputs RPM, Hz, rad/s               *)


(* --- Convert \[Omega] to a numeric magnitude in rad/s (keeps the "Radians"/"Seconds" unit) --- *)
ToRadPerSec[\[Omega]_?QuantityQ] := UnitConvert[\[Omega], "Radians"/"Seconds"]

(* --- Explicit \[Omega] -> f conversion (bypasses UnitConvert::compat) --- *)
ToHzFromRadPerSec[\[Omega]_?QuantityQ] := Module[
  {\[Omega]rs, mag},
  \[Omega]rs = ToRadPerSec[\[Omega]];
  mag = QuantityMagnitude[\[Omega]rs];               (* numeric value in rad/s *)
  Quantity[mag/(2 Pi), "Hertz"]
]

ToRPMFromRadPerSec[\[Omega]_?QuantityQ] := Module[
  {\[Omega]rs, mag, rpmVal},
  \[Omega]rs = ToRadPerSec[\[Omega]];
  mag = QuantityMagnitude[\[Omega]rs];                  (* numeric value in rad/s *)
  rpmVal = (mag/(2 Pi)) * 60;                    (* (rad/s)/(rad/rev) * s/min *)
  Quantity[rpmVal, "Revolutions"/"Minutes"]      (* construct directly; no UnitConvert *)
]

FormatFreqValue[v_?QuantityQ, prec_: 3] := NumberForm[N[v], prec]

Options[PrintFrequency] = {
  "Label" -> "Frequency",
  "Precision" -> 3,
  "RPMFirst" -> True,
  "LabelWidth" -> 200
};

PrintFrequency[\[Omega]_?QuantityQ, OptionsPattern[]] := Module[
  {pmRPM, pmHz, pmRad, label, valueRow},

  pmRad = ToRadPerSec[\[Omega]];
  pmHz  = ToHzFromRadPerSec[\[Omega]];
  pmRPM = ToRPMFromRadPerSec[\[Omega]];

  label = OptionValue["Label"];

  valueRow =
    If[TrueQ[OptionValue["RPMFirst"]],
      Row[{
        FormatFreqValue[pmRPM, OptionValue["Precision"]], " (",
        FormatFreqValue[pmHz,  OptionValue["Precision"]], ", ",
        FormatFreqValue[pmRad, OptionValue["Precision"]], ")"
      }],
      Row[{
        FormatFreqValue[pmHz, OptionValue["Precision"]], " (",
        FormatFreqValue[pmRPM,  OptionValue["Precision"]], ", ",
        FormatFreqValue[pmRad, OptionValue["Precision"]], ")"
      }]
    ];

  Print @ Row[{
    Pane[
      Row[{label, ": "}],
      Alignment -> Right,
      ImageSize -> {OptionValue["LabelWidth"], Automatic}
    ],
    valueRow
  }];
];

fqprint = PrintFrequency;

(* Electrical resistance\[Dash]length dimensions *)
ToSIResLen[r_?QuantityQ]   := UnitConvert[r, "Ohms"*"Centimeters"]
ToSIResLenMeter[r_?QuantityQ]   := UnitConvert[r, "Ohms"*"Meters"]
ToUSCSResLen[r_?QuantityQ] := UnitConvert[r, "Ohms"*"Inches"]

FormatResLenValue[v_?QuantityQ, prec_: 3] :=
  NumberForm[N[v], prec]

Options[PrintResistanceLength] = {
  "Label" -> "Resistance-Length",
  "Precision" -> 9,
  "SIUnitFirst" -> True,
  "LabelWidth" -> 200
};

PrintResistanceLength[RL_?QuantityQ, OptionsPattern[]] := Module[
  {rlSI = ToSIResLen[RL], rlSIMeter = ToSIResLenMeter[RL], rlUSCS = ToUSCSResLen[RL], label, valueRow},

  label = OptionValue["Label"];

  valueRow =
    If[TrueQ[OptionValue["SIUnitFirst"]],
      Row[{
        FormatResLenValue[rlSI, OptionValue["Precision"]],
        " (", FormatResLenValue[rlSIMeter, OptionValue["Precision"]], " ", FormatResLenValue[rlUSCS, OptionValue["Precision"]], ")"
      }],
      Row[{
        FormatResLenValue[rlUSCS, OptionValue["Precision"]],
        " (", FormatResLenValue[rlSI, OptionValue["Precision"]], " ", FormatResLenValue[rlSIMeter, OptionValue["Precision"]], ")"
      }]
    ];

  Print @ Row[{
    Pane[
      Row[{label, ": "}],
      Alignment -> Right,
      ImageSize -> {OptionValue["LabelWidth"], Automatic}
    ],
    valueRow
  }];
];

rlprint = PrintResistanceLength;


(* Angle *)
AngleToRadians[q_?QuantityQ] := UnitConvert[q, "Radians"]
AngleToDegrees[q_?QuantityQ] := UnitConvert[q, "AngularDegrees"]

FormatAngleValue[v_?QuantityQ, prec_: 3] := NumberForm[N[v], {Infinity, prec}]

Options[PrintAngle] = {
  "Label" -> "Angle",
  "Precision" -> 3,
  "DegreesFirst" -> True,
  "LabelWidth" -> 200
};

PrintAngle[theta_ /; (NumericQ[theta] || QuantityQ[theta]), OptionsPattern[]] := Module[
  {thetaQ, angRad, angDeg, label, valueRow},

  (* If numeric, assume radians *)
  thetaQ = If[QuantityQ[theta], theta, Quantity[theta, "Radians"]];

  angRad = AngleToRadians[thetaQ];
  angDeg = AngleToDegrees[thetaQ];

  label = OptionValue["Label"];

  valueRow =
    If[TrueQ[OptionValue["DegreesFirst"]],
      Row[{FormatAngleValue[angDeg, OptionValue["Precision"]], " (",
        FormatAngleValue[angRad, OptionValue["Precision"]], ")"}],
      Row[{FormatAngleValue[angRad, OptionValue["Precision"]], " (",
        FormatAngleValue[angDeg, OptionValue["Precision"]], ")"}]
    ];

  Print @ Row[{
      Pane[Row[{label, ": "}], Alignment -> Right,
        ImageSize -> {OptionValue["LabelWidth"], Automatic}],
      valueRow
    }];
];

(* Complex Coordinates *)
ComplexToMillimeters[l_?QuantityQ] := UnitConvert[l, "Millimeters"]
ComplexToInches[l_?QuantityQ]      := UnitConvert[l, "Inches"]

FormatComplexCoordsValue[v_?QuantityQ, prec_:3] := NumberForm[N[v], prec]

Options[PrintCoords] = {"Label" -> "x, y", 
	"Precision" -> 3, 
	"SIUnitFirst" -> True,
	"LabelWidth" -> 200};
	
PrintCoords[Area_?QuantityQ, OptionsPattern[]] := Module[
  {mmCoords = ComplexToMillimeters[Area], inchCoords = ComplexToInches[Area]},
	
  label = OptionValue["Label"];
	
  valueRow =
    If[TrueQ[OptionValue["SIUnitFirst"]],
      Row[{FormatComplexCoordsValue[Re[mmCoords], OptionValue["Precision"]], " + \[ImaginaryI]", FormatComplexCoordsValue[Im[mmCoords], OptionValue["Precision"]],
           " (", FormatComplexCoordsValue[Re[inchCoords], OptionValue["Precision"]], " + \[ImaginaryI]", FormatComplexCoordsValue[Im[inchCoords], OptionValue["Precision"]], ")"}],
      Row[{FormatComplexCoordsValue[Re[inchCoords], OptionValue["Precision"]], " + \[ImaginaryI]", FormatComplexCoordsValue[Im[inchCoords], OptionValue["Precision"]],
           " (", FormatComplexCoordsValue[Re[mmCoords], OptionValue["Precision"]], " + \[ImaginaryI]", FormatComplexCoordsValue[Im[mmCoords], OptionValue["Precision"]], ")"}]
    ];
  Print @ Row[{
    Pane[
      Row[{label, ": "}],
      Alignment -> Right,
      ImageSize -> {OptionValue["LabelWidth"], Automatic}
    ],
    valueRow
  }];
  
];

cdprint = PrintCoords;

(* Print Phasor *)
(*Pretty angle symbol \[Angle]*)
phasorAngleBoxes[fmt_]:=MakeBoxes[Style["\[Angle]",18,Bold],fmt];

(*Helper:numeric angle in degrees,rounded for display*)
phasorAngleDeg[z_Complex]:=NumberForm[Round[N[Arg[z]*180./Pi],0.1],{4,1}];

(*----Plain Complex----*)
PrintPhasor/:MakeBoxes[PrintPhasor[z_Complex],fmt_:StandardForm]:=With[{mag=Abs[z],ang=phasorAngleDeg[z],angSym=phasorAngleBoxes[fmt]},RowBox[{MakeBoxes[mag,fmt]," ",angSym," ",MakeBoxes[ang,fmt],"\[Degree]"}]];

(*----Complex Quantity----*)
PrintPhasor/:MakeBoxes[PrintPhasor[q_?QuantityQ],fmt_:StandardForm]:=With[{z=QuantityMagnitude[q],u=QuantityUnit[q]},If[!MatchQ[z,_Complex],MakeBoxes[Unevaluated[phasor[q]],fmt],With[{mag=Quantity[Abs[z],u],ang=phasorAngleDeg[z],angSym=phasorAngleBoxes[fmt]},RowBox[{MakeBoxes[mag,fmt]," ",angSym," ",MakeBoxes[ang,fmt],"\[Degree]"}]]]];

(*----Polar form:phasor[mag,ang] where ang is Quantity----*)
PrintPhasor/:MakeBoxes[PrintPhasor[mag_?QuantityQ,ang_?QuantityQ],fmt_:StandardForm]:=With[{magOut=mag,angDeg=NumberForm[Round[N@QuantityMagnitude@UnitConvert[ang,"Degrees"],0.1],{4,1}],angSym=phasorAngleBoxes[fmt]},RowBox[{MakeBoxes[magOut,fmt]," ",angSym," ",MakeBoxes[angDeg,fmt],"\[Degree]"}]];

(*Convenience:phasor[magNumber,"Ohms",angleQuantity]*)
PrintPhasor/:MakeBoxes[PrintPhasor[mag_?NumericQ,unit_,ang_?QuantityQ],fmt_:StandardForm]:=MakeBoxes[phasor[Quantity[mag,unit],ang],fmt];

End[]
EndPackage[]
