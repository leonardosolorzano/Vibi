import { Navigate, Route, Routes } from 'react-router-dom'
import { toast } from 'sonner'
import { useEffect } from 'react'
import { useAuth } from '../../features/auth/auth-context'
import { useDashboardData } from '../../features/dashboard/use-dashboard-data'
import { AppLayout } from '../../components/layout/app-layout'
import { BookingsPage } from '../../pages/bookings-page'
import { DashboardPage } from '../../pages/dashboard-page'
import { ErrorPage } from '../../pages/error-page'
import { HomePage } from '../../pages/public/home-page'
import { LoginPage } from '../../pages/login-page'
import { NotFoundPage } from '../../pages/not-found-page'
import { PropertiesPage } from '../../pages/properties-page'
import { LoadingPage } from '../../components/ui/loading-page'

function PrivateRoutes() {
  const data = useDashboardData()
  const outletContext = {
    allProperties: data.allProperties,
    myProperties: data.myProperties,
    myBookings: data.myBookings,
  }

  useEffect(() => {
    if (data.error) toast.error(data.error)
  }, [data.error])

  useEffect(() => {
    if (data.notice) toast.success(data.notice)
  }, [data.notice])

  return (
    <Routes>
      <Route
        path="/app"
        element={<AppLayout onRefresh={data.refreshData} loading={data.loading} context={outletContext} />}
      >
        <Route index element={<DashboardPage />} />
        <Route path="properties" element={<PropertiesPage onCreateProperty={data.createProperty} onCreateBooking={data.createBooking} />} />
        <Route
          path="bookings"
          element={<BookingsPage onConfirm={data.confirmBooking} onCancel={data.cancelBooking} />}
        />
      </Route>
      <Route path="/" element={<Navigate to="/app" replace />} />
      <Route path="/login" element={<Navigate to="/app" replace />} />
      <Route path="/error" element={<ErrorPage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}

export function AppRoutes() {
  const { user, loading } = useAuth()

  if (loading) return <LoadingPage message="Validando sesión..." />

  if (!user) {
    return (
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/error" element={<ErrorPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    )
  }

  return <PrivateRoutes />
}
