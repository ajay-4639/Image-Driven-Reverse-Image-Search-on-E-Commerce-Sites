import { Link } from 'react-router-dom'
import { ChevronRight, ShoppingBag, User, Footprints } from 'lucide-react'
import type { CategoryInfo } from '../types'

interface CategoryCardProps {
  category: CategoryInfo
}

const categoryIcons: Record<string, typeof ShoppingBag> = {
  'Apparel_Boys': User,
  'Apparel_Girls': User,
  'Footwear_Men': Footprints,
  'Footwear_Women': Footprints,
}

const categoryColors: Record<string, string> = {
  'Apparel_Boys': 'from-blue-500 to-blue-600',
  'Apparel_Girls': 'from-pink-500 to-pink-600',
  'Footwear_Men': 'from-green-500 to-green-600',
  'Footwear_Women': 'from-purple-500 to-purple-600',
}

export default function CategoryCard({ category }: CategoryCardProps) {
  const Icon = categoryIcons[category.name] || ShoppingBag
  const colorClass = categoryColors[category.name] || 'from-gray-500 to-gray-600'

  return (
    <Link
      to={`/categories/${category.name}`}
      className="card group hover:shadow-lg transition-all duration-200"
    >
      <div className="p-6">
        <div className="flex items-start justify-between">
          <div
            className={`w-12 h-12 rounded-xl bg-gradient-to-br ${colorClass} flex items-center justify-center shadow-lg`}
          >
            <Icon className="w-6 h-6 text-white" />
          </div>
          <ChevronRight className="w-5 h-5 text-gray-400 group-hover:text-gray-600 group-hover:translate-x-1 transition-all" />
        </div>
        <div className="mt-4">
          <h3 className="text-lg font-semibold text-gray-900">
            {category.display_name}
          </h3>
          <p className="text-sm text-gray-500 mt-1">
            {category.image_count.toLocaleString()} products
          </p>
        </div>
      </div>
    </Link>
  )
}
