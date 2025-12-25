# Frontend - Image Search UI

React frontend for the Image-Driven Reverse Image Search application.

## Structure

```
frontend/
├── src/
│   ├── api/
│   │   ├── client.ts         # Axios client configuration
│   │   ├── search.ts         # Search API functions
│   │   ├── categories.ts     # Categories API functions
│   │   ├── health.ts         # Health check functions
│   │   └── index.ts          # API exports
│   ├── components/
│   │   ├── Layout.tsx        # App layout with navigation
│   │   ├── ImageUploader.tsx # Drag & drop image upload
│   │   ├── ImageGrid.tsx     # Image results grid
│   │   ├── ImageModal.tsx    # Image detail modal
│   │   ├── CategoryCard.tsx  # Category card component
│   │   └── LoadingSpinner.tsx
│   ├── pages/
│   │   ├── HomePage.tsx      # Landing page
│   │   ├── SearchPage.tsx    # Image search page
│   │   ├── CategoriesPage.tsx    # Categories list
│   │   └── CategoryDetailPage.tsx # Category images
│   ├── types/
│   │   └── index.ts          # TypeScript types
│   ├── utils/
│   │   └── cn.ts             # Class name utility
│   ├── App.tsx               # App component with routes
│   ├── main.tsx              # Entry point
│   └── index.css             # Global styles
├── Dockerfile                # Production image
├── nginx.conf               # Nginx configuration
├── package.json
├── tailwind.config.js
├── vite.config.ts
└── tsconfig.json
```

## Quick Start

```bash
# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Run development server
npm run dev
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | /api/v1 | Backend API URL |

## Tech Stack

- React 18
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Axios
- Lucide React (icons)
- react-dropzone
