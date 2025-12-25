import apiClient from './client'
import type { SearchResponse } from '../types'

export async function searchByImage(
  file: File,
  limit: number = 5
): Promise<SearchResponse> {
  const formData = new FormData()
  formData.append('image', file)

  const response = await apiClient.post<SearchResponse>(`/search?limit=${limit}`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

export async function searchByUrl(
  imageUrl: string,
  limit: number = 5
): Promise<SearchResponse> {
  const response = await apiClient.post<SearchResponse>('/search/url', null, {
    params: { image_url: imageUrl, limit },
  })

  return response.data
}
