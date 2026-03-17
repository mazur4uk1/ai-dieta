import { useState } from 'react';
import { useVision } from '@/hooks/use-api';
import { Card } from '@/components/ui';

export default function Home() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const vision = useVision();

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const formData = new FormData();
      formData.append('image', file);
      try {
        const response = await vision.mutateAsync({ formData });
        setResult(response);
        setImage(URL.createObjectURL(file) as any);
      } catch (error) {
        console.error('Ошибка загрузки изображения:', error);
      }
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">AI Диета - Распознавание еды</h1>
        
        <div className="mb-8">
          <input
            type="file"
            accept="image/*"
            onChange={handleImageUpload}
            className="border-2 border-gray-300 rounded-md p-2 cursor-pointer hover:border-gray-400"
          />
        </div>

        {image && (
          <div className="mb-8">
            <img src={image} alt="Загруженное изображение" className="max-w-full" />
          </div>
        )}

        {result && (
          <Card>
            <h2 className="text-xl font-semibold mb-4">Результат распознавания</h2>
            <div className="space-y-4">
              {Array.isArray((result as any).recognized_foods) && (result as any).recognized_foods.map((food: any, index: number) => (
                <div key={index} className="p-4 bg-white rounded-lg shadow-sm">
                  <div className="flex justify-between items-center">
                    <div>
                      <h3 className="font-medium">{food.name}</h3>
                      <p className="text-gray-600">Калорийность: {food.calories} ккал</p>
                    </div>
                    <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full">
                      {Math.round(food.confidence * 100)}% уверенность
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        )}

        {!result && (
          <Card>
            <p className="text-center text-gray-600">
              Загрузите изображение еды для анализа калорийности
            </p>
          </Card>
        )}
      </div>
    </div>
  );
}
