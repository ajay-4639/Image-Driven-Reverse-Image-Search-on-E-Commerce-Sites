import apiClient from './client'
import type { CategoriesResponse, CategoryResponse } from '../types'

export async function getCategories(): Promise<CategoriesResponse> {
  const response = await apiClient.get<CategoriesResponse>('/categories')
  return response.data
}

export async function getCategoryImages(
  category: string,
  limit: number = 10,
  random: boolean = false
): Promise<CategoryResponse> {
  const response = await apiClient.get<CategoryResponse>(`/categories/${category}`, {
    params: { limit, random },
  })
  return response.data
}

export async function getRandomCategoryImages(
  category: string,
  count: number = 5
): Promise<CategoryResponse> {
  const response = await apiClient.get<CategoryResponse>(`/categories/${category}/random`, {
    params: { count },
  })
  return response.data
}
