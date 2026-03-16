// User types
export interface User {
  id: number
  email?: string
  phone?: string
  telegram_id?: number
  first_name?: string
  last_name?: string
  avatar_url?: string
  weight?: number
  height?: number
  age?: number
  gender?: string
  activity_level?: string
  goal?: string
  dietary_preferences?: string
  created_at: string
  updated_at: string
}

// Meal types
export interface Meal {
  id: number
  user_id: number
  name: string
  description?: string
  calories?: number
  protein?: number
  carbs?: number
  fat?: number
  meal_type: string
  date: string
  created_at: string
}

// Meal Plan types
export interface PlanItem {
  id: number
  meal_name: string
  meal_type: string
  day_of_week: number
  calories?: number
  protein?: number
  carbs?: number
  fat?: number
}

export interface MealPlan {
  id: number
  user_id: number
  name: string
  description?: string
  start_date: string
  end_date: string
  is_active: boolean
  created_at: string
  items: PlanItem[]
}

// Subscription types
export interface SubscriptionTier {
  id: number
  name: string
  price: number
  duration_days: number
  features: string
  created_at: string
}

export interface Subscription {
  id: number
  user_id: number
  tier_id: number
  status: 'active' | 'expired' | 'cancelled'
  start_date: string
  end_date: string
  created_at: string
  updated_at: string
  user?: User
  tier?: SubscriptionTier
}

// Statistics types
export interface Stats {
  total_calories: number
  total_protein: number
  total_carbs: number
  total_fat: number
  meal_count: number
  avg_calories_per_day: number
  period_days: number
}

// API Response types
export interface ApiResponse<T> {
  success: boolean
  message?: string
  data?: T
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  limit: number
}

// Form types
export interface LoginForm {
  email: string
  password: string
}

export interface RegisterForm {
  email: string
  password: string
  first_name?: string
  last_name?: string
}

export interface UserUpdateForm {
  first_name?: string
  last_name?: string
  weight?: number
  height?: number
  age?: number
  gender?: string
  activity_level?: string
  goal?: string
  dietary_preferences?: string
}