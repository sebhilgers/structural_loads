# Glossary  

## Core Concepts

### Einwirkung (class ActionDefinition)
Classification of an action type (permanent, variable, accidental).
(Einwirkung bzw. Einwirkungsart (Kriterium ist zeitliche Veränderung): Ständig (G), Veränderlich (Q), Außergewöhnlich (A).)

#### LoadType
Unterkategorien einer Einwirkung (Einwirkungskategorien):

| Einwirkungstyp               | (Einwirkungs-)Kategorie                                                                                 |
| ---------------------------- | ------------------------------------------------------------------------------------------------------- |
| Ständig (permanent)          | Eigengewicht, Sonstige (z.B. Bodenaufbau)                                                               |
| Veränderlich (variable)      | Nutzlasten (Qn):, z.B. Wohnen (A), Büro (B), Versammlungsräume (C), Verkaufsräume (D), Lagerräume (E))  |
|                              | Verkehrslasten (Qv): F, G, H                                                                            |
|                              | Schnee (Qs): Orte bis 1000m, Orte ueber 1000m                                                           |
|                              | Wind (Qw)                                                                                               |
|                              | Sonstige (Q)                                                                                            |
|                              | Jede Kategorie mit Kombinationsbeiwert: psi_0, psi_1, psi_2                                             |
|                              | Jede Kategorie mit Lasteinwirkungsdauer: ständig, lang, mittel, kurz, sehr_kurz                         |
| Außergewöhnlich (accidental) | Anprall, Others; Dynamic; Static; Temperature; Wind; Snow; Maintenance; Fire; Moving; Seismic; Standard |

### LoadCase
Identifies a calculation case and must always be preserved. Groups loads from the same action source (e.g. Wind).
Parameter: name (str z.B. LC1), category (ActionCategory), description (optional)


### LoadGroup
Groups related loads for organizational purposes.
Defines how the individual load cases may be combined together if inserted into a load case combination. Relation: Exclusive, Together

### LoadCombination
Lastkombination bildet Bemessungskombinationen nach bestimmten Mustern durch Kombination der Lastfälle unter Berücksichtigung der Bedingungen in LoadGroups und Teilsicherheits- und Kombinationsbeiwerten

### Last (class Load) 
- Basisklasse für **Lastarten**: Flächenlast (AreaLoad), Linienlast (LineLoad), Einzellast (PointLoad)
- Parameter: name (str), loadcase (LoadCase), value (float), unit (kN/m², kN/m, kN)
### PointLoad
A concentrated load at a specific location (in node/on beam).
- Einheit: kN- 
- Erzeugt durch direkte Eingabe
- Created as product of AreaLoad with LoadArea and factors

### LineLoad
A distributed load along a line.
- Einheit: kN/m
- Erzeugt durch direkte Eingabe
- Erzeugt als Produkt aus Flächenlast und Lasteinzugsbreite und Faktor
- Erzeugt als Produkt aus Lininelast und Lastlänge
### AreaLoad
A distributed load over an area.
- Einheit: kN/m²

### TributaryArea / Lasteinzugsflächen
Eine Lasteinzugsfläche wird zur vereinfachten Lastermittlung anstelle von Ermittlung der Auflagerlasten an realen Bauteilen wie Balken oder Decken verwendet. Anhand von ein- oder zweiachsigem Lasteinzug und multiplikation mit Faktoren wird eine Durchlaufwirkung von Mehrfeldsystemen angenähert.
- Kann ein 1-Meter-Streifen mit Lasteinzugsbreite x Faktor sein
- Kann eine Lasteinzugsfläche mit Lasteinzugsbreiten in x-/y-Richtung x Faktor für x-/y-Richtung sein 

### Slab
A structural element representing a horizontal plate.
- Ständige Lasten: Eigengewicht (z.B. automatisch ermittelt), Sonstige (z.B. Aufbau)
- Veränderliche Lasten: Nutzlast (z.B. Wohnen)

### Wall
A structural element representing a vertikal wall.
- Usually width of 1 Meter for calculation
- Einheit: kN/m
### Column
A structural element representing a vertikal column.
- Belastung durch vertikale Einzellasten oder Linienlasten entlang des Stabes
- Einheit: kN
### Load Transfer
The explicit routing of loads through structural elements. Should store the origin of loads in the previuous step and show the calculation (e.g. areaload.gk * A_1=10m² * 1.1 * 1.1)
