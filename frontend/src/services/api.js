const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001/api';

export const fetchTasks = async () => {
  const res = await fetch(`${API_URL}/tasks`);
  if (!res.ok) throw new Error('Failed to fetch tasks');
  return res.json();
};

export const fetchTask = async (id) => {
  const res = await fetch(`${API_URL}/tasks/${id}`);
  if (!res.ok) throw new Error('Failed to fetch task');
  return res.json();
};

export const createTask = async (data) => {
  const res = await fetch(`${API_URL}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.message || 'Validation Failed');
  }
  return res.json();
};

export const updateTask = async (id, data) => {
  const res = await fetch(`${API_URL}/tasks/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.message || 'Validation Failed');
  }
  return res.json();
};

export const deleteTask = async (id) => {
  const res = await fetch(`${API_URL}/tasks/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete task');
  return res.json();
};

export const getAiSuggestion = async (title, description) => {
  const res = await fetch(`${API_URL}/tasks/suggest`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, description }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.message || 'AI generation failed');
  }
  return res.json();
};
