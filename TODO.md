# TODO — Autenticação (JWT + Sessões)

> Plano ordenado por etapas. Cada etapa valida (importar/rodar) ao final.
> Base: projeto FastAPI + SQLAlchemy async + Alembic.

## Status geral

| Etapa | Descrição | Status |
|-------|-----------|--------|
| 0 | Pré-requisito: dependência JWT + lock | ✅ Feito |
| 1 | Settings do JWT / cookie / CORS | ✅ Feito |
| 2 | Model de sessão `Sessoes` | ⚠️ Em andamento |
| 3 | Migration `0004` (tabela de sessões) | ⚠️ Em andamento |
| 4 | Segurança PyJWT (`create_access_token` / `decode_token` / session token) | ⬜ Pendente |
| 5 | Schemas de auth (`schemas/auth.py`) | ⬜ Pendente |
| 6 | Dependência `JWTBearer` + `get_current_user` / `get_current_session` | ⬜ Pendente |
| 7 | Rotas de auth (`routes/auth.py`): login / refresh / logout | ⬜ Pendente |
| 8 | Ligar na app (`main.py`): router + CORS | ⬜ Pendente |
| 9 | Documentar env (`.env-example`) | ⬜ Pendente |

---

## Etapa 0 — Pré-requisito ✅
- `pyproject.toml` → `dependencies`: `"pyjwt>=2.13.0"` (instalado, `jwt` presente no venv).
- `uv lock && uv sync` executado.

## Etapa 1 — Settings ✅
`src/settings.py` já contém:
- `jwt_access_token_expire_minutes: int = 30`
- `jwt_refresh_token_expire_days: int = 30`
- `cors_origins: str = ""` (CSV)
- `cookie_secure: bool = False`
- `cookie_samesite: str = "lax"`
- `is_dev` → `environment in ("dev", "local") or startswith("dev-")`
- `use_secure_cookie` → `cookie_secure and not is_dev`

## Etapa 2 — Model `Sessoes` ⚠️
`src/database/models.py`:
- `Sessoes(CommonBase)` já existe.
- Pendência: **adicionar `index=True` em `id_usuario`** (hoje sem índice).
- Relação `Usuarios.sessoes` ↔ `Sessoes.usuario` já criada (back_populates simétrico).
- Campos: `id_sessao` (PK), `id_usuario` FK, `token_hash String(64) unique`, `expira_em`, `ultimo_uso`, `revogado`, `ip_origem String(45)`, `user_agent String(255)`.

## Etapa 3 — Migration `0004` ⚠️
`alembic/versions/0004_criando_tabela_de_sessoes.py` existe.
- Pendência: incluir **índice em `id_usuario`** (conferir alinhamento com o model).
- Revisar: `server_default` de `ativo/excluido/data_criacao`, FK, unique em `token_hash`, downgrade simétrico.
- Após ajuste: `alembic upgrade head` para aplicar.

## Etapa 4 — Segurança PyJWT ⬜
`src/utils/security.py` — implementar (hoje apenas stubs `pass`):
- `create_access_token(sub, claims=None, expires_minutes=None)` → `jwt.encode({...}, secret, algorithm)`.
- `decode_token(token)` → `jwt.decode(...)`; tratar `jwt.ExpiredSignatureError` → HTTPException 401 (`WWW-Authenticate: Bearer error='token_expired'`) e `jwt.PyJWTError` → 401 (`error='invalid_token'`).
- `generate_session_token()` → `secrets.token_urlsafe(32)`.
- `hash_session_token(token)` → `hashlib.sha256(token.encode()).hexdigest()`.

## Etapa 5 — Schemas ⬜
Criar `src/schemas/auth.py`:
- `LoginRequest(login: str, senha: str)`
- `TokenResponse(access_token: str, token_type: str = "bearer", refresh_token: str, expires_in: int)`
- `MessageResponse(detail: str)`

## Etapa 6 — Dependência JWT ⬜
Criar `src/dependencies/auth.py`:
- `class JWTBearer(HTTPBearer)` com `auto_error=False`; `__call__` decodifica e retorna payload.
- `get_current_user(credentials=Depends(JWTBearer()), session=Depends(get_session))` → carrega `Usuarios` (valida ativo/existência).
- `get_current_session(...)` → lê `session_id` do cookie `sistema_ponto_session` (senão header `X-Refresh-Token`); valida `token_hash` em `Sessoes`, `revogado` e `expira_em > now`.

## Etapa 7 — Rotas de auth ⬜
Criar `src/routes/auth.py`:
- `POST /auth/login`: `check_password` (Argon2), cria `Sessoes` (`expira_em=now+30d`), grava cookie, retorna `TokenResponse(access_token, refresh_token=session_id)`.
- `POST /auth/refresh`: resolve sessão (cookie OU header); se `expira_em <= now` → 401; senão revoga token antigo, cria `Sessoes` nova, re-set cookie, emite novo `access_token`.
- `POST /auth/logout`: revoga sessão (`revogado=True`) + limpa cookie.
- Helpers de cookie `create_session_cookie` / `clear_session_cookie` (usar `settings.use_secure_cookie`). Podem ficar em `src/utils/cookies.py`.

## Etapa 8 — Ligar na app ⬜
`main.py`:
- `from src.routes.auth import AuthRouter` + `app.include_router(AuthRouter())`.
- Middleware CORS usando `settings.cors_origins` (CSV parse), `allow_credentials=True`, `allow_methods`/`allow_headers` incluindo `X-Refresh-Token`.

## Etapa 9 — Documentar env ⬜
`.env-example`: adicionar/comentar
```
jwt_secret_key=your_secret_key
jwt_algorithm=HS256
jwt_access_token_expire_minutes=30
jwt_refresh_token_expire_days=30
environment=dev
cors_origins=http://localhost:3000,http://localhost:8000
cookie_secure=false
cookie_samesite=lax
```

---

## Validação final (após todas as etapas)
- `python -c "import main"` → importa sem erro
- `alembic upgrade head` → aplica `0004`
- Com `.env`: via `/docs` testar login → access token → JWTBearer → refresh → logout

## Notas técnicas
- Refresh token é **opaco** (o `session_id`), armazenado como hash SHA-256 em `Sessoes.token_hash` — nunca texto puro.
- `data_criacao` usa `CURRENT_TIMESTAMP` nas migrations de seed (portável SQLite/Postgres), pois `now()` quebra no SQLite.
- Usar o `.venv` (Python 3.14) nas chamadas do projeto; o `alembic`/`python` do PATH global (3.11) **não** tem as dependências.
