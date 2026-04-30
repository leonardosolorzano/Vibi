export function LoadingPage({ message = 'Cargando...' }: { message?: string }) {
  return (
    <main className="grid min-h-screen place-items-center overflow-hidden px-4">
      {/* Fondo decorativo */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-br from-orange-400 via-orange-500 to-red-600" />
      
      <section className="rounded-3xl border-0 bg-white/95 p-8 text-center shadow-2xl backdrop-blur-sm max-w-md">
        <div className="mx-auto mb-6 h-12 w-12 animate-spin rounded-full border-4 border-orange-200 border-t-orange-500" />
        <h1 className="text-2xl font-bold text-neutral-900">Un momento</h1>
        <p className="mt-3 text-sm text-neutral-600">{message}</p>
        <div className="mt-6 flex items-center justify-center gap-2">
          <div className="h-2 w-2 animate-bounce rounded-full bg-orange-500" style={{ animationDelay: '0ms' }} />
          <div className="h-2 w-2 animate-bounce rounded-full bg-orange-500" style={{ animationDelay: '150ms' }} />
          <div className="h-2 w-2 animate-bounce rounded-full bg-orange-500" style={{ animationDelay: '300ms' }} />
        </div>
      </section>
    </main>
  )
}
