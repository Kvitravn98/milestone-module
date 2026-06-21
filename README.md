# Milestones Module

## 1. Descrizione del modulo

`milestones_module` è un modulo custom per Odoo 18 che estende il modulo standard `Project`.

Il modulo aggiunge funzionalità per la gestione avanzata delle milestone di progetto, l’assegnazione dei task alle milestone, la gestione dei membri del team con ruolo progettuale, la visualizzazione dell’avanzamento del progetto e l’import/export dei dati principali tramite file CSV.

L’obiettivo del modulo è fornire un’estensione leggera e integrata del Project Management standard di Odoo, riutilizzando dove possibile i modelli nativi esistenti e aggiungendo solo le entità custom necessarie.

---

## 2. Istruzioni per l’installazione dell’ambiente

### 2.1 Requisiti generali

Prima di installare il modulo è necessario avere un ambiente Odoo 18 funzionante.

Requisiti principali:

* Python 3.10+
* PostgreSQL 14+
* Git
* Odoo 18
* Ambiente virtuale Python
* `wkhtmltopdf`, necessario per la generazione dei report PDF

---

### 2.2 Installazione ambiente su Windows

#### 2.2.1 Installare PostgreSQL

Installare PostgreSQL e creare un utente dedicato a Odoo.

Su Powershell, lanciare il comando psql e lanciare le seguenti query:

```sql
CREATE USER odoo WITH PASSWORD 'your_password';
ALTER USER odoo CREATEDB;
```

#### 2.2.2 Clonare Odoo

```powershell
cd *your_odoo_directory*
git clone https://github.com/odoo/odoo.git --branch 18.0 --depth 1 *your_directory*
cd *your_directory*
```

#### 2.2.3 Creare e attivare il virtual environment

```powershell
python -m venv venv
.\venv\Scripts\activate
```

#### 2.2.4 Installare le dipendenze Python

```powershell
pip install -r requirements.txt
```

#### 2.2.5 Creare la cartella per i moduli custom

```powershell
mkdir custom_addons
```

La struttura sarà simile a:

```text
*your_directory*/
├── addons/
├── custom_addons/
│   └── milestones_module/
├── odoo/
├── odoo-bin
└── odoo.conf
```

#### 2.2.6 Configurare Odoo

Creare o aggiornare il file `odoo.conf`.

Esempio:

```ini
[options]
admin_passwd = mypassword
db_host = localhost
db_port = 5432
db_user = odoo
db_password = your_password
addons_path = *your_folder*\addons,*your_folder*\custom_addons
xmlrpc_port = 8018
```

#### 2.2.7 Installare wkhtmltopdf

Per generare correttamente i report PDF è necessario installare `wkhtmltopdf`.

Dopo l’installazione, aggiungere il percorso dell’eseguibile al `PATH` di Windows oppure indicarlo nel file `odoo.conf`.

Esempio:

```ini
bin_path = C:\Program Files\wkhtmltopdf\bin
```

---

### 2.3 Installazione ambiente su Linux

#### 2.3.1 Installare dipendenze di sistema

Esempio su distribuzioni Debian/Ubuntu:

```bash
sudo apt update
sudo apt install git python3 python3-venv python3-pip postgresql postgresql-client wkhtmltopdf
```

#### 2.3.2 Configurare PostgreSQL

```bash
sudo -u postgres createuser -s odoo
sudo -u postgres psql
```

Dentro PostgreSQL:

```sql
ALTER USER odoo WITH PASSWORD 'your_password';
\q
```

#### 2.3.3 Clonare Odoo

```bash
cd *your_odoo_folder*
git clone https://github.com/odoo/odoo.git --branch 18.0 --depth 1 *your_folder*
cd *your_folder*
```

#### 2.3.4 Creare e attivare il virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 2.3.5 Installare le dipendenze Python

```bash
pip install -r requirements.txt
```

#### 2.3.6 Creare la cartella per i moduli custom

```bash
mkdir custom_addons
```

#### 2.3.7 Configurare Odoo

Creare o aggiornare il file `odoo.conf`.

Esempio:

```ini
[options]
admin_passwd = mypassword
db_host = localhost
db_port = 5432
db_user = odoo
db_password = *your_password*
addons_path = *your_folder*/addons,*your_folder*/odoo18/custom_addons
xmlrpc_port = 8018
```

---

## 3. Istruzioni per l’installazione del modulo

### 3.1 Copiare il modulo

Copiare la cartella `milestones_module` dentro la directory `custom_addons`.

```

### 3.2 Verificare `addons_path`

Assicurarsi che il file `odoo.conf` includa sia gli addons standard di Odoo sia la cartella dei moduli custom.

Esempio:

```ini
addons_path = /path/to/odoo/addons,/path/to/odoo/custom_addons
```

### 3.3 Avviare Odoo

Windows:

```powershell
python .\odoo-bin -c .\odoo.conf -d nome_database
```

Linux:

```bash
python ./odoo-bin -c ./odoo.conf -d nome_database
```

### 3.4 Aggiornare la lista applicazioni

Da interfaccia Odoo:

1. Attivare la modalità sviluppatore
2. Andare su `Apps`
3. Cliccare su `Update Apps List`
4. Cercare `Milestones Module`
5. Installare il modulo

### 3.5 Aggiornare il modulo dopo modifiche

Durante lo sviluppo, dopo modifiche al codice o alle view, aggiornare il modulo con:

Windows:

```powershell
python .\odoo-bin -c .\odoo.conf -d nome_database -u milestones_module --stop-after-init
```

Linux:

```bash
python ./odoo-bin -c ./odoo.conf -d nome_database -u milestones_module --stop-after-init
```

Dopo l’aggiornamento, riavviare Odoo normalmente.

---

## 4. Descrizione delle funzionalità implementate

### 4.1 Gestione milestone

Il modulo estende il modello standard `project.milestone`.

Funzionalità implementate:

* aggiunta del campo `deadline`
* aggiunta del campo `state`
* stati disponibili:

  * `todo`
  * `in_progress`
  * `done`
* conteggio dei task assegnati alla milestone
* vincolo di unicità del nome milestone all’interno dello stesso progetto
* viste dedicate per lista, form e ricerca milestone
* filtri di ricerca per stato e deadline

---

### 4.2 Associazione task a milestone

Il modulo utilizza il campo standard `milestone_id` presente su `project.task`.

Funzionalità implementate:

* visualizzazione dei task assegnati a una milestone
* wizard per assegnare task esistenti a una milestone
* dominio sui task selezionabili, limitato ai task dello stesso progetto
* possibilità di rimuovere un task da una milestone
* validazione per impedire l’associazione di task e milestone appartenenti a progetti diversi

---

### 4.3 Gestione membri del team

È stato introdotto il modello custom `project.team.member`.

Ogni membro del team è collegato a:

* progetto
* utente Odoo
* ruolo progettuale
* stato attivo/non attivo

Ruoli disponibili:

* Team Lead
* Developer
* Tester
* Analyst

Funzionalità implementate:

* lista membri del team
* form di dettaglio membro team
* vincolo di unicità per evitare lo stesso utente duplicato nello stesso progetto
* calcolo dei task assegnati al membro tramite il campo standard `user_ids` di `project.task`
* visualizzazione del numero di task assegnati

---

### 4.4 Integrazione nella form progetto

La form del progetto è stata estesa con nuove sezioni dedicate.

Tab `Milestones`:

* riepilogo numero milestone
* numero milestone completate
* percentuale di avanzamento
* lista milestone del progetto

Tab `Team Allocation`:

* lista membri del team del progetto
* ruolo di ciascun membro
* numero di task assegnati

---

### 4.5 Calcolo avanzamento progetto

Il modulo calcola l’avanzamento del progetto in base alle milestone completate.

Campi custom aggiunti su `project.project`:

* numero totale milestone
* numero milestone completate
* percentuale di avanzamento milestone

La percentuale viene calcolata con la formula:

```text
milestone completate / milestone totali * 100
```

Se il progetto non ha milestone, l’avanzamento viene impostato a `0`.

---

### 4.6 Report PDF stato progetto

È stato implementato un report PDF dedicato al progetto.

Il report contiene:

* informazioni principali del progetto
* project manager
* cliente
* riepilogo milestone
* avanzamento percentuale
* elenco milestone
* task associati alle milestone
* membri del team
* allocazione task per membro

Il report è disponibile dalla form progetto tramite il menu di stampa/report.

Per la corretta generazione del PDF è necessario che `wkhtmltopdf` sia installato e correttamente configurato nell’ambiente.

---

### 4.7 Export CSV

È stato implementato un wizard per esportare i dati principali del progetto in formato CSV.

Il wizard permette di selezionare:

* progetto
* esportazione milestone
* esportazione task
* esportazione membri del team

Il CSV esportato utilizza una struttura unica basata sulla colonna `record_type`.

Tipi di riga esportati:

* `project_summary`
* `milestone`
* `task`
* `team_member`

Questa struttura permette di mantenere un singolo file CSV leggibile e facilmente riutilizzabile per successive operazioni di import.

Il file CSV viene generato tramite controller HTTP e scaricato direttamente dal browser.

---

### 4.8 Import CSV

È stato implementato un wizard per importare milestone e membri del team da file CSV.

Funzionalità implementate:

* selezione del progetto di destinazione
* upload file CSV
* selezione delle sezioni da importare:

  * milestone
  * membri del team
* limitazione dell’upload ai file `.csv`
* validazione degli header richiesti
* import sicuro dei dati
* riepilogo finale dell’import

Il sistema processa solo le righe con:

* `record_type = milestone`
* `record_type = team_member`

---

### 4.9 Strategia safe import

L’import non modifica record già esistenti.

Regole implementate:

* se una milestone con lo stesso nome esiste già nello stesso progetto, viene ignorata
* se un membro team con lo stesso utente esiste già nello stesso progetto, viene ignorato
* se un utente indicato nel CSV non esiste in Odoo, la riga viene ignorata
* se il ruolo del membro team non è valido, la riga viene ignorata
* se lo stato della milestone non è valido, la riga viene ignorata

Al termine dell’import viene mostrato un riepilogo con:

* milestone create
* milestone ignorate
* membri team creati
* membri team ignorati
* righe ignorate

---

### 4.10 Sicurezza e accessi

Sono stati configurati gli accessi tramite `ir.model.access.csv`.

Il modulo utilizza i gruppi standard del modulo Project:

* `project.group_project_user`
* `project.group_project_manager`

I Project Manager possono gestire i membri del team.

Gli utenti progetto possono accedere alle funzionalità operative previste, nel rispetto dei permessi standard Odoo.

---

### 4.11 Traduzioni

Il modulo include traduzioni italiane tramite file `i18n/it.po`.

Le stringhe custom del modulo possono quindi essere visualizzate in italiano quando la lingua utente è impostata su italiano.

---

## 5. Note e decisioni tecniche

### 5.1 Riutilizzo dei modelli standard Odoo

Il modulo riutilizza il più possibile i modelli standard di Odoo.

In particolare:

* le milestone estendono `project.milestone`
* i task restano su `project.task`
* l’associazione task-milestone usa il campo standard `milestone_id`
* l’assegnazione task agli utenti usa il campo standard `user_ids`

Questa scelta evita duplicazioni inutili e mantiene il modulo compatibile con il comportamento standard del Project Management di Odoo.

---

### 5.2 Modello custom per i membri del team

È stato creato il modello `project.team.member` invece di estendere modelli non pensati per questo scopo.

Il modello rappresenta il team operativo di progetto e permette di associare un ruolo specifico a ciascun utente.

Questa scelta separa chiaramente:

* assegnazione operativa dei task
* composizione del team di progetto
* ruolo del membro nel progetto

---

### 5.3 Nessuna ripartizione automatica delle ore per membro

Il modulo mostra i task assegnati ai membri del team, ma non calcola ore allocate per singolo membro.

Motivo tecnico:

`project.task.user_ids` indica gli utenti assegnati a un task, ma non definisce una ripartizione percentuale o oraria dell’effort tra gli assegnatari.

Per questo motivo il modulo mantiene le ore stimate sul task tramite `estimated_hours`, evitando calcoli arbitrari o potenzialmente fuorvianti.

---

### 5.4 CSV con colonna `record_type`

Per l’export è stato scelto un singolo CSV con colonna `record_type`, invece di generare file separati o sezioni multiple con header diversi.

Questa scelta permette di:

* mantenere un solo file di export
* distinguere chiaramente il tipo di dato rappresentato da ogni riga
* semplificare la logica di import
* rendere il formato più stabile e prevedibile

---

### 5.5 Nessun uso degli ID tecnici nel CSV

Il CSV non si basa sugli ID numerici del database.

Sono stati preferiti campi più leggibili e più portabili, come:

* nome progetto
* nome milestone
* login utente
* ruolo tecnico
* stato tecnico

Gli ID database possono cambiare tra ambienti diversi, mentre campi come il login utente sono più adatti per un formato di import/export.

---

### 5.6 Valori tecnici per stati e ruoli

Nel CSV vengono esportati i valori tecnici delle selection.

Per gli stati:

```text
todo
in_progress
done
```

Per i ruoli:

```text
team_lead
developer
tester
analyst
```

Questa scelta rende l’import indipendente dalla lingua dell’interfaccia utente.

---

### 5.7 Strategia di import sicura

L’import CSV segue una logica `create-only`: il wizard crea solo record non ancora presenti nel progetto selezionato.

Prima della creazione vengono eseguiti controlli di esistenza su:

- nome milestone all’interno del progetto
- utente già presente nel team del progetto

Le righe già presenti vengono ignorate e riportate nel riepilogo finale dell’import.

Questa scelta evita sovrascritture accidentali e rende l’import ripetibile sullo stesso file CSV.

---

### 5.8 Controller solo per export

Per l’export CSV è stato utilizzato un controller HTTP, perché il download di un file è gestito in modo più naturale tramite response HTTP.

Per l’import, invece, non è stato usato un controller: il wizard legge direttamente il file caricato e crea i record necessari.

Questa separazione mantiene più chiara la responsabilità dei componenti:

```text
Export: wizard → controller → download CSV
Import: wizard → parsing CSV → creazione record
```
