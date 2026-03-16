'use client'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { useStats } from '@/hooks/use-api'

const COLORS = ['#6b9080', '#a4c3b2', '#cce3de', '#eaf4f4']

export function StatsChart() {
  const { data: stats } = useStats()

  const nutritionData = [
    { name: 'Белки', value: stats?.total_protein || 0, color: '#6b9080' },
    { name: 'Углеводы', value: stats?.total_carbs || 0, color: '#a4c3b2' },
    { name: 'Жиры', value: stats?.total_fat || 0, color: '#cce3de' },
  ]

  const weeklyData = [
    { day: 'Пн', calories: 1850 },
    { day: 'Вт', calories: 2100 },
    { day: 'Ср', calories: 1950 },
    { day: 'Чт', calories: 2200 },
    { day: 'Пт', calories: 2000 },
    { day: 'Сб', calories: 2300 },
    { day: 'Вс', calories: 2150 },
  ]

  return (
    <div className="space-y-8">
      {/* Nutrition Breakdown */}
      <div>
        <h4 className="text-lg font-medium text-jungle-teal mb-4">
          Распределение питательных веществ
        </h4>
        <ResponsiveContainer width="100%" height={200}>
          <PieChart>
            <Pie
              data={nutritionData}
              cx="50%"
              cy="50%"
              innerRadius={40}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
            >
              {nutritionData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip
              formatter={(value: number) => [`${value}г`, '']}
              labelStyle={{ color: '#6b9080' }}
            />
          </PieChart>
        </ResponsiveContainer>
        <div className="flex justify-center space-x-6 mt-4">
          {nutritionData.map((item, index) => (
            <div key={index} className="flex items-center">
              <div
                className="w-3 h-3 rounded-full mr-2"
                style={{ backgroundColor: item.color }}
              />
              <span className="text-sm text-muted-teal">
                {item.name}: {item.value}г
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Weekly Calories */}
      <div>
        <h4 className="text-lg font-medium text-jungle-teal mb-4">
          Калории за неделю
        </h4>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={weeklyData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#cce3de" />
            <XAxis
              dataKey="day"
              stroke="#6b9080"
              fontSize={12}
            />
            <YAxis
              stroke="#6b9080"
              fontSize={12}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#eaf4f4',
                border: '1px solid #cce3de',
                borderRadius: '8px',
              }}
              labelStyle={{ color: '#6b9080' }}
            />
            <Bar
              dataKey="calories"
              fill="#6b9080"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}