// Sticky navbar scroll effect + smooth scrolling for in-page anchors
document.addEventListener("DOMContentLoaded", () => {
    const navbar = document.getElementById("mainNavbar");

    const onScroll = () => {
        if (!navbar) return;
        if (window.scrollY > 40) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    };
    onScroll();
    window.addEventListener("scroll", onScroll);

    document.querySelectorAll('a[href*="#"]').forEach((link) => {
        link.addEventListener("click", (e) => {
            const url = new URL(link.href, window.location.origin);
            if (url.pathname !== window.location.pathname) return;
            const hash = url.hash;
            if (!hash) return;
            const target = document.querySelector(hash);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        });
    });

    // Auto-dismiss flash alerts after a few seconds
    document.querySelectorAll(".fs-alert").forEach((alertEl) => {
        setTimeout(() => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
            bsAlert.close();
        }, 6000);
    });
});
