import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { toast } from 'sonner'
import { Button } from '../components/ui/button'
import { Card } from '../components/ui/card'
import { Input } from '../components/ui/input'
import { useAuth } from '../features/auth/auth-context'
import type { UserCreateInput } from '../types/api'

// Frases inspiradoras para viajeros
const TRAVELER_QUOTES = [
  '✈️ La vida es un viaje, ¡vive cada destino al máximo!',
  '🌍 Viajar es la mejor forma de escribir la historia de tu vida',
  '🗺️ El mundo espera, ¿listo para explorarlo?',
  '🧳 Cada viaje te cambia, conviértete en quién deseas ser',
  '🌅 Las mejores memorias se crean viajando',
]

export function LoginPage() {
  const navigate = useNavigate()
  const { loading, login, register } = useAuth()
  const [error, setError] = useState<string | null>(null)
  const [isRegisterMode, setIsRegisterMode] = useState(false)
  const [dailyQuote] = useState(() => 
    TRAVELER_QUOTES[Math.floor(Math.random() * TRAVELER_QUOTES.length)]
  )
  const [loginForm, setLoginForm] = useState({
    email: '',
    password: '',
  })
  const [registerForm, setRegisterForm] = useState<UserCreateInput>({
    email: '',
    full_name: '',
    phone: '',
    password: '',
  })

  useEffect(() => {
    if (error) toast.error(error)
  }, [error])

  const handleClose = () => {
    navigate('/')
  }

  return (
    <main className="relative grid min-h-screen place-items-center overflow-hidden px-4 py-8">
      {/* Fondo decorativo con gradiente */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-orange-400 via-orange-500 to-red-600" />

      {/* Card con fondo semi-transparente */}
      <Card className="relative w-full max-w-xl border-0 bg-white/95 shadow-2xl backdrop-blur-sm">
        {/* Botón cerrar (X) */}
        <button
          onClick={handleClose}
          className="absolute right-4 top-4 flex h-8 w-8 items-center justify-center rounded-full bg-gray-200 text-gray-600 transition hover:bg-gray-300 hover:text-gray-800"
          aria-label="Cerrar"
        >
          ✕
        </button>

        <div className="pr-10">
          <h1 className="text-3xl font-bold">
            Vi<span className="text-orange-500">bi</span>
          </h1>
          <p className="mt-2 text-sm text-gray-600">{dailyQuote}</p>
          <p className="mt-3 text-sm text-gray-700">Accede o crea tu cuenta para empezar.</p>

          <div className="my-6 grid grid-cols-2 gap-3">
            <Button 
              variant={!isRegisterMode ? 'primary' : 'ghost'} 
              onClick={() => setIsRegisterMode(false)}
              className="w-full"
            >
              Iniciar sesión
            </Button>
            <Button 
              variant={isRegisterMode ? 'primary' : 'ghost'} 
              onClick={() => setIsRegisterMode(true)}
              className="w-full"
            >
              Crear cuenta
            </Button>
          </div>

          {!isRegisterMode ? (
            <form className="grid gap-4"
              onSubmit={(event) => {
                event.preventDefault()
                setError(null)
                void login(loginForm)
                  .then(() => navigate('/app'))
                  .catch((requestError) =>
                    setError(requestError instanceof Error ? requestError.message : 'No se pudo iniciar sesión'),
                  )
              }}
            >
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1.5">Email</label>
                <Input
                  type="email"
                  placeholder="tu@email.com"
                  value={loginForm.email}
                  onChange={(event) => setLoginForm((prev) => ({ ...prev, email: event.target.value }))}
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1.5">Contraseña</label>
                <Input
                  type="password"
                  placeholder="Mínimo 8 caracteres"
                  value={loginForm.password}
                  onChange={(event) => setLoginForm((prev) => ({ ...prev, password: event.target.value }))}
                  minLength={8}
                  required
                />
              </div>
              <Button type="submit" disabled={loading} className="w-full">
                {loading ? 'Entrando...' : 'Entrar'}
              </Button>
            </form>
          ) : (
            <form className="grid gap-4"
              onSubmit={(event) => {
                event.preventDefault()
                setError(null)
                void register(registerForm)
                  .then(() => navigate('/app'))
                  .catch((requestError) =>
                    setError(requestError instanceof Error ? requestError.message : 'No se pudo crear la cuenta'),
                  )
              }}
            >
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1.5">Nombre completo</label>
                <Input
                  placeholder="Tu nombre"
                  value={registerForm.full_name}
                  onChange={(event) => setRegisterForm((prev) => ({ ...prev, full_name: event.target.value }))}
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1.5">Email</label>
                <Input
                  type="email"
                  placeholder="tu@email.com"
                  value={registerForm.email}
                  onChange={(event) => setRegisterForm((prev) => ({ ...prev, email: event.target.value }))}
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1.5">Teléfono (opcional)</label>
                <Input
                  placeholder="+34 123 456 789"
                  value={registerForm.phone ?? ''}
                  onChange={(event) => setRegisterForm((prev) => ({ ...prev, phone: event.target.value }))}
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-gray-700 mb-1.5">Contraseña</label>
                <Input
                  type="password"
                  placeholder="Mínimo 8 caracteres"
                  value={registerForm.password}
                  onChange={(event) => setRegisterForm((prev) => ({ ...prev, password: event.target.value }))}
                  minLength={8}
                  required
                />
              </div>
              <Button type="submit" disabled={loading} className="w-full">
                {loading ? 'Creando...' : 'Crear cuenta'}
              </Button>
            </form>
          )}
        </div>
      </Card>
    </main>
  )
}
