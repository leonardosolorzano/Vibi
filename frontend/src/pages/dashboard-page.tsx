import { useMemo } from 'react'
import { useOutletContext } from 'react-router-dom'
import { Card } from '../components/ui/card'
import { formatCurrency } from '../utils/format'
import type { DashboardOutletContext } from './types'

export function DashboardPage() {
  const { allProperties, myProperties, myBookings } = useOutletContext<DashboardOutletContext>()
  const totalSpent = useMemo(
    () => myBookings.reduce((acc, booking) => acc + booking.total_price, 0),
    [myBookings],
  )

  return (
    <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <Card>
        <h3 className="text-sm font-semibold text-neutral-600">Propiedades publicadas</h3>
        <strong className="mt-1 block text-3xl text-neutral-900">{myProperties.length}</strong>
      </Card>
      <Card>
        <h3 className="text-sm font-semibold text-neutral-600">Reservas realizadas</h3>
        <strong className="mt-1 block text-3xl text-neutral-900">{myBookings.length}</strong>
      </Card>
      <Card>
        <h3 className="text-sm font-semibold text-neutral-600">Gasto total</h3>
        <strong className="mt-1 block text-3xl text-neutral-900">{formatCurrency(totalSpent)}</strong>
      </Card>
      <Card className="bg-neutral-900 text-white">
        <h3 className="text-sm font-semibold text-orange-200">Propiedades disponibles</h3>
        <strong className="mt-1 block text-3xl">{allProperties.length}</strong>
      </Card>
    </section>
  )
}
