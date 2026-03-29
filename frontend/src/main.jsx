import React from 'react'
import ReactDOM from 'react-dom/client'
import { RouterProvider } from 'react-aria-components'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import './index.css'

function Root() {
  return (
    <BrowserRouter>
      <RouterProvider>
        <App />
      </RouterProvider>
    </BrowserRouter>
  )
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Root />
  </React.StrictMode>,
)
