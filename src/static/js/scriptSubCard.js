// SCRIPT TODO MODAL
function openModelSubCard(card_id) {
    document.getElementById('openModalSubCardBtn' + card_id).addEventListener('click', function() {
        document.getElementById('modalSubCard' + card_id).style.display = 'block';
    });
}

function closeButtonSubCard(sub_card_id) {
    document.getElementById('closeModalSubCardBtn' + sub_card_id).addEventListener('click', function() {
        document.getElementById('modalSubCard' + sub_card_id).style.display = 'none';
    });
}

function cancelSubCard(sub_card_id) {
    document.getElementById('cancelSubCardBtn' + sub_card_id).addEventListener('click', function() {
        document.getElementById('modalSubCard' + sub_card_id).style.display = 'none';
    });
}

function submitSubCard(sub_card_id){
    document.getElementById('modalSubCardForm' + sub_card_id).addEventListener('submit', function(event) {
        event.preventDefault();
        // Aqui você pode adicionar a lógica para salvar os dados
        document.getElementById('modalSubCard' + sub_card_id).style.display = 'none';
    });
}