// Sidebar Toggle 
window.addEventListener('DOMContentLoaded', event => {

  // Toggle the side navigation
  const sidebarToggle = document.body.querySelector('#sidebarToggle');
  const sidebarClose = document.body.querySelector('#sidebarClose');
  if (sidebarToggle) {
    //   if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
    //       document.body.classList.toggle('sb-sidenav-toggled');
    //   }
      sidebarToggle.addEventListener('click', event => {
          event.preventDefault();
          document.body.classList.toggle('sb-sidenav-toggled');
        //   localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
      });
      sidebarClose.addEventListener('click', event => {
          event.preventDefault();
          document.body.classList.toggle('sb-sidenav-toggled');
        //   localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
      });
  }

});

$('textarea').keyup(function() {
    
  var characterCount = $(this).val().length,
      current = $('#current'),
      maximum = $('#maximum'),
      theCount = $('#the-count');
    
  current.text(characterCount);
  
  if (characterCount >= 30) {
    maximum.css('color', '#52D89C');
    current.css('color', '#52D89C');  
  } else {
    maximum.css('color','#FF7B5D'); 
  }
  
      
});
