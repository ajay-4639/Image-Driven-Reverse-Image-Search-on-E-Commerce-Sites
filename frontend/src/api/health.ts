import apiClient from './client'
import type { HealthResponse, IndexingStatus } from '../types'

export async function getHealth(): Promise<HealthResponse> {
  const response = await apiClient.get<HealthResponse>('/health')
  return response.data
}

export async function getIndexingStatus(): Promise<IndexingStatus> {
  const response = await apiClient.get<IndexingStatus>('/health/indexing')
  return response.data
}

export async function checkReady(): Promise<boolean> {
  try {
    const response = await apiClient.get('/health/ready')
    return response.data.status === 'ready'
  } catch {
    return false
  }
}
