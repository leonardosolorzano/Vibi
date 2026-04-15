import Hero from "../components/layout/Hero"
import Navbar from "../components/layout/Navbar"
import SearchBar from "../components/layout/SearchBar"

const HomePage = () => {
  return (
    <main>
      <Navbar />

      <section className="bg-gray-100 py-3">
        <div className="max-w-7xl mx-auto px-4 sm:px-6">
          <h1 className="text-5xl md:text-7xl font-bold text-center py-8">
            Encuentra tu próxima
            <span className="text-pink-700 block">aventura</span>
          </h1>
          <SearchBar />
        </div>
      </section>

      <section className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
        <Hero />
      </section>
    </main>
  )
}

export default HomePage
