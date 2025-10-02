'use client'

import { 
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
  InformationCircleIcon,
  XMarkIcon
} from '@heroicons/react/24/outline'

interface AlertProps {
  type: 'success' | 'warning' | 'error' | 'info'
  title?: string
  children: React.ReactNode
  onClose?: () => void
  className?: string
}

export function Alert({ type, title, children, onClose, className = '' }: AlertProps) {
  const config = {
    success: {
      icon: CheckCircleIcon,
      classes: 'alert-success'
    },
    warning: {
      icon: ExclamationTriangleIcon,
      classes: 'alert-warning'
    },
    error: {
      icon: XCircleIcon,
      classes: 'alert-error'
    },
    info: {
      icon: InformationCircleIcon,
      classes: 'alert-info'
    }
  }

  const { icon: IconComponent, classes } = config[type]

  return (
    <div className={`alert ${classes} ${className}`}>
      <div className="flex items-start">
        <IconComponent className="h-5 w-5 mt-0.5 mr-3 flex-shrink-0" />
        <div className="flex-1">
          {title && (
            <h4 className="font-medium mb-1">{title}</h4>
          )}
          <div className="text-sm">{children}</div>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="ml-3 flex-shrink-0"
          >
            <XMarkIcon className="h-5 w-5" />
          </button>
        )}
      </div>
    </div>
  )
}
