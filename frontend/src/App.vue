<script setup>
import { computed, onMounted, ref } from 'vue'
import TaskModal from './components/TaskModal.vue'
import { createTask, deleteTask, listTasks, updateTask } from './api/tasks'
import { getInitialTheme, setTheme } from './theme'

const theme = ref(getInitialTheme())

function toggleTheme() {
  theme.value = theme.value === 'dark' ? 'light' : 'dark'
  setTheme(theme.value)
}

const tasks = ref([])
const loading = ref(false)
const error = ref('')

const modalOpen = ref(false)
const editingTask = ref(null)

function openCreate() {
  editingTask.value = null
  modalOpen.value = true
}

function openEdit(task) {
  editingTask.value = task
  modalOpen.value = true
}

function closeModal() {
  modalOpen.value = false
}

function formatDeadline(isoString) {
  const d = new Date(isoString)
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(d)
}

function isOverdue(isoString) {
  return new Date(isoString).getTime() < Date.now()
}

const sortedTasks = computed(() =>
  [...tasks.value].sort(
    (a, b) => new Date(a.deadline).getTime() - new Date(b.deadline).getTime(),
  ),
)

const overdueCount = computed(
  () => sortedTasks.value.filter((t) => isOverdue(t.deadline)).length,
)

async function refresh() {
  loading.value = true
  error.value = ''
  try {
    tasks.value = await listTasks()
  } catch (e) {
    error.value = e?.message || 'Failed to load tasks.'
  } finally {
    loading.value = false
  }
}

async function onSubmit(payload) {
  error.value = ''
  try {
    if (editingTask.value) {
      await updateTask(editingTask.value.id, payload)
    } else {
      await createTask(payload)
    }
    closeModal()
    await refresh()
  } catch (e) {
    error.value = e?.message || 'Save failed.'
  }
}

async function onDelete(task) {
  const ok = confirm('Delete this task? This cannot be undone.')
  if (!ok) return

  error.value = ''
  try {
    await deleteTask(task.id)
    await refresh()
  } catch (e) {
    error.value = e?.message || 'Delete failed.'
  }
}

onMounted(refresh)
</script>

<template>
  <div
    class="min-h-screen bg-slate-50 text-slate-900 dark:bg-slate-950 dark:text-slate-100"
  >
    <div
      class="pointer-events-none absolute inset-x-0 top-0 h-72 bg-gradient-to-b from-indigo-600/15 to-transparent dark:from-indigo-500/15"
      aria-hidden="true"
    />

    <header class="relative border-b border-slate-200/70 dark:border-white/10">
      <div class="mx-auto max-w-4xl px-4 py-5 sm:px-6">
        <div class="flex items-center justify-between gap-4">
          <div class="min-w-0">
            <h1 class="truncate text-xl font-semibold">
              Todo List
            </h1>
            <p class="mt-1 text-sm text-slate-600 dark:text-slate-300">
              {{ sortedTasks.length }} task{{ sortedTasks.length === 1 ? '' : 's' }}
              <span v-if="overdueCount" class="text-rose-600 dark:text-rose-300">
                · {{ overdueCount }} overdue
              </span>
            </p>
          </div>

          <div class="flex items-center gap-2">
            <button
              type="button"
              class="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm font-semibold text-slate-800 hover:bg-slate-50 dark:border-white/10 dark:bg-white/5 dark:text-slate-100 dark:hover:bg-white/10"
              @click="toggleTheme"
            >
              <span class="hidden sm:inline">Theme</span>
              <span class="text-slate-600 dark:text-slate-300">
                {{ theme === 'dark' ? 'Dark' : 'Light' }}
              </span>
            </button>

            <button
              type="button"
              class="inline-flex items-center justify-center rounded-xl bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
              @click="openCreate"
            >
              New task
            </button>
          </div>
        </div>
      </div>
    </header>

    <main class="relative mx-auto max-w-4xl px-4 py-6 sm:px-6">
      <div
        v-if="error"
        class="mb-4 rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-800 dark:border-rose-500/30 dark:bg-rose-950/40 dark:text-rose-100"
      >
        {{ error }}
      </div>

      <div v-if="loading" class="rounded-2xl border border-slate-200 bg-white p-5 dark:border-white/10 dark:bg-white/5">
        <div class="h-4 w-2/3 animate-pulse rounded bg-slate-200 dark:bg-white/10" />
        <div class="mt-3 h-4 w-1/2 animate-pulse rounded bg-slate-200 dark:bg-white/10" />
        <div class="mt-6 h-24 animate-pulse rounded-xl bg-slate-200 dark:bg-white/10" />
      </div>

      <div v-else class="space-y-4">
        <div
          v-if="!sortedTasks.length"
          class="rounded-2xl border border-slate-200 bg-white p-6 text-center dark:border-white/10 dark:bg-white/5"
        >
          <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-indigo-600/10 text-indigo-700 dark:bg-indigo-500/15 dark:text-indigo-200">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              class="h-6 w-6"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M20 12a8 8 0 11-16 0 8 8 0 0116 0z" />
            </svg>
          </div>
          <h2 class="mt-4 text-lg font-semibold">No tasks yet</h2>
          <p class="mt-1 text-sm text-slate-600 dark:text-slate-300">
            Create your first task and give it a deadline.
          </p>
          <button
            type="button"
            class="mt-4 inline-flex items-center justify-center rounded-xl bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
            @click="openCreate"
          >
            Create a task
          </button>
        </div>

        <ul v-else class="grid gap-4">
          <li
            v-for="task in sortedTasks"
            :key="task.id"
            class="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:shadow-md dark:border-white/10 dark:bg-white/5"
          >
            <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
              <div class="min-w-0">
                <p class="whitespace-pre-wrap break-words text-base font-medium">
                  {{ task.description }}
                </p>
                <p
                  class="mt-2 inline-flex items-center gap-2 text-sm"
                  :class="
                    isOverdue(task.deadline)
                      ? 'text-rose-700 dark:text-rose-300'
                      : 'text-slate-600 dark:text-slate-300'
                  "
                >
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    class="h-4 w-4"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6l4 2" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M20 12a8 8 0 11-16 0 8 8 0 0116 0z" />
                  </svg>
                  <span>
                    {{ formatDeadline(task.deadline) }}
                    <span v-if="isOverdue(task.deadline)" class="font-semibold">
                      · overdue
                    </span>
                  </span>
                </p>
              </div>

              <div class="flex shrink-0 items-center gap-2 sm:justify-end">
                <button
                  type="button"
                  class="inline-flex items-center justify-center rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm font-semibold text-slate-800 hover:bg-slate-50 dark:border-white/10 dark:bg-white/5 dark:text-slate-100 dark:hover:bg-white/10"
                  @click="openEdit(task)"
                >
                  Edit
                </button>
                <button
                  type="button"
                  class="inline-flex items-center justify-center rounded-xl border border-rose-200 bg-rose-50 px-3 py-2 text-sm font-semibold text-rose-700 hover:bg-rose-100 dark:border-rose-500/30 dark:bg-rose-950/30 dark:text-rose-200 dark:hover:bg-rose-950/45"
                  @click="onDelete(task)"
                >
                  Delete
                </button>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </main>

    <TaskModal
      :open="modalOpen"
      :mode="editingTask ? 'edit' : 'create'"
      :task="editingTask"
      @close="closeModal"
      @submit="onSubmit"
    />
  </div>
</template>

