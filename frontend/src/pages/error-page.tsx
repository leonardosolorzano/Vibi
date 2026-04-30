import { Link } from 'react-router-dom'
import { Button } from '../components/ui/button'
import { Card } from '../components/ui/card'

export function ErrorPage() {
  return (
    <main className="relative grid min-h-screen place-items-center overflow-hidden px-4 py-8">
      {/* Fondo decorativo */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-orange-400 via-orange-500 to-red-600" />
      
      <Card className="w-full max-w-xl border-0 bg-white/95 text-center shadow-2xl backdrop-blur-sm">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-orange-600">⚠️ Error</p>
        <h1 className="mt-4 text-4xl font-bold text-neutral-900">Algo salió mal</h1>
        <p className="mt-3 text-sm text-neutral-600">
          Ocurrió un error inesperado. Intenta recargar la página o volver al inicio.
        </p>
        <div className="mt-6 flex flex-col gap-3">
          <Button onClick={() => window.location.reload()} className="w-full">
            🔄 Recargar página
          </Button>
          <Link to="/" className="w-full">
            <Button variant="ghost" className="w-full">
              🏠 Volver al inicio
            </Button>
          </Link>
        </div>
      </Card>
    </main>
  )
}
