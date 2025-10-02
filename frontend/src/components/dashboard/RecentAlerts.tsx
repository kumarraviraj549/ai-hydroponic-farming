'use client'

import { formatDistanceToNow } from 'date-fns'
import { 
  ExclamationTriangleIcon,
  InformationCircleIcon,
  XCircleIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline'

interface Alert {
  id: number
  title: string
  message: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  timestamp: string
}

interface RecentAlertsProps {
  alerts: Alert[]
}

export function RecentAlerts({ alerts }: RecentAlertsProps) {
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

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="text-lg font-semibold text-gray-900">Recent Alerts</h3>
        <p className="text-sm text-gray-600">Latest notifications from your farms</p>
      </div>

      {alerts.length === 0 ? (
        <div className="text-center py-8">
          <CheckCircleIcon className="h-12 w-12 text-green-500 mx-auto mb-4" />
          <h4 className="text-lg font-medium text-gray-900 mb-2">All systems normal</h4>
          <p className="text-gray-600">No alerts at this time</p>
        </div>
      ) : (
        <div className="space-y-4">
          {alerts.map((alert) => {
            const config = getSeverityConfig(alert.severity)
            const IconComponent = config.icon
            
            return (
              <div
                key={alert.id}
                className={`p-4 rounded-lg border ${config.bgColor} ${config.borderColor} hover:shadow-sm transition-shadow duration-200`}
              >
                <div className="flex items-start space-x-3">
                  <div className={`p-1 rounded-full ${config.iconColor}`}>
                    <IconComponent className="h-5 w-5" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <h4 className="text-sm font-medium text-gray-900 truncate">
                        {alert.title}
                      </h4>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium capitalize ${config.iconColor} ${config.bgColor}`}>
                        {alert.severity}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{alert.message}</p>
                    <p className="text-xs text-gray-500">
                      {formatDistanceToNow(new Date(alert.timestamp), { addSuffix: true })}
                    </p>
                  </div>
                </div>
              </div>
            )
          })}
          
          <div className="pt-4 border-t border-gray-200">
            <button className="w-full text-sm text-green-600 hover:text-green-700 font-medium">
              View all alerts →
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
