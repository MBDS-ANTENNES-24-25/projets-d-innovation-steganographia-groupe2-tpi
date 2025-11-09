import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite' 
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(), 
    tailwindcss(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@layouts': path.resolve(__dirname, './src/layouts'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@styles': path.resolve(__dirname, './src/styles'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@schemas': path.resolve(__dirname, './src/schemas'),
      '@services': path.resolve(__dirname, './src/services'),
      '@context': path.resolve(__dirname, './src/context'),
      '@atoms': path.resolve(__dirname, './src/atoms'),
      '@api': path.resolve(__dirname, './src/api'),
      '@utils': path.resolve(__dirname, './src/utils'),
    },
  },
  server: {
    host: '0.0.0.0', // Important pour Docker
    port: 5173,
    strictPort: true,
    watch: {
      usePolling: true, // Nécessaire pour le hot reload dans Docker
      interval: 1000,   // Intervalle de polling en ms
    },
    hmr: {
      host: 'localhost', // Pour le Hot Module Replacement
      port: 5173
    }
  }
})
