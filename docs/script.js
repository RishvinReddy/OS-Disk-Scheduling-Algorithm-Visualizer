document.addEventListener('DOMContentLoaded', () => {
    // Smooth scrolling for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Intersection Observer for fade-in animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Add a small delay based on index to create a staggered animation effect
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 100);

                // Unobserve after animating once
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all feature cards
    document.querySelectorAll('.feature-card').forEach(card => {
        observer.observe(card);
    });

    // Interactive abstract UI tracking
    const panel = document.querySelector('.glass-panel');
    const heroContent = document.querySelector('.hero-content');

    // Slight parallax effect on mouse move in the hero area
    document.addEventListener('mousemove', (e) => {
        if (!panel) return;

        // Only run if screen is wide enough
        if (window.innerWidth < 768) return;

        const mouseX = e.clientX / window.innerWidth - 0.5;
        const mouseY = e.clientY / window.innerHeight - 0.5;

        // Move the panel and blobs slightly opposite to mouse movement
        panel.style.transform = `perspective(1000px) rotateX(${5 - mouseY * 10}deg) rotateY(${mouseX * 10}deg) translateY(${-mouseY * 20}px)`;

        // Subtle background blob shift
        const blobs = document.querySelectorAll('.blob');
        blobs.forEach((blob, i) => {
            const factor = (i + 1) * 15;
            blob.style.transform = `translate(${mouseX * factor}px, ${mouseY * factor}px)`;
        });
    });

    // Reset transforms when mouse leaves document
    document.addEventListener('mouseleave', () => {
        if (panel && window.innerWidth >= 768) {
            panel.style.transform = `perspective(1000px) rotateX(5deg)`;
        }
    });
});
