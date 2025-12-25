import { useEffect } from 'react'
import { X, Download, ExternalLink } from 'lucide-react'
import type { ImageResult } from '../types'

interface ImageModalProps {
  image: ImageResult
  onClose: () => void
}

export default function ImageModal({ image, onClose }: ImageModalProps) {
  // Close on escape key
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    window.addEventListener('keydown', handleEsc)
    return () => window.removeEventListener('keydown', handleEsc)
  }, [onClose])

  // Prevent body scroll when modal is open
  useEffect(() => {
    document.body.style.overflow = 'hidden'
    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [])

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4"
      onClick={onClose}
    >
      <div
        className="relative max-w-4xl w-full bg-white rounded-xl overflow-hidden shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              Product Image
            </h3>
            {image.category && (
              <p className="text-sm text-gray-500">
                {image.category.replace('_', ' ')}
              </p>
            )}
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="w-5 h-5 text-gray-600" />
          </button>
        </div>

        {/* Image */}
        <div className="relative bg-gray-100">
          <img
            src={image.url}
            alt={`Product ${image.id}`}
            className="w-full max-h-[70vh] object-contain"
          />
          {image.score !== undefined && (
            <div className="absolute top-4 right-4 px-3 py-1.5 bg-primary-600 text-white text-sm font-medium rounded-full">
              Similarity: {(image.score * 100).toFixed(1)}%
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between p-4 border-t border-gray-200 bg-gray-50">
          <div className="text-sm text-gray-500">
            ID: {image.id}
          </div>
          <div className="flex items-center space-x-2">
            <a
              href={image.url}
              download
              className="btn-secondary flex items-center"
            >
              <Download className="w-4 h-4 mr-2" />
              Download
            </a>
            <a
              href={image.url}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-primary flex items-center"
            >
              <ExternalLink className="w-4 h-4 mr-2" />
              Open
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
