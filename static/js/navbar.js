document.addEventListener('DOMContentLoaded', function() {
  const toggleButton = document.querySelector('.mobile-menu-toggle');
  const navbarLinks = document.getElementById('main-nav-links');
  
  if (!toggleButton || !navbarLinks) {
    console.error('Essential navbar elements missing');
    return;
  }

  toggleButton.addEventListener('click', function() {
    // Toggle menu visibility
    navbarLinks.classList.toggle('active');
    
    // Toggle hamburger animation
    this.classList.toggle('open');
    
    // Update ARIA attribute
    const isExpanded = this.classList.contains('open');
    this.setAttribute('aria-expanded', isExpanded);
  });
  
  // Close menu when clicking on links (optional)
  navbarLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 768) {
        navbarLinks.classList.remove('active');
        toggleButton.classList.remove('open');
        toggleButton.setAttribute('aria-expanded', 'false');
      }
    });
  });
});