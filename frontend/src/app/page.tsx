'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { DashboardStats } from '@/components/dashboard/DashboardStats'
import { RecentAlerts } from '@/components/dashboard/RecentAlerts'
import { SensorOverview } from '@/components/dashboard/SensorOverview'
import { QuickActions } from '@/components/dashboard/QuickActions'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'

export default function HomePage() {
  const { user, loading } = useAuth()
  const router = useRouter()
  const [dashboardData, setDashboardData] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    if (!loading && !user) {
      router.push('/auth/login')
      return
    }

    if (user) {
      // Load dashboard data
      loadDashboardData()
    }
  }, [user, loading, router])

  const loadDashboardData = async () => {
    try {
      setIsLoading(true)
      // This would typically fetch from your API
      // For demo purposes, we'll use mock data
      const mockData = {
        stats: {
          totalFarms: 3,
          activeSensors: 12,
          alertsToday: 5,
          avgYield: 92.5
        },
        recentAlerts: [
          {
            id: 1,
            title: 'pH Level Critical',
            message: 'Farm A - Tomato section pH dropped to 4.2',
            severity: 'critical',
            timestamp: new Date(Date.now() - 2 * 60 * 1000).toISOString()
          },
          {
            id: 2,
            title: 'Temperature High',
            message: 'Farm B - Lettuce section temperature at 28°C',
            severity: 'high',
            timestamp: new Date(Date.now() - 15 * 60 * 1000).toISOString()
          }
        ],
        sensorOverview: {
          temperature: { current: 24.5, status: 'normal', trend: 'stable' },
          humidity: { current: 65, status: 'normal', trend: 'up' },
          pH: { current: 6.2, status: 'warning', trend: 'down' },
          nutrients: { current: 850, status: 'normal', trend: 'stable' }
        }
      }
      
      setDashboardData(mockData)
    } catch (error) {
      console.error('Failed to load dashboard data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  if (loading || isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="large" />
      </div>
    )
  }

  if (!user) {
    return null // Will redirect to login
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Welcome back, {user.name}! 👋
        </h1>
        <p className="text-gray-600">
          Here's an overview of your hydroponic farming operations
        </p>
      </div>

      {dashboardData && (
        <div className="space-y-8">
          {/* Dashboard Stats */}
          <DashboardStats stats={dashboardData.stats} />

          {/* Main Dashboard Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Sensor Overview - Takes 2 columns on large screens */}
            <div className="lg:col-span-2">
              <SensorOverview data={dashboardData.sensorOverview} />
            </div>

            {/* Recent Alerts */}
            <div>
              <RecentAlerts alerts={dashboardData.recentAlerts} />
            </div>
          </div>

          {/* Quick Actions */}
          <QuickActions />
        </div>
      )}
    </div>
  )
}
