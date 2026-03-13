document.addEventListener('DOMContentLoaded', () => {

    // Initialize tsParticles Geometry Tech Background
    if (typeof tsParticles !== 'undefined') {
        tsParticles.load("tsparticles", {
            fpsLimit: 60,
            interactivity: {
                events: {
                    onClick: { enable: true, mode: "push" },
                    onHover: { enable: true, mode: "grab" },
                    resize: true,
                },
                modes: {
                    push: { quantity: 4 },
                    grab: { distance: 200, links: { opacity: 0.5 } }
                },
            },
            particles: {
                color: { value: ["#2563eb", "#7c3aed", "#e11d48"] }, // Deeper, more saturated colors
                links: {
                    color: "#94a3b8", // visible slate grey for light mode
                    distance: 150,
                    enable: true,
                    opacity: 0.4, // increased opacity for visibility
                    width: 1,
                },
                move: {
                    direction: "none",
                    enable: true,
                    outModes: { default: "bounce" },
                    random: false,
                    speed: 1,
                    straight: false,
                },
                number: {
                    density: { enable: true, area: 800 },
                    value: 60,
                },
                opacity: { value: 0.5 },
                shape: { type: "circle" },
                size: { value: { min: 1, max: 4 } },
            },
            detectRetina: true,
        });
    }

    // Initialize Typed.js for Subtitle
    if (typeof Typed !== 'undefined') {
        new Typed('#typed-subtitle', {
            strings: ['A premium, responsive dashboard to visualize Operating System algorithms in real-time.', 'Sync your workflow and analyze OS concepts with extreme precision.', 'Experience next-gen 3D visual tools for CPU, Memory, and Disk Scheduling.'],
            typeSpeed: 40,
            backSpeed: 20,
            backDelay: 3000,
            loop: true,
            showCursor: true,
            cursorChar: '|'
        });
    }

    // Custom Cursor Logic
    const cursor = document.querySelector('.custom-cursor');
    const follower = document.querySelector('.custom-cursor-follower');
    
    if (cursor && follower) {
        document.addEventListener('mousemove', (e) => {
            cursor.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
            follower.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
        });

        // Add hover effect classes to links and buttons
        const interactives = document.querySelectorAll('a, button, input, select, .feature-card, .glass-panel');
        interactives.forEach(el => {
            el.addEventListener('mouseenter', () => {
                cursor.classList.add('hover');
                follower.classList.add('hover');
            });
            el.addEventListener('mouseleave', () => {
                cursor.classList.remove('hover');
                follower.classList.remove('hover');
            });
        });
    }

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

    // Initialize VanillaTilt for elements with data-tilt that might be loaded dynamically
    if (typeof VanillaTilt !== 'undefined') {
        VanillaTilt.init(document.querySelectorAll(".feature-card"), {
            max: 10,
            speed: 400,
            glare: true,
            "max-glare": 0.5,
        });
    }

    // Interactive abstract UI tracking
    const panel = document.querySelector('.glass-panel');
    const heroContent = document.querySelector('.hero-content');

    // Intense parallax effect on mouse move in the hero area
    document.addEventListener('mousemove', (e) => {
        if (!panel) return;

        // Only run if screen is wide enough
        if (window.innerWidth < 768) return;

        const mouseX = e.clientX / window.innerWidth - 0.5;
        const mouseY = e.clientY / window.innerHeight - 0.5;

        // Move the panel and blobs slightly opposite to mouse movement
        // VanillaTilt handles the panel rotation, but we can exaggerate the translation
        panel.style.transform = `perspective(1000px) translateY(${-mouseY * 30}px) translateX(${-mouseX * 30}px)`;

        // Subtle background blob shift
        const blobs = document.querySelectorAll('.blob');
        blobs.forEach((blob, i) => {
            const factor = (i + 1) * 30; // Increased factor for more pronounced movement
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
