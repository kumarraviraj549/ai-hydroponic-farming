import axios, { AxiosInstance, AxiosResponse, AxiosError } from 'axios'

// Create axios instance with base configuration
export const apiClient: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Handle response errors
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response
  },
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      // Unauthorized - redirect to login
      localStorage.removeItem('authToken')
      window.location.href = '/auth/login'
    }
    return Promise.reject(error)
  }
)

// API endpoints
export const api = {
  // Authentication
  auth: {
    login: (email: string, password: string) =>
      apiClient.post('/auth/login', { email, password }),
    register: (userData: any) =>
      apiClient.post('/auth/register', userData),
    logout: () =>
      apiClient.post('/auth/logout'),
  },

  // Farms
  farms: {
    getAll: () => apiClient.get('/farms'),
    getById: (id: number) => apiClient.get(`/farms/${id}`),
    create: (farmData: any) => apiClient.post('/farms', farmData),
    update: (id: number, farmData: any) => apiClient.put(`/farms/${id}`, farmData),
    delete: (id: number) => apiClient.delete(`/farms/${id}`),
  },

  // Sensors
  sensors: {
    getByFarm: (farmId: number) => apiClient.get(`/farms/${farmId}/sensors`),
    create: (farmId: number, sensorData: any) => 
      apiClient.post(`/farms/${farmId}/sensors`, sensorData),
    update: (sensorId: number, sensorData: any) => 
      apiClient.put(`/sensors/${sensorId}`, sensorData),
    delete: (sensorId: number) => apiClient.delete(`/sensors/${sensorId}`),
  },

  // Sensor Readings
  readings: {
    getBySensor: (sensorId: number, params?: any) =>
      apiClient.get(`/sensors/${sensorId}/readings`, { params }),
    getByFarm: (farmId: number, params?: any) =>
      apiClient.get(`/farms/${farmId}/readings`, { params }),
    create: (sensorId: number, reading: any) =>
      apiClient.post(`/sensors/${sensorId}/readings`, reading),
    getLatest: (farmId: number) =>
      apiClient.get(`/farms/${farmId}/readings/latest`),
  },

  // Recommendations
  recommendations: {
    getByFarm: (farmId: number) => apiClient.get(`/farms/${farmId}/recommendations`),
    generate: (farmId: number) => apiClient.post(`/farms/${farmId}/recommendations/generate`),
    markImplemented: (recommendationId: number) =>
      apiClient.patch(`/recommendations/${recommendationId}/implement`),
  },

  // Alerts
  alerts: {
    getByFarm: (farmId: number) => apiClient.get(`/farms/${farmId}/alerts`),
    markRead: (alertId: number) => apiClient.patch(`/alerts/${alertId}/read`),
    markResolved: (alertId: number) => apiClient.patch(`/alerts/${alertId}/resolve`),
    getUnread: () => apiClient.get('/alerts/unread'),
  },

  // Dashboard
  dashboard: {
    getStats: () => apiClient.get('/dashboard/stats'),
    getOverview: (farmId?: number) => 
      apiClient.get('/dashboard/overview', { params: { farmId } }),
  },

  // Health check
  health: {
    check: () => apiClient.get('/health'),
  },
}

// Demo data fallbacks for when API is not available
export const demoData = {
  farms: [
    {
      id: 1,
      name: 'Tomato Greenhouse A',
      description: 'Main tomato production facility',
      location: 'Sector 1, Building A',
      size_sqft: 2500,
      farm_type: 'greenhouse',
      sensor_count: 8
    },
    {
      id: 2,
      name: 'Lettuce Vertical Farm',
      description: 'Vertical lettuce growing system',
      location: 'Sector 2, Building B',
      size_sqft: 1200,
      farm_type: 'vertical',
      sensor_count: 6
    },
    {
      id: 3,
      name: 'Herbs Hydroponic Unit',
      description: 'Basil, mint and cilantro production',
      location: 'Sector 3, Building C',
      size_sqft: 800,
      farm_type: 'hydroponic',
      sensor_count: 4
    }
  ],

  sensors: [
    { id: 1, name: 'pH Sensor 1', sensor_type: 'ph', unit: 'pH', farm_id: 1 },
    { id: 2, name: 'Temperature Sensor 1', sensor_type: 'temperature', unit: '°C', farm_id: 1 },
    { id: 3, name: 'Humidity Sensor 1', sensor_type: 'humidity', unit: '%', farm_id: 1 },
    { id: 4, name: 'Nutrient Sensor 1', sensor_type: 'nutrients', unit: 'ppm', farm_id: 1 },
  ],

  generateMockReadings: (sensorType: string, hours = 24) => {
    const readings = []
    const now = new Date()
    
    for (let i = hours; i >= 0; i--) {
      const timestamp = new Date(now.getTime() - i * 60 * 60 * 1000)
      let value
      
      switch (sensorType) {
        case 'temperature':
          value = 22 + Math.sin(i * 0.2) * 3 + Math.random() * 2
          break
        case 'humidity':
          value = 65 + Math.sin(i * 0.15) * 10 + Math.random() * 5
          break
        case 'ph':
          value = 6.2 + Math.sin(i * 0.1) * 0.3 + Math.random() * 0.2
          break
        case 'nutrients':
          value = 850 + Math.sin(i * 0.12) * 50 + Math.random() * 20
          break
        default:
          value = Math.random() * 100
      }
      
      readings.push({
        timestamp: timestamp.toISOString(),
        value: Number(value.toFixed(2))
      })
    }
    
    return readings
  }
}
