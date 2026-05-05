# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Comandos de desarrollo

### Backend (Django — puerto 8000)
```bash
cd PlanGo_backend
python manage.py runserver          # servidor de desarrollo
python manage.py migrate            # aplicar migraciones
python manage.py makemigrations     # crear migraciones
python manage.py test               # ejecutar tests
python manage.py dumpdata --indent 4 > initial_data.json   # exportar datos
python manage.py loaddata initial_data.json                 # importar datos
```

### Frontend (Angular — puerto 4200)
```bash
cd PlanGo_frontend
npm start        # ng serve
npm run build    # build de producción
npm test         # Karma test runner
```

## Arquitectura general

Aplicación fullstack de planificación de viajes:

- **Backend:** Django 5.2 + Django REST Framework, SQLite (desarrollo), Redis caché
- **Frontend:** Angular 17 (standalone components), Tailwind CSS, PrimeNG
- **Autenticación:** Firebase Admin SDK en backend; `@angular/fire` en frontend
- **Mapas:** Leaflet (reemplaza Google Maps JS)
- **Búsqueda de lugares:** Overpass API / OSM (reemplaza Google Places API) — ver `PlanGo_backend/apps/places/services/overpass_service.py`

## Flujo de autenticación

1. El usuario se autentica en Firebase desde Angular y obtiene un `idToken`
2. Angular almacena el token en `localStorage` con clave `authToken` (definido en `PlanGo_frontend/src/app/core/globals.ts`)
3. `BaseHttpService` adjunta el token como `Authorization: Bearer {idToken}` en cada petición
4. El middleware `FirebaseAuthenticationMiddleware` (`core/middleware/firebase_authentication.py`) verifica el token con Firebase Admin SDK antes de llegar a las vistas
5. Las vistas usan `@permission_classes([IsAuthenticated])` — la clase `FirebaseAuthentication` (`core/authentication.py`) es el backend de autenticación de DRF

Los CSRF tokens se obtienen del endpoint `/itineraries/csrf-token/` y se renuevan en `AppComponent.ngOnInit()`.

## Apps Django

Cada app sigue el mismo patrón: `models/` → `serializer.py` → `DTO/` → `views*.py` → `urls.py`.

| App | Responsabilidad |
|-----|----------------|
| `users` | Registro/login, modelo User (extiende AbstractUser con `firebase_uid`), Participants |
| `itineraries` | Itinerary y Destination; autocompletado de ciudades vía Geonames API |
| `places` | Accommodation, Activity, Restaurant, SavedPlace; búsqueda con Overpass API |
| `expenses` | Expense y UserExpense; cálculo de deudas entre participantes |

Las vistas usan `@api_view` (function-based), `@permission_classes([IsAuthenticated])` y `transaction.atomic` para operaciones de escritura.

## Patrón DTO

Las apps `places` e `itineraries` usan DTOs en `DTO/` para transformar datos entre la BD y la respuesta JSON. No usar serializers directamente para construir respuestas complejas — crear o actualizar el DTO correspondiente.

## Servicio Overpass (lugares)

`PlanGo_backend/apps/places/services/overpass_service.py` contiene:
- `map_category_to_osm_tags()` — mapea categorías del frontend a tags OSM
- `build_overpass_query()` — construye la query QL
- `search_nearby()` — llama a la API con fallback a mirrors alternativos si el servidor principal devuelve 504 o 429
- `parse_element()` — normaliza la respuesta OSM al formato que espera el frontend

La URL principal se configura con `OVERPASS_API_URL` en `.env`. Los mirrors de fallback están definidos en `OVERPASS_MIRRORS` dentro del mismo archivo.

## Variables de entorno (.env en la raíz del repo)

```
OVERPASS_API_URL          # URL del intérprete Overpass
PLAN_GO_API_PLACES_KEY    # Google Places API Key (legado, aún presente)
PLANG_GO_GEOCODES_KEY     # Geonames API Key
REDIS_HOST / REDIS_PORT / REDIS_DB / REDIS_USER / REDIS_PASSWORD
```

Firebase se configura con el archivo `PlanGo_backend/firebase-credentials.json` (no en git).

## Frontend — servicios y HTTP

- `BaseHttpService` (`core/services/base-http.service.ts`) — clase base con métodos GET/POST/PUT/PATCH/DELETE. Todos los servicios de feature heredan de ella.
- `globals.ts` — define `apiBaseUrl = 'http://localhost:8000'`; cambiar aquí para apuntar a otro entorno.
- El interceptor `auth.interceptor.ts` redirige a `/login` cuando el backend responde 401.
- Las rutas de la app están en `src/app/app.routes.ts`; todos los componentes son standalone.
