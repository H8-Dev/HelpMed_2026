function toggleModal(show) {
      const modal = document.getElementById('modalOverlay');
      if (show) {
        modal.classList.add('active');
      } else {
        modal.classList.remove('active');
      }
    }