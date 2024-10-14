# Rozbehnutie projektu

## Krok 1: Naklonovanie repozitara
```
git clone https://github.com/xmi74/IIS.git
```


## Krok 2: Vytvorenie virtualneho prostredia
```
pyhon3 -m venv venv
```

## Krok 3: Aktivacia virtualneho prostredia (Linux/macOS)
```
source venv/bin/activate
```

## Krok 4: Instalacia rozsireni
```
pip install -r requirements.txt
```

## Krok 5: Spustenie projektu

### Pred spustenim:
Vytvorenie databazy pouzitim skriptu create_db
```
python3 create_db.py
```

### Samotne spustenie:
```
python3 app.py
```

### Mazanie dat (tabuliek) z databazy:
skript reset_data.py
```
python3 reset_data.py
```
