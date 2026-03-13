const THEME_KEY = 'todo_theme'

export function applyTheme(theme) {
  const isDark = theme === 'dark'
  document.documentElement.classList.toggle('dark', isDark)
  // Helps native UI (scrollbars/form controls) match theme.
  document.documentElement.style.colorScheme = isDark ? 'dark' : 'light'
}

export function getInitialTheme() {
  const saved = localStorage.getItem(THEME_KEY)
  if (saved === 'light' || saved === 'dark') return saved

  // Prioritize dark mode by default.
  return 'dark'
}

export function setTheme(theme) {
  localStorage.setItem(THEME_KEY, theme)
  applyTheme(theme)
}

export function initTheme() {
  applyTheme(getInitialTheme())
}

