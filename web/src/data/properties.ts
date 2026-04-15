export type Property = {
  id: string
  location: string
  title: string
  description: string
  price: number
  rating: number
  guests: string
  image: string
  amenities: string[]
}

export const properties: Property[] = [
  {
    id: "1",
    location: "Ayampe, Ecuador",
    title: "Hacienda Hostales",
    description: "Descubre la belleza de la naturaleza en este acogedor hostal con piscina y zonas de descanso.",
    price: 100,
    rating: 4.9,
    guests: "2 huéspedes · 1 cama · 1 baño",
    image: "https://images.trvl-media.com/lodging/8000000/7650000/7641200/7641167/77e7b4a0.jpg?impolicy=resizecrop&rw=575&rh=575&ra=fill",
    amenities: ["Wi-Fi", "Piscina", "Desayuno incluido"],
  },
  {
    id: "2",
    location: "Baños, Ecuador",
    title: "Cabaña Montaña Verde",
    description: "Relájate en una cabaña rústica rodeada de naturaleza y vistas a las montañas.",
    price: 85,
    rating: 4.7,
    guests: "4 huéspedes · 2 camas · 1 baño",
    image: "https://cf.bstatic.com/xdata/images/hotel/max1024x768/770812553.webp?k=3996af4f530cd8df382a8bb0ad350d165ef4c5138e857c2f2ee988afa0e36519&o=",
    amenities: ["Cocina", "Terraza", "Parking gratis"],
  },
  {
    id: "3",
    location: "Quito, Ecuador",
    title: "Apartamento Central",
    description: "Disfruta de un apartamento moderno en el centro, cerca de restaurantes y vida nocturna.",
    price: 120,
    rating: 4.8,
    guests: "3 huéspedes · 2 camas · 1 baño",
    image: "https://www.cruzescalanteconstructores.com/wp-content/uploads/2021/07/Departamentos-en-Quito-Norte-edificio-Cataleya.jpg",
    amenities: ["Aire acondicionado", "Lavadora", "Smart TV"],
  },
]
