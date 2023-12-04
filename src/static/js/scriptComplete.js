// SCRIPT Complete MODAL
function openModelComplete(card_id) {
    document.getElementById('openModalCompleteBtn' + card_id).addEventListener('click', function() {
        document.getElementById('modalComplete' + card_id).style.display = 'block';
    });
  }
  
  function closeButtonComplete(card_id) {
    document.getElementById('closeModalCompleteBtn' + card_id).addEventListener('click', function() {
        document.getElementById('modalComplete' + card_id).style.display = 'none';
    });
  }
  
  function cancelComplete(card_id) {
    document.getElementById('cancelCompleteBtn' + card_id).addEventListener('click', function() {
        document.getElementById('modalComplete' + card_id).style.display = 'none';
    });
  }
  
  function submitComplete(card_id){
    document.getElementById('modalCompleteForm' + card_id).addEventListener('submit', function(event) {
        event.preventDefault();
        // Aqui você pode adicionar a lógica para salvar os dados
        document.getElementById('modalComplete' + card_id).style.display = 'none';
    });
  }