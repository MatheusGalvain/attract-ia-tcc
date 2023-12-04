// SCRIPT InProgress MODAL
function openModelInProgress(card_id) {
  document.getElementById('openModalInProgressBtn' + card_id).addEventListener('click', function() {
      document.getElementById('modalInProgress' + card_id).style.display = 'block';
  });
}

function closeButtonInProgress(card_id) {
  document.getElementById('closeModalInProgressBtn' + card_id).addEventListener('click', function() {
      document.getElementById('modalInProgress' + card_id).style.display = 'none';
  });
}

function cancelInProgress(card_id) {
  document.getElementById('cancelInProgressBtn' + card_id).addEventListener('click', function() {
      document.getElementById('modalInProgress' + card_id).style.display = 'none';
  });
}

function submitInProgress(card_id) {
  document.getElementById('modalInProgressForm' + card_id).addEventListener('submit', function(event) {
      event.preventDefault();
      // Aqui você pode adicionar a lógica para salvar os dados
      document.getElementById('modalInProgress' + card_id).style.display = 'none';
  });
}