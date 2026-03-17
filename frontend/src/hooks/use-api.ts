import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/lib/api'

// Vision hooks
export function useVision() {
  return useMutation({
    mutationFn: async (data: FormData) => {
      const response = await api.post('/api/vision/recognize', data)
      return response.data
    },
  })
}
