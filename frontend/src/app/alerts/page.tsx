'use client'

import { useEffect, useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { formatDistanceToNow } from 'date-fns'
import { 
  ExclamationTriangleIcon,
  InformationCircleIcon,
  XCircleIcon,
  CheckCircleIcon,
  EyeIcon,
  CheckIcon
} from '@heroicons/react/24/outline'

interface Alert {
  id: number
  title: string
  message: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  timestamp: string
  is_read: boolean
  is_resolved: boolean
  farm_name?: string
}

export default function AlertsPage() {
  const { user } = useAuth()
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [filter, setFilter] = useState<'all' | 'unread' | 'critical'>('all')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadAlerts()
  }, [])

  const loadAlerts = async () => {
    try {
      // Demo data for alerts
      const mockAlerts: Alert[] = [
        {
          id: 1,
          title: 'pH Level Critical',
          message: 'Farm A - Tomato section pH dropped to 4.2, immediate attention required',
          severity: 'critical',
          timestamp: new Date(Date.now() - 2 * 60 * 1000).toISOString(),
          is_read: false,
          is_resolved: false,
          farm_name: 'Tomato Greenhouse A'
        },
        {
          id: 2,
          title: 'Temperature High',
          message: 'Farm B - Lettuce section temperature at 28°C, check cooling system',
          severity: 'high',
          timestamp: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
          is_read: false,
          is_resolved: false,
          farm_name: 'Lettuce Vertical Farm'
        },
        {
          id: 3,
          title: 'Nutrient Level Low',
          message: 'Farm C - Herbs section nutrient solution at 20%, schedule refill',
          severity: 'medium',
          timestamp: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
          is_read: true,
          is_resolved: false,
          farm_name: 'Herbs Hydroponic Unit'
        },
        {
          id: 4,
          title: 'System Maintenance Completed',
          message: 'Farm A - Sensor calibration completed successfully',
          severity: 'low',
          timestamp: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
          is_read: true,
          is_resolved: true,
          farm_name: 'Tomato Greenhouse A'
        }
      ]
      setAlerts(mockAlerts)
    } catch (error) {
      console.error('Failed to load alerts:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const filteredAlerts = alerts.filter(alert => {
    switch (filter) {
      case 'unread':
        return !alert.is_read
      case 'critical':
        return alert.severity === 'critical' || alert.severity === 'high'
      default:
        return true
    }
  })

  const getSeverityConfig = (severity: string) => {
    switch (severity) {
      case 'critical':
        return {
          icon: XCircleIcon,
          iconColor: 'text-red-600',
          bgColor: 'bg-red-50',
          borderColor: 'border-red-200'
        }
      case 'high':
        return {
          icon: ExclamationTriangleIcon,
          iconColor: 'text-orange-600',
          bgColor: 'bg-orange-50',
          borderColor: 'border-orange-200'
        }
      case 'medium':
        return {
          icon: InformationCircleIcon,
          iconColor: 'text-yellow-600',
          bgColor: 'bg-yellow-50',
          borderColor: 'border-yellow-200'
        }
      case 'low':
        return {
          icon: CheckCircleIcon,
          iconColor: 'text-green-600',
          bgColor: 'bg-green-50',
          borderColor: 'border-green-200'
        }
      default:
        return {
          icon: InformationCircleIcon,
          iconColor: 'text-gray-600',
          bgColor: 'bg-gray-50',
          borderColor: 'border-gray-200'
        }
    }
  }

  const markAsRead = (alertId: number) => {
    setAlerts(alerts.map(alert => 
      alert.id === alertId ? { ...alert, is_read: true } : alert
    ))
  }

  const markAsResolved = (alertId: number) => {
    setAlerts(alerts.map(alert => 
      alert.id === alertId ? { ...alert, is_resolved: true, is_read: true } : alert
    ))
  }

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-gray-200 rounded w-1/4"></div>
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-24 bg-gray-200 rounded-xl"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Alerts & Notifications</h1>
        <p className="text-gray-600">Monitor and manage system alerts across all farms</p>
      </div>

      {/* Filter tabs */}
      <div className="flex space-x-1 mb-6 bg-gray-100 rounded-lg p-1">
        {[
          { key: 'all', label: 'All Alerts' },
          { key: 'unread', label: 'Unread' },
          { key: 'critical', label: 'Critical' }
        ].map((tab) => (
          <button
            key={tab.key}
            onClick={() => setFilter(tab.key as any)}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
              filter === tab.key
                ? 'bg-white text-green-700 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Alerts list */}
      {filteredAlerts.length === 0 ? (
        <div className="text-center py-12">
          <CheckCircleIcon className="h-12 w-12 text-green-500 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No alerts found</h3>
          <p className="text-gray-600">
            {filter === 'all' ? 'All systems are running normally' : `No ${filter} alerts at this time`}
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredAlerts.map((alert) => {
            const config = getSeverityConfig(alert.severity)
            const IconComponent = config.icon
            
            return (
              <div
                key={alert.id}
                className={`p-6 rounded-lg border transition-all duration-200 ${
                  alert.is_read ? 'opacity-75' : ''
                } ${config.bgColor} ${config.borderColor} ${
                  alert.is_resolved ? 'border-green-300 bg-green-50' : ''
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-4 flex-1">
                    <div className={`p-2 rounded-full ${config.iconColor}`}>
                      <IconComponent className="h-6 w-6" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center space-x-2 mb-2">
                        <h3 className="text-lg font-semibold text-gray-900">{alert.title}</h3>
                        {!alert.is_read && (
                          <span className="inline-block h-2 w-2 bg-blue-500 rounded-full"></span>
                        )}
                        {alert.is_resolved && (
                          <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">
                            Resolved
                          </span>
                        )}
                      </div>
                      <p className="text-gray-700 mb-2">{alert.message}</p>
                      <div className="flex items-center space-x-4 text-sm text-gray-500">
                        <span>{alert.farm_name}</span>
                        <span>•</span>
                        <span>{formatDistanceToNow(new Date(alert.timestamp), { addSuffix: true })}</span>
                        <span>•</span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium capitalize ${config.iconColor} ${config.bgColor}`}>
                          {alert.severity}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  {/* Actions */}
                  <div className="flex items-center space-x-2 ml-4">
                    {!alert.is_read && (
                      <button
                        onClick={() => markAsRead(alert.id)}
                        className="p-2 text-gray-400 hover:text-gray-600 transition-colors duration-200"
                        title="Mark as read"
                      >
                        <EyeIcon className="h-5 w-5" />
                      </button>
                    )}
                    {!alert.is_resolved && alert.severity !== 'low' && (
                      <button
                        onClick={() => markAsResolved(alert.id)}
                        className="p-2 text-gray-400 hover:text-green-600 transition-colors duration-200"
                        title="Mark as resolved"
                      >
                        <CheckIcon className="h-5 w-5" />
                      </button>
                    )}
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
