import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, X, Image as ImageIcon } from 'lucide-react'
import { cn } from '../utils/cn'

interface ImageUploaderProps {
  onImageSelect: (file: File) => void
  isLoading?: boolean
}

export default function ImageUploader({ onImageSelect, isLoading }: ImageUploaderProps) {
  const [preview, setPreview] = useState<string | null>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (file) {
      setSelectedFile(file)
      const reader = new FileReader()
      reader.onload = () => {
        setPreview(reader.result as string)
      }
      reader.readAsDataURL(file)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'],
    },
    maxFiles: 1,
    disabled: isLoading,
  })

  const handleClear = () => {
    setPreview(null)
    setSelectedFile(null)
  }

  const handleSearch = () => {
    if (selectedFile) {
      onImageSelect(selectedFile)
    }
  }

  return (
    <div className="w-full max-w-xl mx-auto">
      {!preview ? (
        <div
          {...getRootProps()}
          className={cn(
            'border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-200',
            isDragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50',
            isLoading && 'opacity-50 cursor-not-allowed'
          )}
        >
          <input {...getInputProps()} />
          <div className="flex flex-col items-center space-y-4">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center">
              <Upload className="w-8 h-8 text-gray-400" />
            </div>
            <div>
              <p className="text-lg font-medium text-gray-700">
                {isDragActive ? 'Drop your image here' : 'Drag & drop an image'}
              </p>
              <p className="text-sm text-gray-500 mt-1">
                or click to browse from your device
              </p>
            </div>
            <div className="flex flex-wrap justify-center gap-2 text-xs text-gray-400">
              <span className="px-2 py-1 bg-gray-100 rounded">PNG</span>
              <span className="px-2 py-1 bg-gray-100 rounded">JPG</span>
              <span className="px-2 py-1 bg-gray-100 rounded">JPEG</span>
              <span className="px-2 py-1 bg-gray-100 rounded">GIF</span>
              <span className="px-2 py-1 bg-gray-100 rounded">WebP</span>
            </div>
          </div>
        </div>
      ) : (
        <div className="card p-4">
          <div className="relative">
            <img
              src={preview}
              alt="Preview"
              className="w-full max-h-64 object-contain rounded-lg bg-gray-100"
            />
            <button
              onClick={handleClear}
              disabled={isLoading}
              className="absolute top-2 right-2 p-1.5 bg-white rounded-full shadow-md hover:bg-gray-100 transition-colors"
            >
              <X className="w-4 h-4 text-gray-600" />
            </button>
          </div>
          <div className="mt-4 flex items-center justify-between">
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <ImageIcon className="w-4 h-4" />
              <span className="truncate max-w-[200px]">{selectedFile?.name}</span>
            </div>
            <button
              onClick={handleSearch}
              disabled={isLoading}
              className="btn-primary"
            >
              {isLoading ? (
                <>
                  <span className="loading-dots">Searching</span>
                </>
              ) : (
                'Search Similar'
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
