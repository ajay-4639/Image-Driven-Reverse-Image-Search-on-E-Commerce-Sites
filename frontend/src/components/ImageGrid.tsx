import { useState } from 'react'
import { ExternalLink, ZoomIn } from 'lucide-react'
import type { ImageResult } from '../types'
import { cn } from '../utils/cn'
import ImageModal from './ImageModal'

interface ImageGridProps {
  images: ImageResult[]
  showScores?: boolean
}

export default function ImageGrid({ images, showScores = false }: ImageGridProps) {
  const [selectedImage, setSelectedImage] = useState<ImageResult | null>(null)

  if (images.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No images to display</p>
      </div>
    )
  }

  return (
    <>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        {images.map((image) => (
          <div
            key={image.id}
            className="group card overflow-hidden cursor-pointer hover:shadow-lg transition-all duration-200"
            onClick={() => setSelectedImage(image)}
          >
            <div className="relative aspect-square bg-gray-100">
              <img
                src={image.url}
                alt={`Product ${image.id}`}
                className="w-full h-full object-cover"
                loading="lazy"
                onError={(e) => {
                  const target = e.target as HTMLImageElement
                  target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"%3E%3Crect fill="%23f3f4f6" width="100" height="100"/%3E%3Ctext fill="%239ca3af" font-family="sans-serif" font-size="14" x="50" y="50" text-anchor="middle" dy=".3em"%3ENo Image%3C/text%3E%3C/svg%3E'
                }}
              />
              <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors flex items-center justify-center">
                <ZoomIn className="w-8 h-8 text-white opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
              {showScores && image.score !== undefined && (
                <div className="absolute top-2 right-2 px-2 py-1 bg-primary-600 text-white text-xs font-medium rounded-full">
                  {(image.score * 100).toFixed(1)}%
                </div>
              )}
            </div>
            {image.category && (
              <div className="p-2">
                <span className="text-xs text-gray-500">
                  {image.category.replace('_', ' ')}
                </span>
              </div>
            )}
          </div>
        ))}
      </div>

      {selectedImage && (
        <ImageModal
          image={selectedImage}
          onClose={() => setSelectedImage(null)}
        />
      )}
    </>
  )
}
