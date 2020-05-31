# Gebruiken

## Accounts
Om accounts aan te maken ga je naar de "gebruikers" pagina bij tools. Accounts kun je rollen toekennen zodat niet iedereen alles kan doen. Iedereen die een account heeft kan aan de muilgraaf.

### Rollen
* "tools": nodig om aan de tools te kunnen
* "gebruikers": nodig om gebruikers te zien en aan te passen, personen met deze rol kunnen zichzelf dus alle andere rollen geven in theorie
* "schachten": om schachtenopdrachten te maken en aan schachten toe te kennen
* "penning": om het poef overzicht te kunnen bekijken en aanpassingen te doen aan personen hun poef/bar transacties die op de poef gezet zijn te verwijderen.
* "poef": om dingen op de poef te kunnen (laten) zetten.
* "stemmingen": om het stem overzicht te kunnen bekijken en aanpassingen aan te doen.

Bij het bewerken van je een rol moet die persoon uitloggen en dan terug inloggen om de verandering te hebben.

## Statuten aanpassen
Om de statuten aan te passen zet je de nieuwe pdf file met de statuten in de map "static" met de naam "statuten.pdf".

## Augustjes uploaden
Om een augustje te uploaden ga je naar de tools sectie van de site. Bij Augustjes kun je op "nieuw" klikken. Bij embed code moet de embed code die je op yumpu kan vinden.

# Andere aanpassen
In de map "vermeylen" en daarin de map "templates" kun je de html voor de website vinden. Daarin kun je aanpassen wat veranderd moet worden aan hoe de website eruit ziet.

# Technische details

## Backend
De backend is geschreven in flask 1.1.1

Alle python requirements staan in requirements.py

## Frontend
De frontend bestaat voornamelijk uit HTML templates die via flask gereturned worden. Voor styling (css) is Bootstrap 4.3 gebruikt. Voor icons Fontawesome 5.3.1. Sommige delen gebruiken wat Vue (versie 2.6.10).

## Database
Om juist geencrypteerde wachtwoorden met de hand te genereren: https://bcrypt-generator.com/ 

### Stemmingen
* Wanneer een stemming verwijderd wordt worden alle opties en stemmen die eraan verbonden waren ook verwijderd.
* Wanneer een optie voor een stemming verwijderd wordt worden alle stemmen die eraan verbonden waren ook verwijderd.
* Wanneer een login voor de stemmingen verwijderd wordt worden alle stemmen met die login gedaan ook verwijderd.
* Er kan maar 1 keer per login op een bepaalde optie gestemd worden. Als er voor een stemming meerdere keren per persoon gestemd zou kunnen worden dan moeten die stemmen dus op verschillende opties gebeuren.

### Schachten
* Wanneer een schacht verwijderd wordt zal hij ook uit de lijst van schachten die meegeholpen heeft aan een opdracht verwijderd worden.
* Wanneer een opdracht verwijderd wordt zal die ook bij alle schachten verdwijnen in de lijst van opdrachten die ze gedaan hebben.
