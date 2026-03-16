'use client'

import { useState } from 'react'
import { Calendar, Activity } from 'lucide-react'
import {
  useSubscriptions,
  useSubscriptionTiers,
  useSubscribe,
  useCancelSubscription,
} from '@/hooks/use-api'
import { Card } from '@/components/ui/card'

export function Account() {
  const [message, setMessage] = useState<string | null>(null)
  const { data: subscriptions, refetch: refetchSubscriptions } = useSubscriptions()
  const { data: tiers } = useSubscriptionTiers()
  const subscribeMutation = useSubscribe()
  const cancelMutation = useCancelSubscription()

  return (
    <div className="min-h-screen bg-gradient-to-br from-mint-cream via-azure-mist to-frozen-water">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-jungle-teal mb-4">Мой аккаунт</h1>
          <p className="text-muted-teal text-lg">Управление подпиской и доступами</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          <Card className="card">
            <div className="flex items-center mb-6">
              <Calendar className="w-6 h-6 text-jungle-teal mr-3" />
              <h3 className="text-xl font-semibold text-jungle-teal">Текущая подписка</h3>
            </div>
            {message ? <div className="mb-4 text-sm text-red-600">{message}</div> : null}
            <div className="space-y-3">
              {subscriptions?.status === 'active' ? (
                <>
                  <div className="text-muted-teal">
                    Тариф: <span className="font-semibold text-jungle-teal">{subscriptions.tier}</span>
                  </div>
                  <div className="text-muted-teal">
                    Действует до:{' '}
                    <span className="font-semibold text-jungle-teal">
                      {new Date(subscriptions.expires_at).toLocaleDateString()}
                    </span>
                  </div>
                  <button
                    onClick={async () => {
                      setMessage(null)
                      try {
                        await cancelMutation.mutateAsync(undefined)
                        await refetchSubscriptions()
                      } catch (err: any) {
                        setMessage(err?.response?.data?.detail || err?.message || 'Ошибка')
                      }
                    }}
                    disabled={cancelMutation.isPending}
                    className="px-4 py-2 rounded-lg bg-red-500 text-white hover:bg-red-600 disabled:opacity-60"
                  >
                    Отписаться
                  </button>
                </>
              ) : (
                <div className="text-muted-teal">Нет активной подписки</div>
              )}
            </div>
          </Card>

          <Card className="card">
            <div className="flex items-center mb-6">
              <Activity className="w-6 h-6 text-muted-teal mr-3" />
              <h3 className="text-xl font-semibold text-jungle-teal">Тарифы</h3>
            </div>
            <div className="space-y-4">
              {tiers?.map((tier: any) => {
                const isActive = subscriptions?.tier === tier.name && subscriptions?.status === 'active'
                const priceLabel = tier.price === 0 ? 'Бесплатно' : `${tier.price} руб`;
                return (
                  <div key={tier.id} className="p-4 rounded-lg border border-frozen-water">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-semibold text-jungle-teal">{tier.name}</div>
                        <div className="text-sm text-muted-teal">{priceLabel}</div>
                      </div>
                      <button
                        onClick={async () => {
                          setMessage(null)
                          try {
                            await subscribeMutation.mutateAsync(tier.id)
                            await refetchSubscriptions()
                          } catch (err: any) {
                            setMessage(err?.response?.data?.detail || err?.message || 'Ошибка')
                          }
                        }}
                        disabled={subscribeMutation.isPending || isActive}
                        className={`px-4 py-2 rounded-lg text-white ${
                          isActive ? 'bg-gray-500 cursor-not-allowed' : 'bg-jungle-teal hover:bg-emerald-500'
                        }`}
                      >
                        {isActive ? 'Текущий тариф' : 'Подписаться'}
                      </button>
                    </div>
                    <div className="mt-2 text-sm text-muted-teal">{tier.features}</div>
                  </div>
                )
              })}
            </div>
          </Card>
        </div>
      </div>
    </div>
  )
}
