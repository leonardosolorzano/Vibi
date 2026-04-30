import { Link } from 'react-router-dom'
import { Button } from '../components/ui/button'
import { Card } from '../components/ui/card'

export function NotFoundPage() {
  return (
    <main className="relative grid min-h-screen place-items-center overflow-hidden px-4 py-8">
      {/* Fondo decorativo */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-orange-400 via-orange-500 to-red-600" />
      
      <Card className="w-full max-w-xl border-0 bg-white/95 text-center shadow-2xl backdrop-blur-sm">
        <p className="text-5xl font-bold text-orange-500">404</p>
        <h1 className="mt-4 text-3xl font-bold text-neutral-900">Página no encontrada</h1>
        <p className="mt-3 text-sm text-neutral-600">
          Lo sentimos, la página que buscas no existe o fue movida. ¡Quizás necesitas explorar otros destinos! 🗺️
        </p>
        <div className="mt-6 flex flex-col gap-3">
          <Link to="/" className="w-full">
            <Button className="w-full">
              🏠 Volver al inicio
            </Button>
          </Link>
        </div>
      </Card>
    </main>
  )
}
