import { NavLink, Outlet } from 'react-router-dom'
import { useAuth } from '../../features/auth/auth-context'
import type { DashboardOutletContext } from '../../pages/types'
import { Button } from '../ui/button'

export function AppLayout({
  onRefresh,
  loading,
  context,
}: {
  onRefresh: () => Promise<void>
  loading: boolean
  context: DashboardOutletContext
}) {
  const { user, logout } = useAuth()

  return (
    <main className="grid min-h-screen md:grid-cols-[260px_1fr]">
      <aside className="grid content-start gap-4 bg-neutral-950 p-5 text-white">
        <h1 className="text-2xl font-bold text-orange-400">Vibi Panel</h1>
        <p className="rounded-lg bg-neutral-900 px-3 py-2 text-sm text-neutral-300">{user?.full_name}</p>
        <nav className="grid gap-2">
          <NavLink
            to="/app"
            end
            className={({ isActive }) =>
              `rounded-xl px-3 py-2 text-sm font-medium ${isActive ? 'bg-orange-500 text-white' : 'bg-neutral-900 text-neutral-100 hover:bg-neutral-800'}`
            }
          >
            Dashboard
          </NavLink>
          <NavLink
            to="/app/properties"
            className={({ isActive }) =>
              `rounded-xl px-3 py-2 text-sm font-medium ${isActive ? 'bg-orange-500 text-white' : 'bg-neutral-900 text-neutral-100 hover:bg-neutral-800'}`
            }
          >
            Propiedades
          </NavLink>
          <NavLink
            to="/app/bookings"
            className={({ isActive }) =>
              `rounded-xl px-3 py-2 text-sm font-medium ${isActive ? 'bg-orange-500 text-white' : 'bg-neutral-900 text-neutral-100 hover:bg-neutral-800'}`
            }
          >
            Reservas
          </NavLink>
        </nav>
        <Button className="mt-auto" variant="ghost" onClick={logout}>Cerrar sesión</Button>
      </aside>

      <section className="grid gap-4 p-4 md:p-7">
        <header className="flex flex-col justify-between gap-3 rounded-2xl border border-orange-100 bg-white p-4 md:flex-row md:items-center">
          <div>
            <h2 className="text-xl font-bold text-neutral-900">Panel de control</h2>
            <small className="text-neutral-600">Conectado a FastAPI `api/v1`</small>
          </div>
          <Button onClick={() => void onRefresh()} disabled={loading}>
            {loading ? 'Actualizando...' : 'Refrescar'}
          </Button>
        </header>
        <Outlet context={context} />
      </section>
    </main>
  )
}
