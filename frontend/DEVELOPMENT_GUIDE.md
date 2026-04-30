# 🎨 Guía de Desarrollo - Frontend Vibi

## 📋 Tabla de Contenidos
1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Convenciones de Código](#convenciones-de-código)
3. [Componentes UI](#componentes-ui)
4. [Buenas Prácticas](#buenas-prácticas)
5. [Desarrollo Local](#desarrollo-local)

---

## 🏗️ Estructura del Proyecto

```
frontend/
├── src/
│   ├── api/
│   │   ├── client.ts        # Cliente HTTP Axios
│   │   └── services.ts      # Servicios de API
│   ├── app/
│   │   └── router/          # Configuración de rutas
│   ├── assets/              # Imágenes, videos, etc.
│   ├── components/
│   │   ├── layout/          # Componentes de maquetación
│   │   └── ui/              # Componentes reutilizables
│   ├── features/            # Características/módulos
│   │   └── auth/            # Autenticación
│   ├── pages/               # Páginas principales
│   │   └── public/          # Páginas públicas
│   ├── services/            # Servicios (sesión, etc.)
│   ├── types/               # Tipos TypeScript
│   ├── utils/               # Funciones de utilidad
│   ├── App.tsx              # Componente raíz
│   ├── index.css            # Estilos globales
│   └── main.tsx             # Punto de entrada
├── public/                  # Archivos estáticos
├── index.html               # HTML principal
├── package.json             # Dependencias
├── tailwind.config.js       # (Si existe) Config Tailwind
├── tsconfig.json            # Configuración TypeScript
└── vite.config.ts           # Configuración Vite
```

---

## 📝 Convenciones de Código

### Nombres de Archivos
```typescript
// Componentes React: PascalCase
LoginPage.tsx
UserCard.tsx
Button.tsx

// Funciones/utilidades: camelCase
formatCurrency.ts
useAuth.ts
apiClient.ts

// Tipos/interfaces: PascalCase
User.ts
Property.ts
UserCreateInput.ts
```

### Nombres de Variables y Funciones
```typescript
// Estado
const [isLoading, setIsLoading] = useState(false)
const [userData, setUserData] = useState<User | null>(null)

// Funciones
const handleClick = () => {}
const fetchProperties = async () => {}
const formatDate = (date: Date) => {}

// Booleanos con prefijo
const isVisible = true
const hasError = false
const canSubmit = true
```

### Tipos TypeScript
```typescript
// Interfaces para objetos
interface User {
  id: string
  email: string
  full_name: string
}

// Types para uniones o tipos complejos
type Status = 'pending' | 'success' | 'error'

// Props de componentes
interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  isLoading?: boolean
}
```

---

## 🎨 Componentes UI

### Componentes Disponibles

#### Button
```tsx
import { Button } from '@/components/ui/button'

// Variantes: primary (default), secondary, ghost, danger
<Button>Click me</Button>
<Button variant="secondary">Secundario</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="danger">Peligro</Button>
<Button disabled>Deshabilitado</Button>
```

#### Card
```tsx
import { Card } from '@/components/ui/card'

<Card>
  <h3>Título</h3>
  <p>Contenido</p>
</Card>

<Card className="bg-blue-50">Custom styling</Card>
```

#### Input
```tsx
import { Input } from '@/components/ui/input'

<Input 
  type="email"
  placeholder="tu@email.com"
  required
/>

<Input 
  type="number"
  min={0}
  max={100}
/>
```

#### Select (si existe)
```tsx
import { Select } from '@/components/ui/select'

<Select>
  <option value="">Selecciona...</option>
  <option value="1">Opción 1</option>
</Select>
```

#### Textarea (si existe)
```tsx
import { Textarea } from '@/components/ui/textarea'

<Textarea 
  placeholder="Escribe aquí..."
  rows={4}
/>
```

---

## ✅ Buenas Prácticas

### 1. Componentes Funcionales con Hooks
```typescript
// ✅ Correcto
export function MyComponent() {
  const [data, setData] = useState<Data | null>(null)
  
  useEffect(() => {
    // Efecto secundario
  }, [])
  
  return <div>{data?.name}</div>
}

// ❌ Evitar
class MyComponent extends React.Component { ... }
```

### 2. Gestión de Estado
```typescript
// ✅ Correcto: Estado cercano a donde se usa
function Form() {
  const [formData, setFormData] = useState({ name: '', email: '' })
  
  return <input value={formData.name} onChange={e => 
    setFormData(prev => ({ ...prev, name: e.target.value }))
  } />
}

// ❌ Evitar: Estado global si solo lo usa un componente
```

### 3. Manejo de Errores
```typescript
// ✅ Correcto
useEffect(() => {
  void api.fetch()
    .then(data => setData(data))
    .catch(error => {
      const message = error instanceof Error 
        ? error.message 
        : 'Error desconocido'
      toast.error(message)
    })
}, [])

// ❌ Evitar
useEffect(() => {
  api.fetch().then(setData) // Sin manejo de errores
}, [])
```

### 4. Renderizado Condicional
```typescript
// ✅ Correcto
return (
  <>
    {loading && <LoadingSpinner />}
    {error && <ErrorMessage error={error} />}
    {data && <DataDisplay data={data} />}
  </>
)

// ❌ Evitar
return (
  loading ? <LoadingSpinner /> : 
  error ? <ErrorMessage error={error} /> : 
  <DataDisplay data={data} />
)
```

### 5. Listas y Keys
```typescript
// ✅ Correcto
{items.map(item => (
  <Card key={item.id}>
    <h3>{item.title}</h3>
  </Card>
))}

// ❌ Evitar
{items.map((item, index) => (
  <Card key={index}> {/* Key inestable */}
    <h3>{item.title}</h3>
  </Card>
))}
```

### 6. Optimización con useMemo
```typescript
// ✅ Para cálculos pesados
const filteredItems = useMemo(() => {
  return items.filter(item => item.active && item.price > minPrice)
}, [items, minPrice])

// ❌ Sin memoización (se recalcula en cada render)
const filteredItems = items.filter(...)
```

### 7. TypeScript Strict
```typescript
// ✅ Correcto: Tipos explícitos
interface User {
  id: string
  name: string
  age: number
}

const users: User[] = []

// ❌ Evitar: Any type
const users: any[] = []
```

---

## 🚀 Desarrollo Local

### Instalación
```bash
cd frontend
npm install
```

### Desarrollo
```bash
npm run dev
# Accede a http://localhost:5173
```

### Build para producción
```bash
npm run build
```

### Previsualizar build
```bash
npm run preview
```

### Linting (si está configurado)
```bash
npm run lint
```

---

## 🎨 Paleta de Colores

### Naranja (Principal)
- `orange-50` - `#FFF7ED`
- `orange-400` - `#FB923C` (Hover)
- `orange-500` - `#F97316` (Principal)
- `orange-600` - `#EA580C` (Oscuro)

### Rojo (Secundario)
- `red-500` - `#EF4444`
- `red-600` - `#DC2626` (Hover)

### Grises
- `gray-100` - `#F3F4F6`
- `gray-700` - `#374151`
- `neutral-900` - `#171717`

---

## 📱 Responsive Breakpoints

```css
/* Tailwind breakpoints */
sm   640px   /* Mobile grande */
md   768px   /* Tablet */
lg   1024px  /* Desktop */
xl   1280px  /* Desktop grande */
2xl  1536px  /* Desktop muy grande */
```

### Ejemplo
```tsx
<div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  {/* 1 columna en mobile, 2 en tablet, 3 en desktop, 4 en desktop grande */}
</div>
```

---

## 🔐 Variables de Entorno

Crear archivo `.env.local`:
```
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Vibi
```

Usar en código:
```typescript
const apiUrl = import.meta.env.VITE_API_URL
```

---

## 🎯 Checklist antes de hacer commit

- [ ] Código compila sin errores
- [ ] Sin `console.log()` en producción
- [ ] Tipos TypeScript correctos
- [ ] Componentes reutilizables cuando es posible
- [ ] Props documentadas
- [ ] Manejo de errores implementado
- [ ] Loading states mostrados
- [ ] Responsive en mobile
- [ ] Accesible (labels, aria-label, etc.)

---

## 📚 Recursos Útiles

- [React Docs](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS](https://tailwindcss.com)
- [Vite Guide](https://vitejs.dev/guide/)
- [React Router](https://reactrouter.com/)

---

**Última actualización**: 30 de Abril de 2026  
**Versión**: 1.0
