# Spustenie projektu

## Krok 1: Vytvorenie virtualneho prostredia
```
python3 -m venv venv
```

## Krok 2: Aktivacia virtualneho prostredia (Linux/macOS)
```
source venv/bin/activate
```

## Krok 3: Instalacia rozsireni
```
pip install -r requirements.txt
```

## Krok 4: Vytvorenie instancie databaze
```
python3 create_db.py
Enter your MySQL username: <root>
Enter your MySQL password: <your_password>
```

## Krok 5: Spustenie projektu
```
python3 app.py
Enter your MySQL username: <root>
Enter your MySQL password: <your_password>
```

