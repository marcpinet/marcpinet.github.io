document.addEventListener('DOMContentLoaded', function() {
    let konamiCode = [];
    const correctCode = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];
    let matrixActive = false;
    let matrixCanvas = null;
    let matrixContext = null;
    let animationId = null;
    
    document.addEventListener('keydown', function(event) {
        konamiCode.push(event.keyCode);
        
        if (konamiCode.length > correctCode.length) {
            konamiCode.shift();
        }
        
        if (konamiCode.length === correctCode.length) {
            let isCorrect = true;
            for (let i = 0; i < correctCode.length; i++) {
                if (konamiCode[i] !== correctCode[i]) {
                    isCorrect = false;
                    break;
                }
            }
            
            if (isCorrect) {
                if (matrixActive) {
                    stopMatrixMode();
                } else {
                    startMatrixMode();
                }
                konamiCode = [];
            }
        }
    });
    
    function startMatrixMode() {
        matrixActive = true;
        
        matrixCanvas = document.createElement('canvas');
        matrixCanvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
            background: rgba(0, 0, 0, 0.1);
        `;
        
        document.body.appendChild(matrixCanvas);
        matrixContext = matrixCanvas.getContext('2d');
        
        resizeCanvas();
        window.addEventListener('resize', resizeCanvas);
        
        const columns = Math.floor(matrixCanvas.width / 20);
        const drops = Array(columns).fill(1);
        
        function draw() {
            matrixContext.fillStyle = 'rgba(0, 0, 0, 0.05)';
            matrixContext.fillRect(0, 0, matrixCanvas.width, matrixCanvas.height);
            
            matrixContext.fillStyle = '#0f0';
            matrixContext.font = '16px monospace';
            
            for (let i = 0; i < drops.length; i++) {
                const char = String.fromCharCode(Math.random() * 128);
                matrixContext.fillText(char, i * 20, drops[i] * 20);
                
                if (drops[i] * 20 > matrixCanvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
            
            if (matrixActive) {
                animationId = requestAnimationFrame(draw);
            }
        }
        
        draw();
        showMatrixMessage("MATRIX MODE ACTIVATED");
    }
    
    function stopMatrixMode() {
        matrixActive = false;
        
        if (animationId) {
            cancelAnimationFrame(animationId);
        }
        
        if (matrixCanvas) {
            document.body.removeChild(matrixCanvas);
            matrixCanvas = null;
            matrixContext = null;
        }
        
        window.removeEventListener('resize', resizeCanvas);
        showMatrixMessage("MATRIX MODE DEACTIVATED");
    }
    
    function resizeCanvas() {
        if (matrixCanvas) {
            matrixCanvas.width = window.innerWidth;
            matrixCanvas.height = window.innerHeight;
        }
    }
    
    function showMatrixMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.textContent = message;
        messageDiv.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #0f0;
            font-family: monospace;
            font-size: 24px;
            font-weight: bold;
            text-shadow: 0 0 10px #0f0;
            z-index: 10000;
            pointer-events: none;
            animation: matrixFade 3s ease-out forwards;
        `;
        
        const style = document.createElement('style');
        style.textContent = `
            @keyframes matrixFade {
                0% { opacity: 0; transform: translate(-50%, -50%) scale(0.5); }
                20% { opacity: 1; transform: translate(-50%, -50%) scale(1.1); }
                40% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
                100% { opacity: 0; transform: translate(-50%, -50%) scale(1); }
            }
        `;
        
        if (!document.head.querySelector('style[data-matrix]')) {
            style.setAttribute('data-matrix', 'true');
            document.head.appendChild(style);
        }
        
        document.body.appendChild(messageDiv);
        
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, 3000);
    }
});
