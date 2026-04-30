# Frontend Vibi

Aplicacion React + TypeScript para el cliente de Vibi. Este frontend consume el backend FastAPI (`/api/v1`) y cubre:

- Landing publica de propiedades
- Autenticacion (login y registro)
- Panel privado con dashboard, gestion de propiedades y reservas

## Stack y herramientas

- `react`, `react-dom`
- `react-router-dom` para rutas publica/privada
- `vite` para desarrollo y build
- `typescript` para tipado
- `eslint` para reglas base de calidad

## Scripts

- `npm run dev`: levanta Vite en desarrollo
- `npm run build`: ejecuta chequeo TypeScript y build de produccion
- `npm run lint`: ejecuta ESLint
- `npm run preview`: previsualiza el build

## Configuracion de entorno

La URL base de API se define en `src/config.ts`:

- Usa `VITE_API_BASE_URL` si existe
- Si no existe, usa `http://localhost:8000/api/v1`

Ejemplo:

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## Flujo de la aplicacion

1. `src/main.tsx` monta la app con `StrictMode`.
2. `src/App.tsx` renderiza `AppRouter`.
3. `AppRouter` envuelve con `BrowserRouter` y `AuthProvider`.
4. `AppRoutes` decide:
   - Sin usuario: rutas publicas (`/`, `/login`)
   - Con usuario: rutas privadas bajo `/app`
5. Las pantallas privadas usan `useDashboardData` para cargar y mutar datos.

## Estructura y documentacion por archivo

### Raiz

- `index.html`: contenedor `#root` y script de entrada.
- `vite.config.ts`: plugin de React + preset de React Compiler via Babel.
- `eslint.config.js`: configuracion ESLint para archivos TS/TSX.
- `tsconfig.json`: archivo de referencias (`app` y `node`).
- `tsconfig.app.json`: compilacion de codigo cliente en `src`.
- `tsconfig.node.json`: compilacion para `vite.config.ts`.
- `.gitignore`: excluye `node_modules`, builds y archivos locales.

### `src/`

- `main.tsx`: bootstrap de React.
- `App.tsx`: punto de entrada visual; delega al router.
- `index.css`: estilos globales y estilos de las vistas publicas/privadas.
- `config.ts`: resolucion de URL base para API.

### `src/app/router/`

- `AppRouter.tsx`
  - Proveedor principal de ruteo y autenticacion.
- `app-routes.tsx`
  - Define todas las rutas.
  - Crea `PrivateRoutes` con layout y subrutas:
    - `/app` -> `DashboardPage`
    - `/app/properties` -> `PropertiesPage`
    - `/app/bookings` -> `BookingsPage`
  - Muestra `Alert` global por errores/notificaciones del hook de dashboard.

### `src/api/`

- `client.ts`
  - Cliente HTTP generico `apiRequest<T>()`.
  - Construye URL con query params.
  - Serializa body JSON.
  - Maneja errores HTTP y `204 No Content`.
- `services.ts`
  - Capa de servicios por recurso:
    - `usersApi`: listar/crear usuarios
    - `authApi`: login
    - `propertiesApi`: listar, listar por owner, crear
    - `bookingsApi`: listar por guest, crear, confirmar, cancelar

### `src/features/auth/`

- `auth-context.tsx`
  - Contexto global de autenticacion.
  - Estado: `user` y `loading`.
  - Acciones: `login`, `register`, `logout`.
  - Persiste sesion en `localStorage` mediante `sessionService`.
  - Expone hook `useAuth()`.

### `src/features/dashboard/`

- `use-dashboard-data.ts`
  - Hook de estado principal para el panel privado.
  - Gestiona:
    - `allProperties`
    - `myProperties`
    - `myBookings`
    - `loading`, `error`, `notice`
  - Acciones:
    - `refreshData`
    - `createProperty`
    - `createBooking`
    - `confirmBooking`
    - `cancelBooking`
  - Usa APIs de propiedades/reservas y depende del usuario autenticado.

### `src/components/`

- `components/layout/app-layout.tsx`
  - Layout del panel privado:
    - Sidebar con navegacion
    - Boton de logout
    - Header con refresco de datos
    - `Outlet` para paginas hijas
- `components/ui/alert.tsx`
  - Alerta reutilizable con variantes `error` y `ok`.
- `components/common/navbar.tsx`
  - Componente generico de navbar (actualmente no usado en rutas).
- `components/common/hero.tsx`
  - Componente de hero basico (actualmente no usado en rutas).

### `src/pages/`

- `pages/login-page.tsx`
  - Vista de autenticacion con dos modos:
    - Login
    - Registro
  - Usa `useAuth` y redirige a `/app` al completar.
- `pages/dashboard-page.tsx`
  - Tarjetas de resumen:
    - propiedades publicadas
    - reservas realizadas
    - gasto total
    - propiedades disponibles
- `pages/properties-page.tsx`
  - Formulario para crear propiedad.
  - Formulario para crear reserva.
  - Lista de propiedades propias.
- `pages/bookings-page.tsx`
  - Lista de reservas del usuario.
  - Acciones por estado:
    - confirmar (si `pending`)
    - cancelar (si no esta `cancelled` ni `completed`)
- `pages/types.ts`
  - Tipo compartido `DashboardOutletContext` para datos de `Outlet`.
- `pages/public/home-page.tsx`
  - Landing publica:
    - carga propiedades activas
    - filtros por ciudad, huespedes y precio
    - link a login
    - muestra cards de propiedades

### `src/services/`

- `services/session.ts`
  - Persistencia de usuario en `localStorage` (`vibi_user`).
  - Metodos:
    - `getUser`
    - `setUser`
    - `clear`

### `src/types/`

- `types/api.ts`
  - Tipos de dominio y payloads:
    - `User`
    - `Property`
    - `Booking`
    - `LoginInput`
    - `UserCreateInput`
    - `PropertyCreateInput`
    - `BookingCreateInput`
  - Enums string:
    - `PropertyType`
    - `BookingStatus`

### `src/utils/`

- `utils/format.ts`
  - `formatCurrency`: moneda USD con locale `es-ES`.
  - `formatDate`: fecha/hora con locale `es-ES`.

## Rutas de la aplicacion

- Publicas:
  - `/` -> Home publica
  - `/login` -> Login/Registro
- Privadas (requieren usuario):
  - `/app` -> Dashboard
  - `/app/properties` -> Propiedades
  - `/app/bookings` -> Reservas

Si la ruta no existe, se redirige segun estado de autenticacion.

## Estado y sesion

- El usuario autenticado vive en `AuthContext`.
- La sesion persiste en `localStorage` para recuperar estado al recargar.
- El panel privado centraliza la data en `useDashboardData`, evitando logica duplicada en paginas.

## Notas tecnicas y mantenimiento

- `navbar.tsx` y `hero.tsx` existen como componentes comunes, pero no estan conectados al flujo principal actual.
- Para nuevos endpoints, seguir patron:
  1. agregar metodo en `src/api/services.ts`
  2. tipar payload/respuesta en `src/types/api.ts`
  3. consumir desde hook o pagina correspondiente
- Para mensajes globales en panel privado, usar `error` y `notice` de `useDashboardData`.
