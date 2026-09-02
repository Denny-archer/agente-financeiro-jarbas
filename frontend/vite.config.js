import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/gastos': 'http://localhost:8000',
      '/resumo': 'http://localhost:8000',
      '/alertas': 'http://localhost:8000',
      '/chat': 'http://localhost:8000',
      '/importar': 'http://localhost:8000',
    },
  },
})
