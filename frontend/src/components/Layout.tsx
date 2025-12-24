import { Outlet, Link, useLocation } from 'react-router-dom'

export function Layout() {
  const location = useLocation()

  const isActive = (path: string) => location.pathname === path

  return (
    <div className="min-h-screen bg-harpia-darker">
      {/* Header */}
      <header className="border-b border-harpia-gray/20 bg-harpia-dark/50 backdrop-blur-lg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center gap-2">
              <span className="text-3xl">🦅</span>
              <span className="text-xl font-bold harpia-gradient-text">Harpia</span>
            </Link>

            {/* Navigation */}
            <nav className="flex items-center gap-6">
              <Link
                to="/"
                className={`text-sm font-medium transition-colors ${
                  isActive('/') ? 'text-harpia-blue' : 'text-harpia-gray hover:text-white'
                }`}
              >
                Home
              </Link>
              <Link
                to="/chat"
                className={`text-sm font-medium transition-colors ${
                  isActive('/chat') ? 'text-harpia-blue' : 'text-harpia-gray hover:text-white'
                }`}
              >
                Análise
              </Link>
              <Link
                to="/dashboard"
                className={`text-sm font-medium transition-colors ${
                  isActive('/dashboard') ? 'text-harpia-blue' : 'text-harpia-gray hover:text-white'
                }`}
              >
                Dashboard
              </Link>
              <Link
                to="/chat"
                className="harpia-btn-primary text-sm"
              >
                Começar Grátis
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main>
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t border-harpia-gray/20 bg-harpia-dark/50 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <span className="text-2xl">🦅</span>
              <span className="text-lg font-semibold">Harpia</span>
              <span className="text-harpia-gray text-sm">- Fazendo a IA recomendar você</span>
            </div>
            <div className="text-harpia-gray text-sm">
              © 2024 Harpia. Todos os direitos reservados.
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
