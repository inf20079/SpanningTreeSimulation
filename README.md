# SpanningTreeSimulation
Aufgabe des Netztechnik Labors in 2021/2022. Ziel ist einen Spanning Tree Algorithmus auf Layer 2 zu implementieren.

### Aufbau der Simulation
Für jede komponente des Netzwerks wurde ein Objekttyp erstellt. Für jeden Knoten des Netzwerks ist ein Thread vorgesehen. Diese kommunizieren über definierte Links. Dabei findet die Kommunikation über Listen statt. Wo die beiden beteiligten Threads ihre "gesendeten" Messages speichern und die "empfangenen" Nachrichten abrufen. So besteht eine bidirektionale halbduplex Verbindung zwischen den Knoten.

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