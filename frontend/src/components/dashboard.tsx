'use client'

import { motion } from 'framer-motion'
import { Users, ChefHat, Calendar, BarChart3, TrendingUp, Activity } from 'lucide-react'
import { useStats, useUsers, useMealPlans, useSubscriptions } from '@/hooks/use-api'
import { Card } from '@/components/ui/card'
import { StatsChart } from '@/components/stats-chart'

export function Dashboard() {
  const { data: stats } = useStats()
  const { data: users } = useUsers()
  const { data: mealPlans } = useMealPlans()
  const { data: subscriptions } = useSubscriptions()

  const statsCards = [
    {
      title: 'Всего пользователей',
      value: users?.length || 0,
      icon: Users,
      color: 'text-jungle-teal',
      bgColor: 'bg-jungle-teal/10',
    },
    {
      title: 'Активных планов',
      value: mealPlans?.filter((plan: any) => plan.is_active).length || 0,
      icon: ChefHat,
      color: 'text-muted-teal',
      bgColor: 'bg-muted-teal/10',
    },
    {
      title: 'Активных подписок',
      value: subscriptions?.filter((sub: any) => sub.status === 'active').length || 0,
      icon: Calendar,
      color: 'text-frozen-water',
      bgColor: 'bg-frozen-water/10',
    },
    {
      title: 'Средний калории/день',
      value: Math.round(stats?.avg_calories_per_day || 0),
      icon: TrendingUp,
      color: 'text-azure-mist',
      bgColor: 'bg-azure-mist/10',
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-mint-cream via-azure-mist to-frozen-water">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-jungle-teal mb-4">
            AI-Dieta Admin Dashboard
          </h1>
          <p className="text-muted-teal text-lg">
            Управление питанием с искусственным интеллектом
          </p>
        </motion.div>

        {/* Stats Cards */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12"
        >
          {statsCards.map((card, index) => (
            <motion.div
              key={card.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              whileHover={{ scale: 1.05 }}
              className="card group"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-teal mb-1">
                    {card.title}
                  </p>
                  <p className="text-3xl font-bold text-jungle-teal">
                    {card.value}
                  </p>
                </div>
                <div className={`p-3 rounded-full ${card.bgColor} group-hover:scale-110 transition-transform duration-300`}>
                  <card.icon className={`w-6 h-6 ${card.color}`} />
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Charts Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="grid grid-cols-1 lg:grid-cols-2 gap-8"
        >
          <Card className="card">
            <div className="flex items-center mb-6">
              <BarChart3 className="w-6 h-6 text-jungle-teal mr-3" />
              <h3 className="text-xl font-semibold text-jungle-teal">
                Статистика питания
              </h3>
            </div>
            <StatsChart />
          </Card>

          <Card className="card">
            <div className="flex items-center mb-6">
              <Activity className="w-6 h-6 text-muted-teal mr-3" />
              <h3 className="text-xl font-semibold text-jungle-teal">
                Активность пользователей
              </h3>
            </div>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-muted-teal">Новые пользователи сегодня</span>
                <span className="font-semibold text-jungle-teal">12</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-muted-teal">Создано планов питания</span>
                <span className="font-semibold text-jungle-teal">8</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-muted-teal">Загружено фото еды</span>
                <span className="font-semibold text-jungle-teal">24</span>
              </div>
            </div>
          </Card>
        </motion.div>

        {/* Recent Activity */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="mt-12"
        >
          <Card className="card">
            <h3 className="text-xl font-semibold text-jungle-teal mb-6">
              Недавняя активность
            </h3>
            <div className="space-y-4">
              {[
                { user: 'Анна Петрова', action: 'создала новый план питания', time: '2 мин назад' },
                { user: 'Михаил Сидоров', action: 'загрузил фото ужина', time: '5 мин назад' },
                { user: 'Елена Иванова', action: 'обновила профиль', time: '12 мин назад' },
                { user: 'Дмитрий Кузнецов', action: 'оформил премиум подписку', time: '1 час назад' },
              ].map((activity, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="flex items-center justify-between py-3 border-b border-frozen-water last:border-b-0"
                >
                  <div>
                    <span className="font-medium text-jungle-teal">{activity.user}</span>
                    <span className="text-muted-teal ml-2">{activity.action}</span>
                  </div>
                  <span className="text-sm text-muted-teal">{activity.time}</span>
                </motion.div>
              ))}
            </div>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}