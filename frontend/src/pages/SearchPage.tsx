import { useState } from 'react'
import { Search, Clock, AlertCircle } from 'lucide-react'
import ImageUploader from '../components/ImageUploader'
import ImageGrid from '../components/ImageGrid'
import LoadingSpinner from '../components/LoadingSpinner'
import { searchByImage } from '../api'
import type { SearchResponse } from '../types'

export default function SearchPage() {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [results, setResults] = useState<SearchResponse | null>(null)

  const handleImageSelect = async (file: File) => {
    setIsLoading(true)
    setError(null)
    setResults(null)

    try {
      const response = await searchByImage(file, 10)
      setResults(response)
    } catch (err) {
      console.error('Search error:', err)
      setError('Failed to search for similar images. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
              <Search className="w-5 h-5 text-primary-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Reverse Image Search
              </h1>
              <p className="text-gray-500">
                Upload an image to find similar products
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Upload Section */}
        <div className="card p-6 sm:p-8">
          <ImageUploader onImageSelect={handleImageSelect} isLoading={isLoading} />
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="mt-8 text-center">
            <LoadingSpinner size="lg" className="mb-4" />
            <p className="text-gray-600">Searching for similar products...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="mt-8 p-4 bg-red-50 border border-red-200 rounded-xl flex items-start space-x-3">
            <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-medium text-red-800">Search Failed</p>
              <p className="text-sm text-red-600 mt-1">{error}</p>
            </div>
          </div>
        )}

        {/* Results Section */}
        {results && !isLoading && (
          <div className="mt-8">
            {/* Results Header */}
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-xl font-semibold text-gray-900">
                  Search Results
                </h2>
                <p className="text-sm text-gray-500 mt-1">
                  Found {results.total} similar products
                </p>
              </div>
              <div className="flex items-center text-sm text-gray-500">
                <Clock className="w-4 h-4 mr-1" />
                {results.search_time_ms.toFixed(2)}ms
              </div>
            </div>

            {/* Results Grid */}
            {results.results.length > 0 ? (
              <ImageGrid images={results.results} showScores />
            ) : (
              <div className="text-center py-12 bg-white rounded-xl border border-gray-200">
                <Search className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500">No similar products found</p>
                <p className="text-sm text-gray-400 mt-1">
                  Try uploading a different image
                </p>
              </div>
            )}
          </div>
        )}

        {/* Initial State */}
        {!results && !isLoading && !error && (
          <div className="mt-8 text-center py-12">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Search className="w-8 h-8 text-gray-400" />
            </div>
            <h3 className="text-lg font-medium text-gray-700">
              Upload an image to get started
            </h3>
            <p className="text-gray-500 mt-2 max-w-md mx-auto">
              Drag and drop an image above or click to browse.
              We'll find similar products from our catalog.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
