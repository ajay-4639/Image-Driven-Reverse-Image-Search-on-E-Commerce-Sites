import { Link } from 'react-router-dom'
import { Search, Grid3X3, Zap, Shield, ArrowRight } from 'lucide-react'

const features = [
  {
    icon: Search,
    title: 'Visual Search',
    description: 'Upload any image and find visually similar products instantly using AI-powered image recognition.',
  },
  {
    icon: Grid3X3,
    title: 'Browse Categories',
    description: 'Explore products across different categories including apparel and footwear for all.',
  },
  {
    icon: Zap,
    title: 'Fast Results',
    description: 'Get search results in milliseconds powered by GPU-accelerated vector similarity search.',
  },
  {
    icon: Shield,
    title: 'State-of-the-Art AI',
    description: 'Built with Meta\'s ImageBind model for accurate multi-modal understanding.',
  },
]

export default function HomePage() {
  return (
    <div>
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900 text-white">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml,...')] opacity-10" />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 sm:py-32 relative">
          <div className="text-center max-w-3xl mx-auto">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight">
              Find Products with
              <span className="block text-primary-200">Visual Search</span>
            </h1>
            <p className="mt-6 text-lg sm:text-xl text-primary-100 max-w-2xl mx-auto">
              Upload an image and discover similar products from our e-commerce catalog.
              Powered by advanced AI for accurate and fast results.
            </p>
            <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/search"
                className="inline-flex items-center justify-center px-6 py-3 text-lg font-medium bg-white text-primary-700 rounded-xl hover:bg-primary-50 transition-colors shadow-lg"
              >
                <Search className="w-5 h-5 mr-2" />
                Start Searching
              </Link>
              <Link
                to="/categories"
                className="inline-flex items-center justify-center px-6 py-3 text-lg font-medium border-2 border-white/30 text-white rounded-xl hover:bg-white/10 transition-colors"
              >
                Browse Categories
                <ArrowRight className="w-5 h-5 ml-2" />
              </Link>
            </div>
          </div>
        </div>
        {/* Wave decoration */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg viewBox="0 0 1440 120" fill="none" className="w-full h-auto">
            <path
              d="M0 120L60 110C120 100 240 80 360 70C480 60 600 60 720 65C840 70 960 80 1080 85C1200 90 1320 90 1380 90L1440 90V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0Z"
              fill="#f9fafb"
            />
          </svg>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900">
              Powerful Features
            </h2>
            <p className="mt-4 text-lg text-gray-600 max-w-2xl mx-auto">
              Our image search platform combines cutting-edge AI with intuitive design
              to deliver the best product discovery experience.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature) => {
              const Icon = feature.icon
              return (
                <div
                  key={feature.title}
                  className="card p-6 hover:shadow-lg transition-shadow"
                >
                  <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center mb-4">
                    <Icon className="w-6 h-6 text-primary-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {feature.title}
                  </h3>
                  <p className="mt-2 text-gray-600">
                    {feature.description}
                  </p>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-primary-600 to-primary-800 rounded-2xl p-8 sm:p-12 text-center text-white">
            <h2 className="text-2xl sm:text-3xl font-bold">
              Ready to find similar products?
            </h2>
            <p className="mt-4 text-primary-100 max-w-xl mx-auto">
              Upload an image and let our AI find the most similar products
              from our extensive e-commerce catalog.
            </p>
            <Link
              to="/search"
              className="mt-8 inline-flex items-center justify-center px-8 py-4 text-lg font-medium bg-white text-primary-700 rounded-xl hover:bg-primary-50 transition-colors shadow-lg"
            >
              <Search className="w-5 h-5 mr-2" />
              Try Image Search Now
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
