# structural_loads

This is a package for civil engineers.
The goal is to implement the model of a loadpath engineers have in their mind.

Ziel von `structural_loads` ist das Gedankenmodell nachzubilden mit welchem Ingenieure bei der Lastpfadberechnung arbeiten, um die Parameter wie Einheitslasten (kN/m²), Lasteinzugsflächen und Lastweitergabe zu berechnen und dokumentieren.

## Lastdefinition
### Einwirkungstyp
Die Definition einer Einwirkung erfolgt zunächst über die zeitliche Dauer (ActionType):
- Ständig (Permanent) - G
- Veränderlich (Variable) - Q
- Außergewöhnlich (Accidental) - A

### Einwirkungskategorie
Für Permanent: Eigengewicht, Ständige Last
Für Variable: QA-Wohnen, QB-Büro, ...QS-Schnee, W-Wind 
Für Accidental: Anprall
 
### Lastarten
- Flächenlast [kN/m²]
- Lininelast [kN/m]
- Einzellast [kN]

## Lastzusammenstellung für Einzelbauteile
### Lasteinzugsbreite / -fläche
Die Lastdefinition für Bauteile (Dach, Decke, Wand) erfolgt mittels Flächenlasten (auch Einheitslast) in kN/m².
Daraus können Linienlasten durch Multiplikation mit einer Lasteinzugsfläche in Kombination mit Faktoren für die Durchlaufwirkung gebildet werden.
Ebenso können Linienlasten durch Multiplikation mit einer Lasteinzugsbreite in Kombination mit Faktoren für die Durchlaufwirkung gebildet werden.
Ebenso können Lastsummen für gesamte Flächen zur Kontrolle gebildet werden.

### Lastzusammenstellung
Für Balken, Wände oder Stützen ist es oft sinnvoll die einwirkenden Lasten separat ausserhalb einer Bemessungssoftware zusammenzustellen. So kann die Herkunft und Ermittlung nachvollziehbar dokumentiert werden. 

## Lastberechnung für einen vordefinierten Lastpfad


