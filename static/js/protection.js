// ========================================
// Website Protection Script
// Disables: Right-click, Inspect, DevTools, Copy
// ========================================

(function() {
    'use strict';

    // 1. Disable Right Click
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        showAlert('Right-click disabled for security!');
        return false;
    });

    // 2. Disable F12 (DevTools)
    document.addEventListener('keydown', function(e) {
        // F12
        if (e.keyCode === 123) {
            e.preventDefault();
            showAlert('Developer tools are disabled!');
            return false;
        }
        
        // Ctrl+Shift+I (Inspect)
        if (e.ctrlKey && e.shiftKey && e.keyCode === 73) {
            e.preventDefault();
            showAlert('Inspect Element is disabled!');
            return false;
        }
        
        // Ctrl+Shift+J (Console)
        if (e.ctrlKey && e.shiftKey && e.keyCode === 74) {
            e.preventDefault();
            showAlert('Console is disabled!');
            return false;
        }
        
        // Ctrl+U (View Source)
        if (e.ctrlKey && e.keyCode === 85) {
            e.preventDefault();
            showAlert('View Source is disabled!');
            return false;
        }
        
        // Ctrl+Shift+C (Inspect Element)
        if (e.ctrlKey && e.shiftKey && e.keyCode === 67) {
            e.preventDefault();
            return false;
        }
        
        // Ctrl+S (Save Page)
        if (e.ctrlKey && e.keyCode === 83) {
            e.preventDefault();
            showAlert('Saving page is disabled!');
            return false;
        }
    });

    // 3. Disable Text Selection (Optional)
    document.addEventListener('selectstart', function(e) {
        e.preventDefault();
        return false;
    });

    // 4. Disable Copy
    document.addEventListener('copy', function(e) {
        e.preventDefault();
        showAlert('Copying content is disabled!');
        return false;
    });

    // 5. Disable Cut
    document.addEventListener('cut', function(e) {
        e.preventDefault();
        return false;
    });

    // 6. Detect DevTools Opening (Advanced)
    let devtoolsOpen = false;
    const threshold = 160;

    setInterval(function() {
        if (window.outerWidth - window.innerWidth > threshold || 
            window.outerHeight - window.innerHeight > threshold) {
            if (!devtoolsOpen) {
                devtoolsOpen = true;
                document.body.innerHTML = '<h1 style="text-align:center;margin-top:20%;color:#d32f2f;">⚠️ Developer Tools Detected! Page Disabled.</h1>';
            }
        }
    }, 1000);

    // 7. Disable Drag and Drop
    document.addEventListener('dragstart', function(e) {
        e.preventDefault();
        return false;
    });

    // 8. Alert Function
    function showAlert(message) {
        // Create custom alert (optional - remove if annoying)
        console.warn(message);
        // Uncomment below for popup alerts
        // alert(message);
    }

    // 9. Disable Print Screen (Detection only)
    document.addEventListener('keyup', function(e) {
        if (e.key === 'PrintScreen') {
            navigator.clipboard.writeText('');
            showAlert('Screenshots disabled!');
        }
    });

    // 10. Watermark on page (Optional - Discourage screenshots)
    function addWatermark() {
        const watermark = document.createElement('div');
        watermark.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-45deg);
            font-size: 80px;
            color: rgba(211, 47, 47, 0.1);
            pointer-events: none;
            z-index: 9999;
            user-select: none;
            font-weight: bold;
        `;
        watermark.textContent = 'MANOVASTRA.NET';
        document.body.appendChild(watermark);
    }
    // addWatermark(); // Uncomment to enable watermark

    console.log('%c⚠️ WARNING!', 'font-size: 50px; color: red; font-weight: bold;');
    console.log('%cThis website is protected. Unauthorized access is prohibited.', 'font-size: 20px; color: #d32f2f;');
})();
