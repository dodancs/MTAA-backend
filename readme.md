# MTAA: Čili Cat - back-end

[Front-end](https://github.com/dodancs/MTAA-frontend)

## Špecifikácia API rozhrania
- [Dátový model](data-model.png)
- [SQL schémy](schema/)
- [API Dokumentácia](API.md)
- [API Dokumentácia [PDF]](API.pdf)

## Moduly

- [Autentifikácia](module_auth.py)
- [Nastavenia](module_settings.py)





## Spustenie programu

Pred spustením je potrebné nainštalovať Python 3.7 spolu s manažérom balíkov (pip).

Stiahnite zdrojový kód projektu, alebo ho naklonujte:

```bash
$ git clone git@github.com:dodancs/MTAA-backend.git
```

Pomocou manažéra balíkov Pythonu nainštalujte potrebné balíky:

```bash
$ cd ./MTAA-backend
$ pip install -r ./requirements.txt
```

Teraz vytvorte [konfiguračný súbor](config.example.json) s nastavením backendu:

```bash
$ cp ./config.example.json config.json
$ nano ./config.json
```

Po importovaní [SQL schémy](schema/) do databázy môžete server spustiť:

```bash
$ python ./server.py
```

