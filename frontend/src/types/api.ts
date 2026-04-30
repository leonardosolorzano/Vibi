export type PropertyType = 'apartment' | 'house' | 'villa' | 'cabin' | 'loft'

export type BookingStatus = 'pending' | 'confirmed' | 'cancelled' | 'completed'

export interface User {
  id: number
  email: string
  full_name: string
  phone: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Property {
  id: number
  title: string
  description: string
  property_type: PropertyType
  price_per_night: number
  city: string
  address: string
  max_guests: number
  bedrooms: number
  bathrooms: number
  owner_id: number
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface Booking {
  id: number
  property_id: number
  guest_id: number
  check_in_date: string
  check_out_date: string
  number_of_guests: number
  notes: string | null
  total_price: number
  status: BookingStatus
  created_at: string
  updated_at: string
}

export interface UserCreateInput {
  email: string
  full_name: string
  password: string
  phone?: string
}

export interface LoginInput {
  email: string
  password: string
}

export interface PropertyCreateInput {
  title: string
  description: string
  property_type: PropertyType
  price_per_night: number
  city: string
  address: string
  max_guests: number
  bedrooms: number
  bathrooms: number
}

export interface BookingCreateInput {
  property_id: number
  check_in_date: string
  check_out_date: string
  number_of_guests: number
  notes?: string
}
