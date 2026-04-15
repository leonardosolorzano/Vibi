import { Heart, Star } from "lucide-react"
import { Link } from "react-router-dom"
import type { Property } from "../../data/properties"

interface CardPostProps {
  property: Property
}

const CardPost = ({ property }: CardPostProps) => {
  return (
    <Link
      to={`/propiedad/${property.id}`}
      className="flex flex-col gap-1 group cursor-pointer w-full max-w-[320px]"
    >
      <div className="relative aspect-[4/3] w-full overflow-hidden rounded-xl mb-2">
        <img
          src={property.image}
          alt={property.title}
          className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
        />

        <div className="absolute top-3 right-3 rounded-full bg-white/90 p-2 text-pink-600 shadow-sm transition-transform duration-200 group-hover:scale-110">
          <Heart size={24} strokeWidth={2} />
        </div>
      </div>

      <div className="flex justify-between items-start px-1">
        <div className="flex flex-col">
          <h2 className="font-semibold text-base text-gray-900">{property.location}</h2>
          <span className="text-gray-500 text-sm">{property.title}</span>
          <p className="text-gray-500 text-sm line-clamp-1 mt-0.5">{property.description}</p>
          <div className="mt-2 text-sm">
            <span className="font-semibold text-black">${property.price}</span>
            <span className="text-gray-800"> noche</span>
          </div>
        </div>

        <div className="flex items-center gap-1 text-sm text-gray-900">
          <Star size={14} className="fill-current" />
          <span>{property.rating}</span>
        </div>
      </div>
    </Link>
  )
}

export default CardPost;