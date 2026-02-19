document.addEventListener('DOMContentLoaded', function () {
  // Delete modal functionality
  var deleteModalEl = document.getElementById('deleteEntryModal');
  if (!deleteModalEl) return;

  var deleteModal = new bootstrap.Modal(deleteModalEl);
  var deleteForm = document.getElementById('deleteEntryForm');
  var deleteTitle = document.getElementById('deleteEntryTitle');
  var confirmBtn = document.getElementById('confirmDeleteBtn');

  document.querySelectorAll('.btn-delete-entry').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var url = btn.getAttribute('data-delete-url');
      var title = btn.getAttribute('data-entry-title') || 'this entry';

      if (deleteForm) deleteForm.setAttribute('action', url);
      if (deleteTitle) deleteTitle.textContent = title;

      deleteModal.show();
    });
  });

  if (deleteForm) {
    deleteForm.addEventListener('submit', function () {
      if (confirmBtn) {
        confirmBtn.disabled = true;
        confirmBtn.textContent = 'Deleting…';
      }
    });
  }
});
