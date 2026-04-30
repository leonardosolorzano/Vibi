import type { Booking, Property } from '../types/api'

export interface DashboardOutletContext {
  allProperties: Property[]
  myProperties: Property[]
  myBookings: Booking[]
}
