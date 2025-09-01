$(document).ready(function() {
    // Newsletter form submission
    $('#newsletterForm').on('submit', function(e) {
        e.preventDefault();
        var form = $(this);
        var responseDiv = $('#newsletterResponse');
        
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(data) {
                if (data.success) {
                    responseDiv.html('<div class="alert alert-success">Thanks for subscribing!</div>');
                    form[0].reset();
                } else {
                    var errors = '';
                    for (var key in data.errors) {
                        errors += data.errors[key] + '<br>';
                    }
                    responseDiv.html('<div class="alert alert-danger">' + errors + '</div>');
                }
            },
            error: function() {
                responseDiv.html('<div class="alert alert-danger">An error occurred. Please try again.</div>');
            }
        });
    });
    
    // Contact form submission
    $('#contactForm').on('submit', function(e) {
        e.preventDefault();
        var form = $(this);
        var submitButton = form.find('button[type="submit"]');
        var originalText = submitButton.text();
        
        submitButton.prop('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Sending...');
        
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(data) {
                if (data.success) {
                    form.html('<div class="alert alert-success">Your message has been sent successfully!</div>');
                } else {
                    var errors = '';
                    for (var key in data.errors) {
                        errors += data.errors[key] + '<br>';
                    }
                    form.prepend('<div class="alert alert-danger">' + errors + '</div>');
                    submitButton.prop('disabled', false).text(originalText);
                }
            },
            error: function() {
                form.prepend('<div class="alert alert-danger">An error occurred. Please try again.</div>');
                submitButton.prop('disabled', false).text(originalText);
            }
        });
    });
    
    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(event) {
        event.preventDefault();
        $('html, body').animate({
            scrollTop: $($.attr(this, 'href')).offset().top - 70
        }, 500);
    });
    
    // Initialize tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();
    
    // Sidebar sliding on mobile
    $('.sidebar-toggle').on('click', function() {
        $('.sidebar').toggleClass('active');
    });
});