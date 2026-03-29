import React, { useState, useEffect } from 'react'
import { useNavigate, useParams, Link } from 'react-router-dom'
import { Button, Card, Input, TextArea, Chip, Spinner } from '@heroui/react'
import { createTask, fetchTask, updateTask, getAiSuggestion } from '../services/api'

const PRIORITY_OPTIONS = [
  { key: 'LOW', label: 'Low' },
  { key: 'MEDIUM', label: 'Medium' },
  { key: 'HIGH', label: 'High' },
]

const STATUS_OPTIONS = [
  { key: 'PENDING', label: 'Pending' },
  { key: 'IN_PROGRESS', label: 'In Progress' },
  { key: 'DONE', label: 'Done' },
]

function TaskForm() {
  const navigate = useNavigate()
  const { id } = useParams()
  const isEdit = !!id

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 'MEDIUM',
    deadline: '',
    status: 'PENDING',
  })

  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)
  const [aiLoading, setAiLoading] = useState(false)

  useEffect(() => {
    if (isEdit) {
      const loadTask = async () => {
        try {
          const data = await fetchTask(id)
          setFormData({
            title: data.title,
            description: data.description || '',
            priority: data.priority,
            deadline: data.deadline || '',
            status: data.status,
          })
        } catch (err) {
          alert('Error loading task')
          navigate('/')
        }
      }
      loadTask()
    }
  }, [id, isEdit, navigate])

  const validate = () => {
    const newErrors = {}
    if (!formData.title.trim()) newErrors.title = 'Title is required'
    if (formData.deadline) {
      const selected = new Date(formData.deadline)
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      if (selected < today) {
        newErrors.deadline = 'Deadline cannot be in the past'
      }
    }
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleAiSuggest = async () => {
    if (!formData.title.trim()) {
      setErrors({ title: 'Title is required for AI suggestions' })
      return
    }
    setAiLoading(true)
    setErrors({})
    try {
      const suggestion = await getAiSuggestion(formData.title, formData.description, formData.deadline)
      
      // Auto-apply the AI suggestions immediately so the user can just hit Save Task
      const updates = { priority: suggestion.priority }
      
      // We strictly ensure deadline_days handles 0 as a valid offset
      if (typeof suggestion.deadline_days === 'number') {
        const targetDate = new Date()
        targetDate.setDate(targetDate.getDate() + suggestion.deadline_days)
        updates.deadline = targetDate.toISOString().split('T')[0]
      }

      setFormData((prev) => {
        let currentDesc = prev.description || ''
        let finalDesc = currentDesc.trim()
        
        if (suggestion.subtasks && suggestion.subtasks.length > 0) {
          const subtasksText = '\n\nSubtasks:\n' + suggestion.subtasks.map((t) => `- ${t}`).join('\n')
          finalDesc = finalDesc + subtasksText
        }
        
        return {
          ...prev,
          ...updates,
          description: finalDesc
        }
      })
    } catch (err) {
      alert(err.message || 'AI request failed')
    } finally {
      setAiLoading(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!validate()) return
    setLoading(true)

    // Ensure empty dates are sent as null to satisfy backend schema
    const payload = {
      ...formData,
      deadline: formData.deadline === '' ? null : formData.deadline
    }

    try {
      if (isEdit) {
        await updateTask(id, payload)
      } else {
        await createTask(payload)
      }
      navigate('/')
    } catch (err) {
      alert(err.message || 'Error saving task')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="max-w-2xl mx-auto p-8">
      <h2 className="text-2xl font-bold text-foreground mb-6">
        {isEdit ? 'Edit Task' : 'Create New Task'}
      </h2>

      <form onSubmit={handleSubmit} className="flex flex-col gap-5">
        {/* Title */}
        <Input
          label="Task Title"
          name="title"
          placeholder="E.g., Design Database Schema"
          value={formData.title}
          onChange={handleChange}
          isRequired
          isInvalid={!!errors.title}
          errorMessage={errors.title}
          variant="bordered"
        />

        {/* Description */}
        <TextArea
          label="Description"
          name="description"
          placeholder="Add task details..."
          value={formData.description}
          onChange={handleChange}
          minRows={4}
          variant="bordered"
        />

        {/* Priority & Deadline row */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-1">Priority</label>
            <select
              name="priority"
              value={formData.priority}
              onChange={handleChange}
              className="w-full rounded-lg border border-default-200 bg-default-100 px-3 py-2 text-sm text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
            >
              {PRIORITY_OPTIONS.map((opt) => (
                <option key={opt.key} value={opt.key}>{opt.label}</option>
              ))}
            </select>
          </div>

          <Input
            type="date"
            label="Deadline"
            name="deadline"
            value={formData.deadline}
            onChange={handleChange}
            isInvalid={!!errors.deadline}
            errorMessage={errors.deadline}
            variant="bordered"
            min={new Date().toISOString().split('T')[0]}
          />
        </div>

        {/* Status (edit mode only) */}
        {isEdit && (
          <div>
            <label className="block text-sm font-medium text-foreground mb-1">Status</label>
            <select
              name="status"
              value={formData.status}
              onChange={handleChange}
              className="w-full rounded-lg border border-default-200 bg-default-100 px-3 py-2 text-sm text-foreground outline-none focus:border-primary focus:ring-2 focus:ring-primary/20"
            >
              {STATUS_OPTIONS.map((opt) => (
                <option key={opt.key} value={opt.key}>{opt.label}</option>
              ))}
            </select>
          </div>
        )}

        {/* AI Suggestion Button */}
        <Button
          type="button"
          variant="flat"
          color="secondary"
          className="w-full flex justify-center items-center"
          onPress={handleAiSuggest}
          isDisabled={aiLoading || !formData.title}
          isLoading={aiLoading}
        >
          ✨ Auto-Fill Priority & Subtasks
        </Button>

        {/* Actions */}
        <div className="flex justify-between items-center pt-4 border-t border-default-200">
          <Button onPress={() => navigate('/')} variant="flat" color="default">
            Cancel
          </Button>
          <Button
            type="submit"
            color="primary"
            isLoading={loading}
            isDisabled={loading}
          >
            {isEdit ? 'Update Task' : 'Save Task'}
          </Button>
        </div>
      </form>
    </Card>
  )
}

export default TaskForm
