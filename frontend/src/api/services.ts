import { apiRequest } from './client'
import type {
  Booking,
  BookingCreateInput,
  LoginInput,
  Property,
  PropertyCreateInput,
  User,
  UserCreateInput,
} from '../types/api'

export const usersApi = {
  list: () => apiRequest<User[]>('/users'),
  create: (payload: UserCreateInput) =>
    apiRequest<User>('/users', { method: 'POST', body: payload }),
}

export const authApi = {
  login: (payload: LoginInput) =>
    apiRequest<User>('/auth/login', { method: 'POST', body: payload }),
}

export const propertiesApi = {
  list: (filters?: {
    city?: string
    property_type?: string
    min_price?: number
    max_price?: number
    min_guests?: number
  }) => apiRequest<Property[]>('/properties', { query: filters }),
  listByOwner: (ownerId: number) =>
    apiRequest<Property[]>(`/properties/owner/${ownerId}/properties`),
  create: (ownerId: number, payload: PropertyCreateInput) =>
    apiRequest<Property>('/properties', {
      method: 'POST',
      query: { owner_id: ownerId },
      body: payload,
    }),
}

export const bookingsApi = {
  listByGuest: (guestId: number) =>
    apiRequest<Booking[]>('/bookings', { query: { guest_id: guestId } }),
  create: (guestId: number, payload: BookingCreateInput) =>
    apiRequest<Booking>('/bookings', {
      method: 'POST',
      query: { guest_id: guestId },
      body: payload,
    }),
  confirm: (bookingId: number) =>
    apiRequest<Booking>(`/bookings/${bookingId}/confirm`, { method: 'PATCH' }),
  cancel: (bookingId: number, guestId: number) =>
    apiRequest<void>(`/bookings/${bookingId}`, {
      method: 'DELETE',
      query: { guest_id: guestId },
    }),
}
