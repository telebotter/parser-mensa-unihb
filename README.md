# parser-mensa-unihb
Ein kleines Script um Infos von den Studentenwerk Webseiten der Uni Mensen in Bremen auszulesen. In die Wege geleitet, da openmensa.org zum Start 2018 keinen funktionierenden parser am laufen hat.

**ACHTUNG** Das nächstemal oder wenn mal zeit ist, vlt einfach darauf aufbauen,
statt den karm selbst zu schreiben, vorallem die xml formatierung ist warsch
einfacher:
https://pyopenmensa.readthedocs.io/en/latest/

# OpenMensaOrg Integration
Das Konzept von OpenMensa ist einfach, die parser sind komplett ausgelagert und
werden vom jeweiligen Entwickler des parsers bereitgestellt. Das heißt, wenn
man den Parser sinnvoll einsetzen möchte sollte er gut erreichbar auf einem
Server liegen.

Registriert man sich als Entwickler auf der OpenMensa.org Seite, kann man dort
unter Angabe einer (oder mehrere für weitere zwecke) URL einen Parser
registrieren. Die OMO-Datenbank fragt diesen Link um Mitternacht (bzw.
stündlich) ab und erwartet ein bestimmtes xml layout der Daten (siehe
example.xml)

Da es über github mit dem ausführbaren code etwas schwierig zu werden droht,
würde ich das script auf dem server ablegen, sobald der xml output gegeben ist
(hab jetzt leider auf json gesetzt bevor ich das gelesen habe) und es dann
unter sarbot.de/telebotter/parser/201 erreichbar machen.


Nurnoch die daten in son xml template verpacken und dann als django mini app
aufn server packen und url eintragen.. sollte übermorgen spätestens wieder
laufen (also zu beginn der nächsten woche) 

