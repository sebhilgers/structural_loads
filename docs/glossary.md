# docs/glossary.md

# Glossary

## Core Concepts

### Action
Classification of a load type (permanent, variable, accidental).
(Einwirkung bzw. Einwirkungsart (Kriterium ist zeitliche Veränderung): Ständig (G), Veränderlich (Q), Außergewöhnlich (A).)

### LoadType
Unterkategorien von Einwirkungen (Einwirkungskategorien):
- Ständig/Permanent: Eigengewicht, Sonstige (z.B. Bodenaufbau)
- Veränderlich/Variable: Nutzlast (Qn, z.B. Wohnen, Büro, VErsammlungsräume), Schnee (Qs), Wind (Qw)
- Außergewöhnlich/Accidental: Anprall 

### LoadCase
Identifies a calculation case and must always be preserved. Groups loads from the same action source.

### LoadGroup
Groups related loads for organizational purposes.
Defines how the individual load cases may be combined together if inserted into a load case combination. Relation: Exclusive, Together

### PointLoad
A concentrated load at a specific location.
- Einheit: kN
- Creation from AreaLoad by multiplying with LoadArea and factors
- 

### LineLoad
A distributed load along a line.
- Einheit: kN/m
- Erzeugt durch direkte Eingabe
- Erzeugt durch Flächenlast multipliziert mit Lasteinzugsbreite und Faktor

### AreaLoad
A distributed load over an area.
- Einheit: kN/m²

### Slab
A structural element representing a horizontal plate.
- Ständige Lasten: Eigengewicht (z.B. automatisch ermittelt), Sonstige (z.B. Aufbau)
- Veränderliche Lasten: Nutzlast (z.B. Wohnen)

### Wall
A structural element representing a vertikal wall.
- Usually width of 1 Meter
- 


### Load Transfer
The explicit routing of loads through structural elements.