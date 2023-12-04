// SCRIPT InProgress MODAL
function openModelSubActivite(card_id) {
    document.getElementById('openModalSubActiviteBtn' + card_id).addEventListener('click', function () {
        document.getElementById('modalSubActivite' + card_id).style.display = 'block';
    });
}

function closeButtonSubActivite(card_id) {
    document.getElementById('closeModalSubActiviteBtn' + card_id).addEventListener('click', function () {
        document.getElementById('modalSubActivite' + card_id).style.display = 'none';
    });
}

function cancelSubActivite(card_id) {
    document.getElementById('cancelSubActiviteBtn' + card_id).addEventListener('click', function () {
        document.getElementById('modalSubActivite' + card_id).style.display = 'none';
    });
}
