import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '@/lib/api'
import { User, Meal, MealPlan, Subscription, Stats, LoginForm, RegisterForm, UserUpdateForm } from '@/types'

// Auth hooks
export function useLogin() {
  return useMutation({
    mutationFn: async (data: LoginForm) => {
      const response = await api.post('/auth/login', data)
      return response.data
    },
    onSuccess: (data) => {
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
    },
  })
}

export function useRegister() {
  return useMutation({
    mutationFn: async (data: RegisterForm) => {
      const response = await api.post('/auth/register', data)
      return response.data
    },
  })
}

// User hooks
export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const response = await api.get('/users')
      return response.data
    },
  })
}

export function useUser(id: number) {
  return useQuery({
    queryKey: ['users', id],
    queryFn: async () => {
      const response = await api.get(`/users/${id}`)
      return response.data
    },
    enabled: !!id,
  })
}

export function useUpdateUser() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async ({ id, data }: { id: number; data: UserUpdateForm }) => {
      const response = await api.put(`/users/${id}`, data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })
}

// Meal hooks
export function useMeals() {
  return useQuery({
    queryKey: ['meals'],
    queryFn: async () => {
      const response = await api.get('/meals')
      return response.data
    },
  })
}

export function useCreateMeal() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: Omit<Meal, 'id' | 'user_id' | 'created_at'>) => {
      const response = await api.post('/meals', data)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['meals'] })
    },
  })
}

// Meal Plan hooks
export function useMealPlans() {
  return useQuery({
    queryKey: ['meal-plans'],
    queryFn: async () => {
      const response = await api.get('/meal-plans')
      return response.data
    },
  })
}

// Subscription hooks
export function useSubscriptionTiers() {
  return useQuery({
    queryKey: ['subscription-tiers'],
    queryFn: async () => {
      const response = await api.get('/subscription/tiers')
      return response.data
    },
  })
}

export function useSubscriptions() {
  return useQuery({
    queryKey: ['subscriptions'],
    queryFn: async () => {
      const response = await api.get('/subscription')
      return response.data
    },
  })
}

export function useSubscribe() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (tierId: number) => {
      const response = await api.post(`/subscription/subscribe/${tierId}`)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subscriptions'] })
    },
  })
}

export function useCancelSubscription() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async () => {
      const response = await api.post('/subscription/cancel')
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subscriptions'] })
    },
  })
}

// Stats hooks
export function useStats(days: number = 7) {
  return useQuery({
    queryKey: ['stats', days],
    queryFn: async () => {
      const response = await api.get(`/stats?days=${days}`)
      return response.data
    },
  })
}