'use client'

import { useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'
import { demoData } from '@/services/api'

interface SensorData {
  temperature: { current: number; status: string; trend: string }
  humidity: { current: number; status: string; trend: string }
  pH: { current: number; status: string; trend: string }
  nutrients: { current: number; status: string; trend: string }
}

interface SensorOverviewProps {
  data: SensorData
}

export function SensorOverview({ data }: SensorOverviewProps) {
  const [selectedMetric, setSelectedMetric] = useState('temperature')
  
  const chartData = demoData.generateMockReadings(selectedMetric, 24)
  
  const metrics = [
    { key: 'temperature', name: 'Temperature', unit: '°C', color: '#ef4444' },
    { key: 'humidity', name: 'Humidity', unit: '%', color: '#3b82f6' },
    { key: 'pH', name: 'pH Level', unit: 'pH', color: '#10b981' },
    { key: 'nutrients', name: 'Nutrients', unit: 'ppm', color: '#f59e0b' }
  ]

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'normal': return 'text-green-600 bg-green-100'
      case 'warning': return 'text-yellow-600 bg-yellow-100'
      case 'critical': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up': return '↗️'
      case 'down': return '↘️'
      case 'stable': return '➡️'
      default: return '➡️'
    }
  }

  return (
    <div className="card">
      <div className="card-header">
        <h3 className="text-lg font-semibold text-gray-900">Sensor Overview</h3>
        <p className="text-sm text-gray-600">Real-time monitoring across all farms</p>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {metrics.map((metric) => {
          const sensorData = data[metric.key as keyof SensorData]
          return (
            <div 
              key={metric.key}
              className={`p-4 rounded-lg border-2 cursor-pointer transition-all duration-200 ${
                selectedMetric === metric.key 
                  ? 'border-green-500 bg-green-50' 
                  : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => setSelectedMetric(metric.key)}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-600">{metric.name}</span>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(sensorData.status)}`}>
                  {sensorData.status}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-2xl font-bold text-gray-900">
                  {sensorData.current}{metric.unit}
                </span>
                <span className="text-lg">{getTrendIcon(sensorData.trend)}</span>
              </div>
            </div>
          )
        })}
      </div>

      {/* Chart */}
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey="timestamp" 
              tickFormatter={(value) => new Date(value).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
              stroke="#666"
            />
            <YAxis stroke="#666" />
            <Tooltip 
              labelFormatter={(value) => new Date(value).toLocaleString()}
              formatter={(value: number) => [value, selectedMetric]}
            />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="value" 
              stroke={metrics.find(m => m.key === selectedMetric)?.color || '#3b82f6'}
              strokeWidth={2}
              dot={{ fill: metrics.find(m => m.key === selectedMetric)?.color || '#3b82f6', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
