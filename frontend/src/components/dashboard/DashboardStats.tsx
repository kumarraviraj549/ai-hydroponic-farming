'use client'

import { 
  BuildingOfficeIcon,
  CpuChipIcon,
  ExclamationTriangleIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline'

interface StatsProps {
  stats: {
    totalFarms: number
    activeSensors: number
    alertsToday: number
    avgYield: number
  }
}

export function DashboardStats({ stats }: StatsProps) {
  const statCards = [
    {
      title: 'Total Farms',
      value: stats.totalFarms,
      icon: BuildingOfficeIcon,
      color: 'green',
      change: '+2 this month'
    },
    {
      title: 'Active Sensors',
      value: stats.activeSensors,
      icon: CpuChipIcon,
      color: 'blue',
      change: '100% uptime'
    },
    {
      title: 'Alerts Today',
      value: stats.alertsToday,
      icon: ExclamationTriangleIcon,
      color: stats.alertsToday > 5 ? 'red' : 'yellow',
      change: '-2 vs yesterday'
    },
    {
      title: 'Avg Yield',
      value: `${stats.avgYield}%`,
      icon: ChartBarIcon,
      color: 'green',
      change: '+5.2% vs last month'
    }
  ]

  const getColorClasses = (color: string) => {
    switch (color) {
      case 'green':
        return 'bg-green-100 text-green-600'
      case 'blue':
        return 'bg-blue-100 text-blue-600'
      case 'yellow':
        return 'bg-yellow-100 text-yellow-600'
      case 'red':
        return 'bg-red-100 text-red-600'
      default:
        return 'bg-gray-100 text-gray-600'
    }
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {statCards.map((stat, index) => {
        const IconComponent = stat.icon
        const colorClasses = getColorClasses(stat.color)
        
        return (
          <div key={index} className="card hover:shadow-md transition-shadow duration-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">{stat.value}</p>
                <p className="text-sm text-gray-500 mt-1">{stat.change}</p>
              </div>
              <div className={`p-3 rounded-full ${colorClasses}`}>
                <IconComponent className="h-6 w-6" />
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
