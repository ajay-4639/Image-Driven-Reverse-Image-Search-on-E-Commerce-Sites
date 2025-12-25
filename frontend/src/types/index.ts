export interface ImageResult {
  id: string
  path: string
  url: string
  score?: number
  category?: string
}

export interface SearchResponse {
  query_image?: string
  results: ImageResult[]
  total: number
  search_time_ms: number
}

export interface CategoryInfo {
  name: string
  display_name: string
  image_count: number
}

export interface CategoryResponse {
  category: string
  images: ImageResult[]
  total: number
}

export interface CategoriesResponse {
  categories: CategoryInfo[]
}

export interface HealthResponse {
  status: string
  model_loaded: boolean
  vector_db_connected: boolean
  indexed_images: number
  timestamp: string
}

export interface IndexingStatus {
  is_indexing: boolean
  total_images: number
  indexed_images: number
  current_category?: string
  progress_percentage: number
}

export interface ApiError {
  error: string
  message: string
  details?: Record<string, unknown>
}
