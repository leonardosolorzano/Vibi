import { Link, useParams } from "react-router-dom"
import { ArrowLeft, Star, MapPin, Users, CheckCircle2, Share, Heart } from "lucide-react"
import Navbar from "./Navbar"
import { properties } from "../../data/properties"

const PropertyDetail = () => {
  const { id } = useParams<{ id: string }>()
  const property = properties.find((item) => item.id === id)

  if (!property) {
    // Mantengo tu estado de error pero con el color de marca
    return (
      <div className="min-h-screen bg-white">
        <Navbar />
        <main className="max-w-6xl mx-auto px-4 py-20 text-center">
          <h1 className="text-2xl font-bold">Ups, no encontramos ese lugar</h1>
          <Link to="/" className="mt-4 inline-block text-[#E21C5F] font-semibold underline">
            Volver a explorar
          </Link>
        </main>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-white">
      <Navbar />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Cabecera: Título y Acciones */}
        <div className="mb-6">
          <Link to="/" className="flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-black mb-4 transition-colors">
            <ArrowLeft size={16} /> Volver a los resultados
          </Link>
          
          <div className="flex justify-between items-end">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{property.title}</h1>
              <div className="flex items-center gap-4 mt-2 text-sm font-semibold">
                <div className="flex items-center gap-1">
                  <Star size={14} className="fill-black" />
                  <span>{property.rating} · 12 reseñas</span>
                </div>
                <div className="flex items-center gap-1 underline cursor-pointer">
                  <MapPin size={14} />
                  <span>{property.location}</span>
                </div>
              </div>
            </div>
            
            <div className="hidden sm:flex gap-4">
              <button className="flex items-center gap-2 text-sm font-semibold underline hover:bg-gray-100 px-3 py-2 rounded-lg transition-colors">
                <Share size={16} /> Compartir
              </button>
              <button className="flex items-center gap-2 text-sm font-semibold underline hover:bg-gray-100 px-3 py-2 rounded-lg transition-colors">
                <Heart size={16} /> Guardar
              </button>
            </div>
          </div>
        </div>

        {/* Galería: Diseño de "Hero" (1 grande, el resto ocultas o en grid) */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-2 h-[300px] md:h-[450px] rounded-2xl overflow-hidden mb-8">
          <div className="md:col-span-2 md:row-span-2">
            <img src={property.image} className="w-full h-full object-cover hover:brightness-90 transition-all cursor-pointer" alt="Main" />
          </div>
          <div className="hidden md:block">
            <img src={property.image} className="w-full h-full object-cover hover:brightness-90 transition-all cursor-pointer" alt="Extra 1" />
          </div>
          <div className="hidden md:block">
            <img src={property.image} className="w-full h-full object-cover hover:brightness-90 transition-all cursor-pointer" alt="Extra 2" />
          </div>
          <div className="hidden md:block">
            <img src={property.image} className="w-full h-full object-cover hover:brightness-90 transition-all cursor-pointer" alt="Extra 3" />
          </div>
          <div className="hidden md:block">
            <img src={property.image} className="w-full h-full object-cover hover:brightness-90 transition-all cursor-pointer" alt="Extra 4" />
          </div>
        </div>

        {/* Contenido Principal + Sidebar Sticky */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
          
          {/* Columna Izquierda: Información */}
          <div className="lg:col-span-2">
            <div className="flex justify-between items-center pb-6 border-b">
              <div>
                <h2 className="text-2xl font-semibold">Anfitrión: Gestionado por Vibi</h2>
                <p className="text-gray-600">{property.guests} huéspedes · 1 dormitorio · 1 baño</p>
              </div>
              <div className="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center">
                <Users className="text-gray-500" />
              </div>
            </div>

            <div className="py-8 border-b">
              <h3 className="text-xl font-semibold mb-4">Sobre este lugar</h3>
              <p className="text-gray-700 leading-relaxed text-lg font-light">
                {property.description}
              </p>
            </div>

            <div className="py-8">
              <h3 className="text-xl font-semibold mb-6">Lo que este lugar ofrece</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {property.amenities.map((amenity) => (
                  <div key={amenity} className="flex items-center gap-4 text-gray-700">
                    <CheckCircle2 size={20} className="text-gray-400" />
                    <span className="text-base">{amenity}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Columna Derecha: Tarjeta de Reserva (Sticky) */}
          <aside className="relative">
            <div className="sticky top-28 border border-gray-200 rounded-2xl p-6 shadow-xl bg-white">
              <div className="flex justify-between items-baseline mb-6">
                <div>
                  <span className="text-2xl font-bold">${property.price}</span>
                  <span className="text-gray-600"> noche</span>
                </div>
                <div className="flex items-center gap-1 text-sm font-semibold">
                  <Star size={14} className="fill-black" />
                  <span>{property.rating}</span>
                </div>
              </div>

              {/* Simulador de Inputs */}
              <div className="border border-gray-400 rounded-xl overflow-hidden mb-4">
                <div className="grid grid-cols-2 border-b border-gray-400">
                  <div className="p-3 border-r border-gray-400">
                    <label className="block text-[10px] font-bold uppercase">Llegada</label>
                    <input type="text" placeholder="Añadir fecha" className="text-sm w-full outline-none" />
                  </div>
                  <div className="p-3">
                    <label className="block text-[10px] font-bold uppercase">Salida</label>
                    <input type="text" placeholder="Añadir fecha" className="text-sm w-full outline-none" />
                  </div>
                </div>
                <div className="p-3">
                  <label className="block text-[10px] font-bold uppercase">Huéspedes</label>
                  <select className="text-sm w-full outline-none bg-transparent">
                    <option>1 huésped</option>
                    <option>2 huéspedes</option>
                  </select>
                </div>
              </div>

              <button className="w-full bg-[#E21C5F] hover:bg-[#D11152] text-white font-bold py-3 rounded-xl transition-all active:scale-[0.98]">
                Reservar ahora
              </button>

              <p className="text-center text-sm text-gray-500 mt-4">No se te cobrará nada aún</p>
            </div>
          </aside>

        </div>
      </main>
    </div>
  )
}

export default PropertyDetail
