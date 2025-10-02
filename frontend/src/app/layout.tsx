import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from './providers'
import { Navbar } from '@/components/layout/Navbar'
import { AuthProvider } from '@/providers/AuthProvider'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'HydroAI - AI-Powered Hydroponic Farming',
  description: 'Optimize your hydroponic farming operations with AI-powered insights, real-time monitoring, and predictive analytics.',
  keywords: ['hydroponics', 'AI', 'farming', 'agriculture', 'IoT', 'sensors', 'automation'],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <Providers>
            <div className="min-h-screen bg-gray-50">
              <Navbar />
              <main className="">
                {children}
              </main>
            </div>
          </Providers>
        </AuthProvider>
      </body>
    </html>
  )
}
