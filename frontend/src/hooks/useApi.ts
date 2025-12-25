import { useState, useCallback } from 'react'

interface UseApiState<T> {
  data: T | null
  error: string | null
  isLoading: boolean
}

interface UseApiResult<T> extends UseApiState<T> {
  execute: (...args: unknown[]) => Promise<T | null>
  reset: () => void
}

export function useApi<T>(
  apiFunction: (...args: unknown[]) => Promise<T>
): UseApiResult<T> {
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    error: null,
    isLoading: false,
  })

  const execute = useCallback(
    async (...args: unknown[]): Promise<T | null> => {
      setState((prev) => ({ ...prev, isLoading: true, error: null }))

      try {
        const result = await apiFunction(...args)
        setState({ data: result, error: null, isLoading: false })
        return result
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : 'An error occurred'
        setState((prev) => ({ ...prev, error: errorMessage, isLoading: false }))
        return null
      }
    },
    [apiFunction]
  )

  const reset = useCallback(() => {
    setState({ data: null, error: null, isLoading: false })
  }, [])

  return {
    ...state,
    execute,
    reset,
  }
}
