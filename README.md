# Chatbot RASA gestione appuntamenti
Chatbot sviluppato utilizzando il framework [RASA](https://rasa.com/) per la gestione degli appuntamenti.

In questa repository lo sviluppo del bot si concentra nello use case dei parrucchieri.

**Nota:** *Per runnare il bot occorre avere almeno rasa 3.0.0 (3.1.0 raccomandato). Dirigersi nella cartella contenente il file **config.yml** e digitare:*
```shell
rasa train; rasa shell
```

## Features principali
- Conversazione,
- Bot Challenge,
- Connessione a database e scheduling appuntamenti,

### Path di conversazione principali:
- [] Richiesta appuntamento no giorno
  - intent: saluto (opzionale)
  - action: saluto
  - intent: richiesta appuntamento generico
  - action: per cosa? (taglio, shampoo, barba, shampo + taglio, ...)
  - intent: selezione prestazione (**per cosa?** ritorna dei bottoni)
  - action: ricerca primo spazio disponibile (a seconda delle tempistiche previste per il soddisfacimento della prestazione si cerca all'interno del calendario le *n* disponibilità e si ritornano come bottoni. **Prevedere anche un bottone per nessuna che triggera di nuovo la ricerca.**).
  - intent: selezione appuntamento
  - action_form: ok, nome e cognome?
  - intent: fill form
  - action: registrazione appuntamento e feedback.
  - intent: goodbye
  - action: goodbye

- [] Richiesta appuntamento con giorno
  - intent: saluto (opzionale)
  - action: saluto
  - intent: richiesta appuntamento [giorno]
  - path come sopra ma filtraggio per giorno

- [] Modificare appuntamento
  - intent: saluto (opzionale)
  - action: saluto
  - intent: richiesta modifica appunamento
  - action: chiedi nominativo (form)
  - intent: inserisci nominativo (form fill)
  - action: cerca appuntamenti e mostra + modifica o elimina?
  - intent: sceglie cosa fare
  - action: fa quello che chiede l'utente

- [x] Bot challenge
  - intent: sei un bot?
  - action: dipende, sai cos'è il test di turing? (torna bottoni, si, no).
  - intent: si
    - action: allora si, sono un bot.
  - inent: no
    - action: no, non sono un bot.
