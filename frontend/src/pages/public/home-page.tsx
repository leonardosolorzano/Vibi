import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { toast } from 'sonner'
import { propertiesApi } from '../../api/services'
import { Button } from '../../components/ui/button'
import { Card } from '../../components/ui/card'
import { Input } from '../../components/ui/input'
import type { Property } from '../../types/api'
import { formatCurrency } from '../../utils/format'

const HOME_QUOTES = [
  '✈️ El mundo es un libro, y aquellos que no viajan solo leen una página',
  '🌍 La vida es un viaje de descubrimiento, no un destino fijo',
  '🗺️ Viajar es la mejor manera de crecer como persona',
]

export function HomePage() {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [properties, setProperties] = useState<Property[]>([])
  const [quote] = useState(() => HOME_QUOTES[Math.floor(Math.random() * HOME_QUOTES.length)])
  const [search, setSearch] = useState({
    city: '',
    min_guests: '',
    min_price: '',
    max_price: '',
  })

  useEffect(() => {
    setLoading(true)
    setError(null)
    void propertiesApi
      .list()
      .then((items) => setProperties(items.filter((item) => item.is_active)))
      .catch((requestError) =>
        setError(requestError instanceof Error ? requestError.message : 'No se pudieron cargar propiedades'),
      )
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    if (error) toast.error(error)
  }, [error])

  const filteredProperties = useMemo(() => {
    const citySearch = search.city.trim().toLowerCase()
    const minGuests = Number(search.min_guests || 0)
    const minPrice = Number(search.min_price || 0)
    const maxPrice = Number(search.max_price || Number.POSITIVE_INFINITY)

    return properties.filter((property) => {
      if (citySearch && !property.city.toLowerCase().includes(citySearch)) return false
      if (property.max_guests < minGuests) return false
      if (property.price_per_night < minPrice) return false
      if (property.price_per_night > maxPrice) return false
      return true
    })
  }, [properties, search])

  return (
    <main className="min-h-screen bg-gradient-to-br from-orange-50 via-orange-100 to-orange-200">
      <div className="mx-auto max-w-7xl px-4 py-8">
        {/* Header */}
        <header className="mb-8 flex items-center justify-between">
          <h1 className="text-4xl font-bold text-neutral-900">
            Vi<span className="text-orange-500">bi</span>
          </h1>
          <Link to="/login">
            <Button>Iniciar sesión</Button>
          </Link>
        </header>

        {/* Hero Section */}
        <section className="mb-12 rounded-3xl bg-gradient-to-r from-orange-500 to-red-600 p-8 text-white shadow-xl">
          <h2 className="text-4xl font-bold leading-tight">
            Descubre el mundo, un viaje a la vez
          </h2>
          <p className="mt-3 text-lg text-orange-100">{quote}</p>
          <p className="mt-2 text-base text-orange-50">
            Encuentra alojamientos únicos y asequibles para tu próxima aventura
          </p>
        </section>

        {/* Search Section */}
        <section className="mb-12 rounded-3xl bg-white p-6 shadow-lg">
          <h3 className="mb-4 text-lg font-bold text-neutral-900">¿A dónde quieres viajar?</h3>
          <div className="grid gap-4 md:grid-cols-4">
            <div>
              <label className="mb-2 block text-xs font-semibold text-gray-700">Destino</label>
              <Input
                placeholder="¿A dónde vas?"
                value={search.city}
                onChange={(event) => setSearch((prev) => ({ ...prev, city: event.target.value }))}
              />
            </div>
            <div>
              <label className="mb-2 block text-xs font-semibold text-gray-700">Huéspedes</label>
              <Input
                type="number"
                min={1}
                placeholder="Número de huéspedes"
                value={search.min_guests}
                onChange={(event) => setSearch((prev) => ({ ...prev, min_guests: event.target.value }))}
              />
            </div>
            <div>
              <label className="mb-2 block text-xs font-semibold text-gray-700">Precio mínimo</label>
              <Input
                type="number"
                min={0}
                placeholder="Desde..."
                value={search.min_price}
                onChange={(event) => setSearch((prev) => ({ ...prev, min_price: event.target.value }))}
              />
            </div>
            <div>
              <label className="mb-2 block text-xs font-semibold text-gray-700">Precio máximo</label>
              <Input
                type="number"
                min={0}
                placeholder="Hasta..."
                value={search.max_price}
                onChange={(event) => setSearch((prev) => ({ ...prev, max_price: event.target.value }))}
              />
            </div>
          </div>
        </section>

        {/* Properties Section */}
        <section>
          <h3 className="mb-6 text-2xl font-bold text-neutral-900">Propiedades disponibles</h3>
          
          {loading && (
            <div className="flex justify-center py-12">
              <div className="text-center">
                <div className="mb-4 inline-block h-12 w-12 animate-spin rounded-full border-4 border-orange-200 border-t-orange-500" />
                <p className="text-sm font-medium text-neutral-700">Cargando propiedades...</p>
              </div>
            </div>
          )}

          {!loading && filteredProperties.length === 0 && (
            <Card className="bg-gradient-to-r from-orange-50 to-red-50 text-center">
              <p className="text-lg font-semibold text-neutral-700">No hay propiedades para esos filtros</p>
              <p className="mt-2 text-sm text-neutral-600">Intenta con otros criterios de búsqueda</p>
            </Card>
          )}

          {!loading && filteredProperties.length > 0 && (
            <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-3">
              {filteredProperties.map((property) => (
                <Card key={property.id} className="flex flex-col hover:scale-105 transition-transform">
                  <div className="mb-3 h-40 rounded-2xl bg-gradient-to-br from-orange-300 to-red-400" />
                  <h3 className="text-lg font-bold text-neutral-900">{property.title}</h3>
                  <p className="mt-1 text-sm text-orange-600 font-medium">{property.city}</p>
                  <p className="text-sm text-neutral-600">{property.address}</p>
                  <p className="mt-2 line-clamp-2 text-sm text-neutral-700">{property.description}</p>
                  <div className="mt-4 flex items-baseline justify-between border-t pt-4">
                    <span className="text-2xl font-bold text-orange-600">
                      {formatCurrency(property.price_per_night)}
                    </span>
                    <span className="text-sm text-neutral-600">/ noche</span>
                  </div>
                  <div className="mt-3 text-xs text-neutral-600">
                    👥 {property.max_guests} · 🛏️ {property.bedrooms} · 🚿 {property.bathrooms}
                  </div>
                  <Button variant="primary" className="mt-4 w-full">
                    Ver más
                  </Button>
                </Card>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  )
}