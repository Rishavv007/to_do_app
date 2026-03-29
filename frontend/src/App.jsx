import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import TaskList from './pages/TaskList'
import TaskForm from './pages/TaskForm'

function App() {
  return (
    <div className="min-h-screen bg-default-50">
      <header className="border-b border-default-200 bg-default-100/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link to="/" className="text-xl font-bold text-primary">
            🚀 AI Task Manager
          </Link>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-8">
        <Routes>
          <Route path="/" element={<TaskList />} />
          <Route path="/new" element={<TaskForm />} />
          <Route path="/edit/:id" element={<TaskForm />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
