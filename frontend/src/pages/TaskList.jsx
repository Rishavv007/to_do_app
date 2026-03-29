import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button, Card, Chip, Spinner } from '@heroui/react'
import { fetchTasks, deleteTask } from '../services/api'

function TaskList() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  const loadTasks = async () => {
    try {
      const data = await fetchTasks()
      setTasks(data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadTasks()
  }, [])

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this task?')) return
    try {
      await deleteTask(id)
      setTasks(tasks.filter((t) => t.id !== id))
    } catch (err) {
      alert('Failed to delete task.')
    }
  }

  const priorityColorMap = {
    HIGH: 'danger',
    MEDIUM: 'warning',
    LOW: 'success',
  }

  const statusColorMap = {
    PENDING: 'default',
    IN_PROGRESS: 'primary',
    DONE: 'success',
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center py-20">
        <Spinner size="lg" label="Loading tasks..." />
      </div>
    )
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-foreground">Your Tasks</h1>
        <Button onPress={() => navigate('/new')} color="primary" variant="solid" size="md">
          + New Task
        </Button>
      </div>

      {tasks.length === 0 ? (
        <Card className="p-12 text-center">
          <p className="text-default-500 text-lg">
            No tasks yet. Create one to get started!
          </p>
        </Card>
      ) : (
        <div className="flex flex-col gap-4">
          {tasks.map((task) => (
            <Card key={task.id} className="p-5">
              <div className="flex justify-between items-start mb-2">
                <h3
                  className={`text-lg font-semibold ${
                    task.status === 'DONE'
                      ? 'line-through text-default-400'
                      : 'text-foreground'
                  }`}
                >
                  {task.title}
                </h3>
                <div className="flex gap-2">
                  <Chip
                    color={priorityColorMap[task.priority] || 'default'}
                    variant="flat"
                    size="sm"
                  >
                    {task.priority}
                  </Chip>
                  <Chip
                    color={statusColorMap[task.status] || 'default'}
                    variant="bordered"
                    size="sm"
                  >
                    {task.status?.replace('_', ' ')}
                  </Chip>
                </div>
              </div>

              {task.description && (
                <p className="text-default-500 text-sm mb-3 whitespace-pre-wrap">
                  {task.description}
                </p>
              )}

              <div className="flex justify-between items-center">
                <span className="text-xs text-default-400">
                  {task.deadline
                    ? `Deadline: ${new Date(task.deadline).toLocaleDateString()}`
                    : 'No deadline'}
                </span>
                <div className="flex gap-2">
                  <Button
                    onPress={() => navigate(`/edit/${task.id}`)}
                    variant="bordered"
                    size="sm"
                  >
                    Edit
                  </Button>
                  <Button
                    color="danger"
                    variant="flat"
                    size="sm"
                    onPress={() => handleDelete(task.id)}
                  >
                    Delete
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

export default TaskList
