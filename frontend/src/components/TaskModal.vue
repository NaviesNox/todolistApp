<script setup>
import { computed, reactive, watch } from 'vue'

const props = defineProps({
  open: { type: Boolean, default: false },
  mode: { type: String, default: 'create' }, // 'create' | 'edit'
  task: { type: Object, default: null },
})

const emit = defineEmits(['close', 'submit'])

function isoToLocalInputValue(isoString) {
  if (!isoString) return ''
  const d = new Date(isoString)
  const pad = (n) => String(n).padStart(2, '0')
  const yyyy = d.getFullYear()
  const mm = pad(d.getMonth() + 1)
  const dd = pad(d.getDate())
  const hh = pad(d.getHours())
  const mi = pad(d.getMinutes())
  return `${yyyy}-${mm}-${dd}T${hh}:${mi}`
}

function localInputValueToIso(value) {
  // value is "YYYY-MM-DDTHH:MM" in local time
  return new Date(value).toISOString()
}

const form = reactive({
  description: '',
  deadlineLocal: '',
})

watch(
  () => [props.open, props.task],
  () => {
    if (!props.open) return
    form.description = props.task?.description || ''
    form.deadlineLocal = isoToLocalInputValue(props.task?.deadline || '')
  },
  { immediate: true },
)

const title = computed(() => (props.mode === 'edit' ? 'Edit task' : 'New task'))

function close() {
  emit('close')
}

function onBackdropClick(e) {
  if (e.target === e.currentTarget) close()
}

function submit() {
  const description = form.description.trim()
  if (!description) return
  if (!form.deadlineLocal) return

  emit('submit', {
    description,
    deadline: localInputValueToIso(form.deadlineLocal),
  })
}
</script>

<template>
  <div
    v-if="open"
    class="fixed inset-0 z-50 flex items-end justify-center p-4 sm:items-center"
    role="dialog"
    aria-modal="true"
    @click="onBackdropClick"
    @keydown.esc="close"
    tabindex="0"
  >
    <div
      class="absolute inset-0 bg-slate-950/60 backdrop-blur-sm"
      aria-hidden="true"
    />

    <div
      class="relative w-full max-w-lg rounded-2xl border border-white/10 bg-white shadow-xl dark:bg-slate-900 dark:shadow-glow"
    >
      <div class="flex items-start justify-between gap-4 px-5 pb-4 pt-5">
        <div>
          <h2 class="text-lg font-semibold text-slate-900 dark:text-slate-100">
            {{ title }}
          </h2>
          <p class="mt-1 text-sm text-slate-600 dark:text-slate-300">
            Description and deadline are required.
          </p>
        </div>

        <button
          type="button"
          class="rounded-lg p-2 text-slate-600 hover:bg-slate-100 hover:text-slate-900 dark:text-slate-300 dark:hover:bg-white/10 dark:hover:text-white"
          @click="close"
          aria-label="Close"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            class="h-5 w-5"
          >
            <path stroke-linecap="round" d="M6 6l12 12M18 6L6 18" />
          </svg>
        </button>
      </div>

      <form class="px-5 pb-5" @submit.prevent="submit">
        <div class="space-y-4">
          <div>
            <label
              class="mb-1.5 block text-sm font-medium text-slate-800 dark:text-slate-200"
              for="description"
              >Description</label
            >
            <textarea
              id="description"
              v-model="form.description"
              rows="4"
              class="block w-full resize-none rounded-xl border-slate-200 bg-white text-slate-900 shadow-sm placeholder:text-slate-400 focus:border-indigo-500 focus:ring-indigo-500 dark:border-white/10 dark:bg-slate-950/40 dark:text-slate-100 dark:placeholder:text-slate-500"
              placeholder="What do you need to do?"
              required
            />
          </div>

          <div>
            <label
              class="mb-1.5 block text-sm font-medium text-slate-800 dark:text-slate-200"
              for="deadline"
              >Deadline</label
            >
            <input
              id="deadline"
              v-model="form.deadlineLocal"
              type="datetime-local"
              class="block w-full rounded-xl border-slate-200 bg-white text-slate-900 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:border-white/10 dark:bg-slate-950/40 dark:text-slate-100"
              required
            />
          </div>
        </div>

        <div class="mt-6 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
          <button
            type="button"
            class="inline-flex items-center justify-center rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-800 hover:bg-slate-50 dark:border-white/10 dark:bg-white/5 dark:text-slate-100 dark:hover:bg-white/10"
            @click="close"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="inline-flex items-center justify-center rounded-xl bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-offset-2 focus:ring-offset-white dark:focus:ring-offset-slate-900"
          >
            {{ mode === 'edit' ? 'Save changes' : 'Create task' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

