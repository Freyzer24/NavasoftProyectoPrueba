

function cambiarFoto(input, imgElementId) {
  const file = input.files[0];
  if (file) {
      const reader = new FileReader();
      reader.onload = function(e) {
          document.getElementById(imgElementId).src = e.target.result;
      }
      reader.readAsDataURL(file);
  } else {
      // Puedes definir una imagen por defecto si no se selecciona ninguna
      document.getElementById(imgElementId).src = './imagenes/default-avatar.png'; // Cambia esta ruta por la de tu imagen por defecto
  }
}

// Añadiendo event listeners a los inputs de archivo
document.addEventListener('DOMContentLoaded', function() {
  const fotoInput = document.getElementById('foto');
  const fotoDosInput = document.getElementById('fotoDos');

  // Cambiar la foto del primer perfil
  fotoInput.addEventListener('change', function() {
      cambiarFoto(fotoInput, 'img');
  });

  // Cambiar la foto del segundo perfil
  fotoDosInput.addEventListener('change', function() {
      cambiarFoto(fotoDosInput, 'imgDos');
  });
});