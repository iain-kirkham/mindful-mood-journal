/**
 * Toast Notification System
 * Provides unobtrusive feedback for user actions with color-coded toasts.
 * Toasts appear in the top-center and auto-dismiss after 4 seconds.
 */
const TOAST_TITLES = { success: 'Success', error: 'Error', danger: 'Error', warning: 'Warning', info: 'Info' };
const TOAST_SVGS = (() => {
  const svgWrapper = (inner) => `\n<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">${inner}\n</svg>\n`;
  return {
    success: svgWrapper('\n  <circle cx="12" cy="12" r="10" fill="currentColor" opacity="0.08"/>\n  <path d="M8 12L11 15L16 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'),
    info: svgWrapper('\n  <circle cx="12" cy="12" r="10" fill="currentColor" opacity="0.08"/>\n  <path d="M12 8V12M12 16H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'),
    error: svgWrapper('\n  <circle cx="12" cy="12" r="10" fill="currentColor" opacity="0.08"/>\n  <path d="M12 8V12M12 16H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'),
    warning: svgWrapper('\n  <path d="M12 2L2 20H22L12 2Z" fill="currentColor" opacity="0.08"/>\n  <path d="M12 3L3 19H21L12 3Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>\n  <path d="M12 9V13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>\n  <circle cx="12" cy="17" r="1" fill="currentColor"/>')
  };
})();

const ToastManager = {
  containerEl: null,
  pendingToasts: [],
  maxVisibleToasts: 5,

  init() {
    this.containerEl = document.getElementById('toastContainer') || this.createContainerEl();
    // initialise any server-rendered toasts
    this.containerEl.querySelectorAll('.toast').forEach(el => {
      const toast = new bootstrap.Toast(el, { autohide: true, delay: 4000 });
      toast.show();
      el.addEventListener('hidden.bs.toast', () => { el.remove(); this._showNextFromQueue(); }, { once: true });
    });
  },

  createContainerEl() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container position-fixed top-0 start-50 translate-middle-x p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
  },

  showToast(message, type = 'info', duration = 4000) {
    const visible = this.containerEl.querySelectorAll('.toast.show').length;
    if (visible >= this.maxVisibleToasts) {
      this.pendingToasts.push({ message, type, duration });
      return;
    }
    const toastEl = this.buildToastElement(message, type);
    this.containerEl.appendChild(toastEl);
    const bsToast = new bootstrap.Toast(toastEl, { autohide: true, delay: duration });
    bsToast.show();
    toastEl.addEventListener('hidden.bs.toast', () => { toastEl.remove(); this._showNextFromQueue(); }, { once: true });
  },

  /**
   * show the next toast from the pending queue.
   * This is called after a visible toast is hidden to keep at most
   * `maxVisibleToasts` displayed at once.
   */
  showNextFromQueue() {
    if (this.pendingToasts.length === 0) return;
    const { message, type, duration } = this.pendingToasts.shift();
    this.showToast(message, type, duration);
  },

  buildToastElement(message, type) {
    const el = document.createElement('div');
    el.className = `toast border-0 mb-2 toast-${type}`;
    el.setAttribute('role', 'alert');
    el.setAttribute('aria-live', 'assertive');
    el.setAttribute('aria-atomic', 'true');
    const title = TOAST_TITLES[type] || TOAST_TITLES.info;
    const svg = TOAST_SVGS[type] || TOAST_SVGS.info;
    el.innerHTML = `\n      <div class="toast-content">\n        <div class="toast-icon-wrapper">${svg}</div>\n        <div class="toast-text">\n          <div class="toast-title">${title}</div>\n          <div class="toast-message">${this.escapeHtml(message)}</div>\n        </div>\n        <button type="button" class="btn-close toast-close" data-bs-dismiss="toast" aria-label="Close"></button>\n      </div>\n    `;
    return el;
  },

  /**
   * Escape HTML content to prevent XSS.
   * Uses a DOM text node so browser handles entity encoding reliably.
   * @param {string} text - untrusted user content
   * @returns {string} safe HTML-encoded string
   */
  escapeHtml(text) {
    const d = document.createElement('div');
    d.textContent = text;
    return d.innerHTML;
  },

  success(message, duration = 4000) { this.showToast(message, 'success', duration); },
  error(message, duration = 5000) { this.showToast(message, 'error', duration); },
  info(message, duration = 4000) { this.showToast(message, 'info', duration); },
  warning(message, duration = 4000) { this.showToast(message, 'warning', duration); },

  clearAll() {
    this.containerEl.querySelectorAll('.toast').forEach(el => {
      const instance = bootstrap.Toast.getInstance(el);
      if (instance) instance.hide();
    });
    this.pendingToasts = [];
  }
};

document.addEventListener('DOMContentLoaded', () => ToastManager.init());
window.ToastManager = ToastManager;
    this.container.appendChild(toastEl);
