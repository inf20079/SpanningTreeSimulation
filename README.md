# SpanningTreeSimulation
Aufgabe des Netztechnik Labors in 2021/2022. Ziel ist einen Spanning Tree Algorithmus auf Layer 2 zu implementieren.

### Aufbau der Simulation
Für jede komponente des Netzwerks wurde ein Objekttyp erstellt. Für jeden Knoten des Netzwerks ist ein Thread vorgesehen. Diese kommunizieren über definierte Links. Dabei findet die Kommunikation über Listen statt. Wo die beiden beteiligten Threads ihre "gesendeten" Messages speichern und die "empfangenen" Nachrichten abrufen. Der Link stellt dabei ein shared media (zwischen Threads) dar und wird über ein Semaphor abgesichert.

### Eingabe- und Ausgabeformat
**Eingabeformat**

Die Eingabe findet über folgendes definiertes Format in form einer Textdatei statt. Die Datei hat folgenden Aufbau. Gestartet wird mit folgendem:
```
Graph mygraph {
```
Anschließend werden die Nodes definiert: Bezeichnung = ID;. Hier ein paar Beispiele:
```
    // Node-IDs
     A = 5;
     B = 1;
     C = 3;
     D = 7;
     E = 6;
     F = 4;
```
Folgend werden die Links folgendermaßen definiert: KnotenA - KnotenB : Kosten;. Beispiele:
```
    // Links und zugeh. Kosten
     A - B : 10;
     A - C : 10;
     B - D : 15;
     B - E : 10;
     C - D : 3;
     C - E : 10;
     D - E : 2;
     D - F : 10;
     E - F : 2;
}
```
Abgeschlossen mit '}'.

**Ausgabeformat**

Der Spanning Tree wird folgendermaßen ausgegeben: 
```
Spanning-Tree of mygraph {
    Root: B;
     A - B;
     C - D;
     D - E;
     E - B;
     F - E;
}
```
Der Root wird mit Root gekennzeichnet, die nächsten Hops von den Knoten immer so: Knoten - Hop;.

**Benutzung**
<br>Benötigt:
- Python
- pip

1. In Verzeichnis navigieren und requirements (tabulate zur darstellung des spanning trees) installieren.
```
pip install -r requirements.txt
```
2. Aufrufen des Skripts (-help für Argumente). Argumente:
- "-f", "--filepath": Path to the .txt file that contains the Network specifications (default=./Inputdateien/graph.txt).
- "-amsg", "--waitformsg": Amount of empty messages before stopping (default=5).
- "-t", "--showtraffic": Shows every interaction. Slows down routing process (default=False).
- "-mit", "--maxitems": Max amount of items (default=50).
- "-mco", "--maxcost": Max cost (default=50).
- "-mid", "--maxid": Max ID (default=50).