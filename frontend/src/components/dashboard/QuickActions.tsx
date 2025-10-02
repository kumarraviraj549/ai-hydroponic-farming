'use client'

import Link from 'next/link'
import { 
  PlusIcon,
  CogIcon,
  DocumentArrowDownIcon,
  BellIcon,
  ChartBarIcon,
  WrenchScrewdriverIcon
} from '@heroicons/react/24/outline'

const quickActions = [
  {
    title: 'Add New Farm',
    description: 'Set up a new hydroponic farming operation',
    href: '/farms/new',
    icon: PlusIcon,
    color: 'green'
  },
  {
    title: 'Configure Sensors',
    description: 'Manage and calibrate your IoT sensors',
    href: '/sensors',
    icon: CogIcon,
    color: 'blue'
  },
  {
    title: 'Generate Report',
    description: 'Download performance and analytics reports',
    href: '/reports',
    icon: DocumentArrowDownIcon,
    color: 'purple'
  },
  {
    title: 'Alert Settings',
    description: 'Customize notification preferences',
    href: '/settings/alerts',
    icon: BellIcon,
    color: 'orange'
  },
  {
    title: 'View Analytics',
    description: 'Deep dive into farm performance data',
    href: '/analytics',
    icon: ChartBarIcon,
    color: 'indigo'
  },
  {
    title: 'System Maintenance',
    description: 'Schedule and manage maintenance tasks',
    href: '/maintenance',
    icon: WrenchScrewdriverIcon,
    color: 'gray'
  }
]

export function QuickActions() {
  const getColorClasses = (color: string) => {
    switch (color) {
      case 'green':
        return 'bg-green-100 text-green-600 hover:bg-green-200'
      case 'blue':
        return 'bg-blue-100 text-blue-600 hover:bg-blue-200'
      case 'purple':
        return 'bg-purple-100 text-purple-600 hover:bg-purple-200'
      case 'orange':
        return 'bg-orange-100 text-orange-600 hover:bg-orange-200'
      case 'indigo':
        return 'bg-indigo-100 text-indigo-600 hover:bg-indigo-200'
      case 'gray':
        return 'bg-gray-100 text-gray-600 hover:bg-gray-200'
      default:
        return 'bg-gray-100 text-gray-600 hover:bg-gray-200'
    }
  }

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="text-lg font-semibold text-gray-900">Quick Actions</h3>
        <p className="text-sm text-gray-600">Frequently used operations</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {quickActions.map((action, index) => {
          const IconComponent = action.icon
          const colorClasses = getColorClasses(action.color)
          
          return (
            <Link
              key={index}
              href={action.href}
              className="block p-4 rounded-lg border border-gray-200 hover:border-gray-300 hover:shadow-sm transition-all duration-200 group"
            >
              <div className="flex items-start space-x-3">
                <div className={`p-2 rounded-lg transition-colors duration-200 ${colorClasses}`}>
                  <IconComponent className="h-5 w-5" />
                </div>
                <div className="flex-1 min-w-0">
                  <h4 className="text-sm font-medium text-gray-900 group-hover:text-green-600 transition-colors duration-200">
                    {action.title}
                  </h4>
                  <p className="text-sm text-gray-600 mt-1">
                    {action.description}
                  </p>
                </div>
              </div>
            </Link>
          )
        })}
      </div>
    </div>
  )
}
