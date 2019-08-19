# Vermeylen site

Alle python requirements staan in requirements.py

## Backend
De backend is geschreven in flask 1.1.1

## Frontend
De frontend bestaat voornamelijk uit HTML templates die via flask gereturned worden. Voor styling (css) is Bootstrap 4.3 gebruikt.

Sommige delen gebruiken wat Vue (versie 2.6.10).

## Database
De database is postgresql. Kan geinstalleerd worden via de officiële site.

### Uitleg many to many relationship
https://www.youtube.com/watch?v=OvhoYbjtiKc

## Icons
Fontawesome 5.3.1

## Rollen
* iedereen die ingelogd is kan aan de muilgraaf
* de "poef" rol zorgt ervoor dat iemand dingen op de poef kan zetten
* de "penning" rol zorgt dat je bar transacties die via de poef geregeld zijn kan ongedaan maken

Bij het bewerken van je een rol moet die persoon uitloggen en dan terug inloggen om de verandering te hebben.