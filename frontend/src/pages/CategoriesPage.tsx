import { useEffect, useState } from 'react'
import { Grid3X3, AlertCircle } from 'lucide-react'
import CategoryCard from '../components/CategoryCard'
import LoadingSpinner from '../components/LoadingSpinner'
import { getCategories } from '../api'
import type { CategoryInfo } from '../types'

export default function CategoriesPage() {
  const [categories, setCategories] = useState<CategoryInfo[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchCategories() {
      try {
        const response = await getCategories()
        setCategories(response.categories)
      } catch (err) {
        console.error('Failed to fetch categories:', err)
        setError('Failed to load categories. Please try again later.')
      } finally {
        setIsLoading(false)
      }
    }

    fetchCategories()
  }, [])

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
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
              <Grid3X3 className="w-5 h-5 text-primary-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Product Categories
              </h1>
              <p className="text-gray-500">
                Browse products by category
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
          <div className="card p-4 text-center">
            <p className="text-2xl font-bold text-gray-900">
              {categories.length}
            </p>
            <p className="text-sm text-gray-500">Categories</p>
          </div>
          <div className="card p-4 text-center">
            <p className="text-2xl font-bold text-gray-900">
              {categories.reduce((acc, cat) => acc + cat.image_count, 0).toLocaleString()}
            </p>
            <p className="text-sm text-gray-500">Total Products</p>
          </div>
        </div>

        {/* Categories Grid */}
        {categories.length > 0 ? (
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {categories.map((category) => (
              <CategoryCard key={category.name} category={category} />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 bg-white rounded-xl border border-gray-200">
            <Grid3X3 className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">No categories available</p>
          </div>
        )}
      </div>
    </div>
  )
}
