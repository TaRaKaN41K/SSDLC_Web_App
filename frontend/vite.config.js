import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import fs from 'fs'
import path from 'path'


export default defineConfig({
  plugins: [
    react(),
    tailwindcss()
  ],
  server: {
    https: {
      key: fs.readFileSync(path.resolve(__dirname, 'certs/selfsigned.key')),
      cert: fs.readFileSync(path.resolve(__dirname, 'certs/selfsigned.crt')),
    },
    host: "0.0.0.0",
    port: 3000,
  },
})