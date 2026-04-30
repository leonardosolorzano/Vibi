import { useCallback, useEffect, useState } from 'react'
import { bookingsApi, propertiesApi } from '../../api/services'
import { useAuth } from '../auth/auth-context'
import type { Booking, BookingCreateInput, Property, PropertyCreateInput } from '../../types/api'

export function useDashboardData() {
  const { user } = useAuth()
  const [allProperties, setAllProperties] = useState<Property[]>([])
  const [myProperties, setMyProperties] = useState<Property[]>([])
  const [myBookings, setMyBookings] = useState<Booking[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)

  const refreshData = useCallback(async () => {
    if (!user) return
    setLoading(true)
    setError(null)
    try {
      const [properties, ownerProperties, bookings] = await Promise.all([
        propertiesApi.list(),
        propertiesApi.listByOwner(user.id),
        bookingsApi.listByGuest(user.id),
      ])
      setAllProperties(properties)
      setMyProperties(ownerProperties)
      setMyBookings(bookings)
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'No se pudieron cargar los datos')
    } finally {
      setLoading(false)
    }
  }, [user])

  useEffect(() => {
    void refreshData()
  }, [refreshData])

  const createProperty = async (payload: PropertyCreateInput) => {
    if (!user) return
    setLoading(true)
    setError(null)
    setNotice(null)
    try {
      await propertiesApi.create(user.id, payload)
      await refreshData()
      setNotice('Propiedad publicada con éxito.')
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'No se pudo crear la propiedad')
    } finally {
      setLoading(false)
    }
  }

  const createBooking = async (payload: BookingCreateInput) => {
    if (!user) return
    setLoading(true)
    setError(null)
    setNotice(null)
    try {
      await bookingsApi.create(user.id, payload)
      await refreshData()
      setNotice('Reserva creada correctamente.')
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'No se pudo crear la reserva')
    } finally {
      setLoading(false)
    }
  }

  const confirmBooking = async (bookingId: number) => {
    setLoading(true)
    setError(null)
    try {
      await bookingsApi.confirm(bookingId)
      await refreshData()
      setNotice('Reserva confirmada.')
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'No se pudo confirmar la reserva')
    } finally {
      setLoading(false)
    }
  }

  const cancelBooking = async (bookingId: number) => {
    if (!user) return
    setLoading(true)
    setError(null)
    try {
      await bookingsApi.cancel(bookingId, user.id)
      await refreshData()
      setNotice('Reserva cancelada.')
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : 'No se pudo cancelar la reserva')
    } finally {
      setLoading(false)
    }
  }

  return {
    allProperties,
    myProperties,
    myBookings,
    loading,
    error,
    notice,
    setError,
    setNotice,
    refreshData,
    createProperty,
    createBooking,
    confirmBooking,
    cancelBooking,
  }
}
