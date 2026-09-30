# AeroPulse

Projekt edukacyjny i portfolio rozwijany w Pythonie. Docelowo będzie backendem do zarządzania flotą dronów oraz odbierania, przetwarzania i prezentowania ich telemetrii.

Projekt powstaje etapami jako modularny monolit. Obecna wersja obejmuje fundamenty aplikacji (Milestone 0): FastAPI, endpoint `/health`, konfigurację środowiskową, podstawowe logowanie, test oraz narzędzia kontroli jakości. Obsługa dronów, baza danych i telemetria są planowane w kolejnych etapach.

## Technologie obecnej wersji

- Python 3.13+ oraz FastAPI uruchamiane przez Uvicorn.
- Pydantic Settings do odczytu i walidacji konfiguracji.
- Standardowy moduł `logging` do logów aplikacji.
- pytest i FastAPI TestClient korzystający z httpx2 do testowania API.
- Ruff, mypy i pre-commit do kontroli jakości kodu.

## Przygotowanie środowiska

Poniższe polecenia są przeznaczone dla Linux/Bash. Wykonuj je w katalogu głównym repozytorium. Potrzebujesz Git oraz Pythona w wersji co najmniej 3.13 z obsługą `venv` i `pip`.

Sprawdź wersję interpretera, a następnie utwórz i aktywuj środowisko:

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
```

Jeżeli `python3` wskazuje wersję starszą niż 3.13, użyj do utworzenia środowiska dostępnego interpretera 3.13 lub nowszego.

Zainstaluj projekt w trybie edytowalnym wraz z narzędziami deweloperskimi:

```bash
python -m pip install -e ".[dev]"
```

Tryb edytowalny pozwala korzystać ze zmian kodu bez ponownej instalacji projektu. Po zmianie zależności w `pyproject.toml` ponów powyższe polecenie. Zestaw `dev` zawiera narzędzia testowe i kontrole jakości; do samego uruchamiania aplikacji wystarcza `python -m pip install -e .`.

Przy pierwszym uruchomieniu utwórz lokalną konfigurację, kopiując przykład. Jeśli masz już własny `.env`, zachowaj jego ustawienia:

```bash
cp .env.example .env
```

## Konfiguracja

| Zmienna | Wartość domyślna w kodzie | Znaczenie |
|---|---|---|
| `AEROPULSE_APP_NAME` | `AeroPulse` | Tytuł API widoczny w dokumentacji. |
| `AEROPULSE_DEBUG` | `false` | Włącza diagnostyczne odpowiedzi przy nieobsłużonych błędach. |

Plik `.env.example` ustawia nazwę `AeroPulse Local` i pozostawia debug wyłączony. `.env` jest ignorowany przez Git; `.env.example` dokumentuje ustawienia i powinien zawierać wyłącznie bezpieczne wartości przykładowe.

W standardowym uruchomieniu ustawienia są wybierane w kolejności: zmienne środowiskowe procesu, wartości z `.env`, wartości domyślne w klasie `Settings`. Nazwy zmiennych są dopasowywane bez rozróżniania wielkości liter, a wartości są konwertowane i walidowane przez Pydantic.

Ścieżka `.env` jest względna wobec katalogu uruchomienia. Ustawienia są odczytywane przy tworzeniu obiektu `Settings` podczas importu `app.main`. Po zmianie `.env` zrestartuj aplikację. Tryb debug pozostaw wyłączony na publicznym serwerze; nie jest on odpowiednikiem opcji `--reload`.

## Uruchomienie API

W aktywnym środowisku, z katalogu głównego repozytorium:

```bash
python -m uvicorn app.main:app --reload
```

Opcja `--reload` służy do lokalnej pracy i przeładowuje aplikację po zmianach kodu. Serwer zatrzymasz przez `Ctrl+C`.

- API: <http://127.0.0.1:8000>
- Swagger UI: <http://127.0.0.1:8000/docs>
- Schemat OpenAPI: <http://127.0.0.1:8000/openapi.json>

Sprawdź endpoint w drugim terminalu:

```bash
curl -i http://127.0.0.1:8000/health
```

Oczekiwana odpowiedź to HTTP `200 OK` z treścią:

```json
{"status": "ok"}
```

`/health` potwierdza, że aplikacja odpowiada; nie sprawdza zewnętrznych usług. Ścieżki `/` oraz `/favicon.ico` nie są zdefiniowane i zwracają `404`.

Logi aplikacji trafiają do terminala i zawierają czas, poziom, nazwę modułu oraz komunikat. Próg logowania wynosi `INFO`.

## Testy i kontrola jakości

```bash
python -m pytest -v
python -m ruff check .
python -m ruff format --check .
python -m mypy app tests
```

Test sprawdza status HTTP i JSON zwracany przez `/health`. Korzysta z `TestClient`, więc osobne uruchomienie Uvicorn nie jest potrzebne.

Ruff sprawdza kod i formatowanie, a mypy analizuje zgodność typów. Kontrole nie zastępują testowania zachowania aplikacji.

Aby zapisać automatyczne poprawki importów i formatowania:

```bash
python -m ruff check --select I --fix app tests
python -m ruff format app tests
```

## Pre-commit

Po przygotowaniu środowiska zainstaluj lokalny hook Git:

```bash
python -m pre_commit install
```

Obecna konfiguracja uruchamia wyłącznie `ruff check` dla przygotowanych do commita plików Pythona. Błąd kontroli zatrzymuje commit. Hook korzysta z narzędzi dostępnych w środowisku, dlatego przed commitowaniem aktywuj `.venv`. Instalację hooka należy powtórzyć w nowej kopii repozytorium.

Ręczne sprawdzenie wszystkich plików śledzonych przez Git:

```bash
python -m pre_commit run --all-files
```

Nowe, jeszcze nieśledzone pliki możesz wskazać jawnie:

```bash
python -m pre_commit run --files app/main.py app/config.py app/logging_config.py tests/test_health.py
```

pytest, mypy i kontrolę formatowania uruchamiaj osobno komendami z poprzedniej sekcji.

## Struktura projektu

```text
app/
    __init__.py          # Pakiet aplikacji.
    main.py              # Obiekt FastAPI, konfiguracja aplikacji i /health.
    config.py            # Odczyt i walidacja ustawień.
    logging_config.py    # Konfiguracja logowania.
tests/
    test_health.py      # Test odpowiedzi /health.
pyproject.toml          # Metadane, zależności, ustawienia Ruff i mypy.
.pre-commit-config.yaml # Definicja hooka kontroli kodu.
.env.example            # Przykładowe ustawienia lokalne.
.gitignore              # Wykluczenia środowiska i plików generowanych.
```

## Następny etap

Milestone 1 obejmuje PostgreSQL, SQLAlchemy 2, migracje Alembic, modele użytkowników i dronów, endpointy CRUD oraz testy integracyjne. Kolejne technologie będą dodawane wraz z uzasadniającymi je funkcjonalnościami.
