// SCRIPT TODO MODAL
function openModelToDo(card_id) {
    document.getElementById('openModalToDoBtn' + card_id).addEventListener('click', function() {
        document.getElementById('modalToDo' + card_id).style.display = 'block';
    });
}

function closeButtonToDo(card_id) {
    document.getElementById('closeModalToDoBtn' + card_id).addEventListener('click', function() {
        document.getElementById('modalToDo' + card_id).style.display = 'none';
    });
}

function cancelToDo(card_id) {
    document.getElementById('cancelToDoBtn' + card_id).addEventListener('click', function() {
        document.getElementById('modalToDo' + card_id).style.display = 'none';
    });
}

function submitToDo(card_id){
    document.getElementById('modalToDoForm' + card_id).addEventListener('submit', function(event) {
        event.preventDefault();
        // Aqui você pode adicionar a lógica para salvar os dados
        document.getElementById('modalToDo' + card_id).style.display = 'none';
    });
}