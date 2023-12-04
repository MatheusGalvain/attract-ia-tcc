document.getElementById('openModalBtn').addEventListener('click', function() {
    document.getElementById('modal').style.display = 'block';
  });
  
  document.getElementById('closeModalBtn').addEventListener('click', function() {
    document.getElementById('modal').style.display = 'none';
  });
  
  document.getElementById('cancelBtn').addEventListener('click', function() {
    document.getElementById('modal').style.display = 'none';
  });
  
  document.getElementById('modalForm').addEventListener('submit', function(event) {
    event.preventDefault();
    // Aqui você pode adicionar a lógica para salvar os dados
    document.getElementById('modal').style.display = 'none';
  });