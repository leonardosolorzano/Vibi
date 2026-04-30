import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from '../../features/auth/auth-context'
import { AppRoutes } from './app-routes'

export function AppRouter() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  )
}
