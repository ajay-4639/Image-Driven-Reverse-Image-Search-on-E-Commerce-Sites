import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ChevronLeft, RefreshCw, AlertCircle } from 'lucide-react'
import ImageGrid from '../components/ImageGrid'
import LoadingSpinner from '../components/LoadingSpinner'
import { getCategoryImages } from '../api'
import type { CategoryResponse } from '../types'

export default function CategoryDetailPage() {
  const { category } = useParams<{ category: string }>()
  const [data, setData] = useState<CategoryResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [isRefreshing, setIsRefreshing] = useState(false)

  const fetchImages = async (random: boolean = false) => {
    if (!category) return

    try {
      const response = await getCategoryImages(category, 20, random)
      setData(response)
      setError(null)
    } catch (err) {
      console.error('Failed to fetch category images:', err)
      setError('Failed to load images. Please try again later.')
    }
  }

  useEffect(() => {
    setIsLoading(true)
    fetchImages().finally(() => setIsLoading(false))
  }, [category])

  const handleRefresh = async () => {
    setIsRefreshing(true)
    await fetchImages(true)
    setIsRefreshing(false)
  }

  const displayName = category?.replace('_', ' ') || 'Category'

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <Link
            to="/categories"
            className="inline-flex items-center text-gray-600 hover:text-gray-900 mb-6"
          >
            <ChevronLeft className="w-4 h-4 mr-1" />
            Back to Categories
          </Link>
          <div className="p-4 bg-red-50 border border-red-200 rounded-xl flex items-start space-x-3">
            <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-medium text-red-800">Error</p>
              <p className="text-sm text-red-600 mt-1">{error}</p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Link
            to="/categories"
            className="inline-flex items-center text-gray-600 hover:text-gray-900 mb-4"
          >
            <ChevronLeft className="w-4 h-4 mr-1" />
            Back to Categories
          </Link>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                {displayName}
              </h1>
              {data && (
                <p className="text-gray-500">
                  {data.total.toLocaleString()} products available
                </p>
              )}
            </div>
            <button
              onClick={handleRefresh}
              disabled={isRefreshing}
              className="btn-secondary"
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${isRefreshing ? 'animate-spin' : ''}`} />
              {isRefreshing ? 'Loading...' : 'Shuffle'}
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {data && data.images.length > 0 ? (
          <ImageGrid images={data.images} />
        ) : (
          <div className="text-center py-12 bg-white rounded-xl border border-gray-200">
            <p className="text-gray-500">No images found in this category</p>
          </div>
        )}
      </div>
    </div>
  )
}
