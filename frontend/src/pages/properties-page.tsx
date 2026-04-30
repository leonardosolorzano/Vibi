import { useState } from 'react'
import { useOutletContext } from 'react-router-dom'
import { Button } from '../components/ui/button'
import { Card } from '../components/ui/card'
import { Input } from '../components/ui/input'
import { Select } from '../components/ui/select'
import { Textarea } from '../components/ui/textarea'
import type { BookingCreateInput, PropertyCreateInput, PropertyType } from '../types/api'
import { formatCurrency } from '../utils/format'
import type { DashboardOutletContext } from './types'

const propertyTypes: PropertyType[] = ['apartment', 'house', 'villa', 'cabin', 'loft']
const defaultPropertyForm: PropertyCreateInput = {
  title: '',
  description: '',
  property_type: 'apartment',
  price_per_night: 80,
  city: '',
  address: '',
  max_guests: 2,
  bedrooms: 1,
  bathrooms: 1,
}

export function PropertiesPage({
  onCreateProperty,
  onCreateBooking,
}: {
  onCreateProperty: (payload: PropertyCreateInput) => Promise<void>
  onCreateBooking: (payload: BookingCreateInput) => Promise<void>
}) {
  const { allProperties, myProperties } = useOutletContext<DashboardOutletContext>()
  const [propertyForm, setPropertyForm] = useState<PropertyCreateInput>(defaultPropertyForm)
  const [bookingForm, setBookingForm] = useState<BookingCreateInput>({
    property_id: 0,
    check_in_date: '',
    check_out_date: '',
    number_of_guests: 1,
    notes: '',
  })

  return (
    <section className="grid gap-4 xl:grid-cols-2">
      <Card>
        <h3 className="mb-4 text-lg font-bold text-neutral-900">Nueva propiedad</h3>
        <form className="grid gap-3"
          onSubmit={(event) => {
            event.preventDefault()
            void onCreateProperty(propertyForm).then(() => setPropertyForm(defaultPropertyForm))
          }}
        >
          <Input
            placeholder="Título"
            value={propertyForm.title}
            onChange={(event) => setPropertyForm((prev) => ({ ...prev, title: event.target.value }))}
            required
          />
          <Textarea
            placeholder="Descripción"
            value={propertyForm.description}
            onChange={(event) =>
              setPropertyForm((prev) => ({ ...prev, description: event.target.value }))
            }
            minLength={10}
            required
          />
          <Select
            value={propertyForm.property_type}
            onChange={(event) =>
              setPropertyForm((prev) => ({ ...prev, property_type: event.target.value as PropertyType }))
            }
          >
            {propertyTypes.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </Select>
          <Input
            placeholder="Ciudad"
            value={propertyForm.city}
            onChange={(event) => setPropertyForm((prev) => ({ ...prev, city: event.target.value }))}
            required
          />
          <Input
            placeholder="Dirección"
            value={propertyForm.address}
            onChange={(event) => setPropertyForm((prev) => ({ ...prev, address: event.target.value }))}
            required
          />
          <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
            <Input
              type="number"
              min={1}
              value={propertyForm.max_guests}
              onChange={(event) =>
                setPropertyForm((prev) => ({ ...prev, max_guests: Number(event.target.value) }))
              }
              required
            />
            <Input
              type="number"
              min={1}
              value={propertyForm.bedrooms}
              onChange={(event) =>
                setPropertyForm((prev) => ({ ...prev, bedrooms: Number(event.target.value) }))
              }
              required
            />
            <Input
              type="number"
              min={1}
              value={propertyForm.bathrooms}
              onChange={(event) =>
                setPropertyForm((prev) => ({ ...prev, bathrooms: Number(event.target.value) }))
              }
              required
            />
          </div>
          <Input
            type="number"
            min={1}
            step="0.01"
            value={propertyForm.price_per_night}
            onChange={(event) =>
              setPropertyForm((prev) => ({ ...prev, price_per_night: Number(event.target.value) }))
            }
            required
          />
          <Button type="submit">Publicar</Button>
        </form>
      </Card>

      <Card>
        <h3 className="mb-4 text-lg font-bold text-neutral-900">Nueva reserva</h3>
        <form className="grid gap-3"
          onSubmit={(event) => {
            event.preventDefault()
            void onCreateBooking(bookingForm)
          }}
        >
          <Select
            value={bookingForm.property_id}
            onChange={(event) =>
              setBookingForm((prev) => ({ ...prev, property_id: Number(event.target.value) }))
            }
            required
          >
            <option value={0}>Selecciona una propiedad</option>
            {allProperties.map((property) => (
              <option key={property.id} value={property.id}>
                {property.title} - {formatCurrency(property.price_per_night)}
              </option>
            ))}
          </Select>
          <Input
            type="datetime-local"
            value={bookingForm.check_in_date}
            onChange={(event) =>
              setBookingForm((prev) => ({ ...prev, check_in_date: event.target.value }))
            }
            required
          />
          <Input
            type="datetime-local"
            value={bookingForm.check_out_date}
            onChange={(event) =>
              setBookingForm((prev) => ({ ...prev, check_out_date: event.target.value }))
            }
            required
          />
          <Input
            type="number"
            min={1}
            value={bookingForm.number_of_guests}
            onChange={(event) =>
              setBookingForm((prev) => ({ ...prev, number_of_guests: Number(event.target.value) }))
            }
            required
          />
          <Textarea
            placeholder="Notas opcionales"
            value={bookingForm.notes ?? ''}
            onChange={(event) => setBookingForm((prev) => ({ ...prev, notes: event.target.value }))}
          />
          <Button type="submit" variant="secondary">Reservar</Button>
        </form>

        <h4 className="mb-3 mt-6 text-base font-bold text-neutral-900">Mis propiedades</h4>
        <ul className="grid gap-2">
          {myProperties.map((property) => (
            <li key={property.id} className="grid gap-1 rounded-xl border border-orange-100 bg-orange-50 p-3">
              <strong className="text-neutral-900">{property.title}</strong>
              <span className="text-sm text-neutral-700">
                {property.city} - {formatCurrency(property.price_per_night)}
              </span>
            </li>
          ))}
          {myProperties.length === 0 && <li className="rounded-xl border border-dashed border-orange-200 p-3 text-sm text-neutral-600">Aún no has publicado propiedades.</li>}
        </ul>
      </Card>
    </section>
  )
}
