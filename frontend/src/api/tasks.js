function getApiBaseUrl() {
  const raw = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  return raw.replace(/\/+$/, '')
}

async function request(path, options = {}) {
  const res = await fetch(`${getApiBaseUrl()}${path}`, {
    ...options,
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  })

  if (res.status === 204) return null

  const text = await res.text()
  const data = text ? JSON.parse(text) : null

  if (!res.ok) {
    const message =
      (data && (data.detail || data.message)) ||
      `Request failed (${res.status})`
    throw new Error(message)
  }

  return data
}

export async function listTasks() {
  return await request('/tasks')
}

export async function createTask(payload) {
  return await request('/tasks', { method: 'POST', body: JSON.stringify(payload) })
}

export async function updateTask(id, payload) {
  return await request(`/tasks/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export async function deleteTask(id) {
  await request(`/tasks/${id}`, { method: 'DELETE' })
}

