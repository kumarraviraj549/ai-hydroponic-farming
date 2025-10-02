'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'
import { demoData } from '@/services/api'
import { 
  PlusIcon,
  BuildingOfficeIcon,
  MapPinIcon,
  CpuChipIcon
} from '@heroicons/react/24/outline'

interface Farm {
  id: number
  name: string
  description: string
  location: string
  size_sqft: number
  farm_type: string
  sensor_count: number
}

export default function FarmsPage() {
  const { user } = useAuth()
  const [farms, setFarms] = useState<Farm[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadFarms()
  }, [])

  const loadFarms = async () => {
    try {
      // For demo purposes, use mock data
      setFarms(demoData.farms)
    } catch (error) {
      console.error('Failed to load farms:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const getFarmTypeColor = (type: string) => {
    switch (type) {
      case 'greenhouse': return 'bg-green-100 text-green-800'
      case 'vertical': return 'bg-blue-100 text-blue-800'
      case 'hydroponic': return 'bg-purple-100 text-purple-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-gray-200 rounded w-1/4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-48 bg-gray-200 rounded-xl"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">My Farms</h1>
          <p className="text-gray-600">Manage your hydroponic farming operations</p>
        </div>
        <Link href="/farms/new" className="btn btn-primary flex items-center">
          <PlusIcon className="h-5 w-5 mr-2" />
          Add New Farm
        </Link>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-green-100 rounded-full mr-4">
              <BuildingOfficeIcon className="h-6 w-6 text-green-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Total Farms</p>
              <p className="text-2xl font-bold text-gray-900">{farms.length}</p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-blue-100 rounded-full mr-4">
              <CpuChipIcon className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Total Sensors</p>
              <p className="text-2xl font-bold text-gray-900">
                {farms.reduce((sum, farm) => sum + farm.sensor_count, 0)}
              </p>
            </div>
          </div>
        </div>
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-purple-100 rounded-full mr-4">
              <MapPinIcon className="h-6 w-6 text-purple-600" />
            </div>
            <div>
              <p className="text-sm text-gray-600">Total Area</p>
              <p className="text-2xl font-bold text-gray-900">
                {farms.reduce((sum, farm) => sum + farm.size_sqft, 0).toLocaleString()} sq ft
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Farms Grid */}
      {farms.length === 0 ? (
        <div className="text-center py-12">
          <BuildingOfficeIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No farms yet</h3>
          <p className="text-gray-600 mb-6">Get started by adding your first hydroponic farm</p>
          <Link href="/farms/new" className="btn btn-primary">
            Add Your First Farm
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {farms.map((farm) => (
            <Link key={farm.id} href={`/farms/${farm.id}`}>
              <div className="card hover:shadow-lg transition-shadow duration-200 cursor-pointer">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-1">{farm.name}</h3>
                    <p className="text-sm text-gray-600 mb-2">{farm.description}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium capitalize ${getFarmTypeColor(farm.farm_type)}`}>
                    {farm.farm_type}
                  </span>
                </div>
                
                <div className="space-y-2 mb-4">
                  <div className="flex items-center text-sm text-gray-600">
                    <MapPinIcon className="h-4 w-4 mr-2" />
                    {farm.location}
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <BuildingOfficeIcon className="h-4 w-4 mr-2" />
                    {farm.size_sqft.toLocaleString()} sq ft
                  </div>
                  <div className="flex items-center text-sm text-gray-600">
                    <CpuChipIcon className="h-4 w-4 mr-2" />
                    {farm.sensor_count} sensors
                  </div>
                </div>

                <div className="flex items-center justify-between pt-4 border-t border-gray-200">
                  <span className="text-sm text-green-600 font-medium">View Details →</span>
                  <div className="flex items-center space-x-1">
                    <div className="h-2 w-2 bg-green-500 rounded-full"></div>
                    <span className="text-xs text-gray-500">Active</span>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
