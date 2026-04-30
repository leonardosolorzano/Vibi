import { useMemo } from 'react'
import { useOutletContext } from 'react-router-dom'
import { Button } from '../components/ui/button'
import { Card } from '../components/ui/card'
import { formatCurrency, formatDate } from '../utils/format'
import type { DashboardOutletContext } from './types'

export function BookingsPage({
  onConfirm,
  onCancel,
}: {
  onConfirm: (bookingId: number) => Promise<void>
  onCancel: (bookingId: number) => Promise<void>
}) {
  const { allProperties, myBookings } = useOutletContext<DashboardOutletContext>()
  const propertyById = useMemo(
    () => new Map(allProperties.map((property) => [property.id, property])),
    [allProperties],
  )

  return (
    <Card>
      <h3 className="mb-4 text-lg font-bold text-neutral-900">Mis reservas</h3>
      <ul className="grid gap-3">
        {myBookings.map((booking) => {
          const property = propertyById.get(booking.property_id)
          const statusColor = {
            pending: 'bg-amber-100 text-amber-900',
            confirmed: 'bg-emerald-100 text-emerald-900',
            cancelled: 'bg-red-100 text-red-900',
            completed: 'bg-blue-100 text-blue-900',
          }[booking.status]

          return (
            <li key={booking.id} className="grid gap-3 rounded-xl border border-orange-100 p-4 md:grid-cols-[1fr_auto] md:items-center">
              <div>
                <strong className="block text-neutral-900">{property?.title ?? `Propiedad #${booking.property_id}`}</strong>
                <span className="block text-sm text-neutral-700">
                  {formatDate(booking.check_in_date)} {'->'} {formatDate(booking.check_out_date)}
                </span>
                <span className="block text-sm text-neutral-700">
                  {booking.number_of_guests} huésped(es) - {formatCurrency(booking.total_price)}
                </span>
                <span className={`mt-2 inline-block rounded-full px-3 py-1 text-xs font-semibold ${statusColor}`}>
                  {booking.status}
                </span>
              </div>
              <div className="flex gap-2">
                {booking.status === 'pending' && (
                  <Button onClick={() => void onConfirm(booking.id)}>Confirmar</Button>
                )}
                {booking.status !== 'cancelled' && booking.status !== 'completed' && (
                  <Button variant="danger" onClick={() => void onCancel(booking.id)}>
                    Cancelar
                  </Button>
                )}
              </div>
            </li>
          )
        })}
        {myBookings.length === 0 && <li className="rounded-xl border border-dashed border-orange-200 p-3 text-sm text-neutral-600">No tienes reservas todavía.</li>}
      </ul>
    </Card>
  )
}
