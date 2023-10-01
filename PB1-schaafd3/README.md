# Dokkie Python

# Opdracht blok 1 HBO-ICT BIM

<img src="hbo-ict-logo.png" width="175" height="175" alt="HBO-ICT-LOGO">

## Hoe is deze repository ingericht 🔠

- Bovenstaande broncode is een uitwerking van de Dokkie-opdracht voor BIM. Een aantal user stories uit de opdracht is hierin uitgewerkt. 
- In dit bestand (`readme.md`) vind je algemene informatie over de repository, zoals hoe je deze kunt gebruiken. Daaronder is informatie gerelateerd tot techniek te vinden 🛠.
- De Wiki, onder Plan in het menu, bevat alle inforamtie over het project.

## Techniek specifiek voor de BIM-opdacht

*Heb je al je coach toegevoegd aan je project op Gitlab?*

### Installatie algemeen

Volg de installatie handleiding die je in [deze plek in de repository](./docs/getting-started) vindt. Hij staat onder docs/getting-started en heeft de vorm van een .md bestand. Vragen? Stel ze elkaar, vraag pas de studentenmentor als je er niet uitkomt en als die niet beschikbaar is een docent.

### Eerste keer starten applicatie

*Je kunt de applicatie pas starten nadat je de installatie geheel hebt doorlopen!*

De applicatie Dokkie slaat gegevens op in een database. Die database moeten we starten voordat de applicatie is gestart. Volg daarom onderstaande stappen in deze volgorde.

1. Open een CMD terminal in Visual Studio Code. Let op: op Windows wordt er standaard een Powershell terminal geopend. Open de juiste door naast de plus te klikken en kies Command Prompt.
2. Controleer op de tekst daar begint met (.venv). Zo niet, dan heb je nog geen Python Virtuele omgeving geinstalleerd.
3. Kijk in de explorer links of je een directory 'instance' hebt. Zo niet, maak die aan.
4. Kopieer het bestand db.local.config naar de directory instance
5. Hernoem dit bestand naar db.config. Tip: dit is een standaard manier in Flask om instellingen te bewerken.
6. Start nu de database. Dit doen we met behulp van een zogenaamde container techniek: Docker. Ga in de terminal met het commando `cd db` naar de db directory. Geef daar het commando `docker compose up`. Je zult nu een download zien en daarna een lange lijst met opstart regels. Zie je dit niet, en wel een foutmelding? Doe de volgende stap, sla die anders over.
7. (Optioneel) Je kon de docker container niet openen met het commande `docker compose up`. Dit kan een aantal oorzaken hebben. Voorkomend zijn: - je zit niet in de juiste directory: geef dit commando in de db directory, alleen daar werkt het - je docker engine draait niet. Herstart docker desktop of de service (Mac) - je werkt niet met voldoende rechten. Windows 10+: open een Powershell met adminstrator rights. Ga naar de juiste directory met het `cd` commando. Voer daar nogmaals `docker compose up` uit.
8. Je database draait nu. Ga in de terminal een directory lager, met het commando `cd ..` (de 2 puntjes betekenen: 1 niveau terug).
9. Start je applicatie met het commando `flusk run`
10. Je ziet nu een URL (127.0.0.1:5000). Open die in je browser.
11. Probeer in je applicatie in te loggen met een gebruiker die je zelf hebt aangemaakt. Tip: hou alle terminals in de gaten. Zie je daar meldingen/fouten? Heel goed, dan zie je dat je applicatie bezig is. Lees ze goed door.
12. Begin nu met een User Story over documenteren OF HTML OF CSS. Zorg ervoor dat je met Git al je wijzigingen in je code opslaat.
13. Lees ook weer de WIKI...
14. Heb je al je coach toegevoegd aan je project hier op Gitlab?

### Technieken & tools 🛠

- HTML/CSS
- Package Manager:
    - Python
    - Flask
    - pyWhatKit (Versturen whatsapp messages) ("pip install pywhatkit" om deze los te installeren)
- Database
    - MariaDB lokaal beschikbaar via een docker container
    - Evt Oege mySQL
- Beschikbaar stellen als SAAS
    - Docker cloud oplossing op hva-fys.nl via CI/CE in Gitlab.
