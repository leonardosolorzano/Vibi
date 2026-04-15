import CategoriesBar from "./CategoriesBar"
import CardPost from "../common/CardPost"
import { properties } from "../../data/properties"

const Hero = () => {
  return (
    <div>
      <CategoriesBar />
      <div className="flex flex-wrap gap-3 justify-center">
        {properties.map((property) => (
          <CardPost key={property.id} property={property} />
        ))}
      </div>
    </div>
  )
}

export default Hero;
