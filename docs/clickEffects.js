(function() {
    // 颜色库（糖果色）
    const colors = ['#ff5252', '#ff4081', '#e040fb', '#7c4dff', '#536dfe', '#448aff', '#40c4ff', '#18ffff', '#64ffda', '#69f0ae', '#b2ff59', '#eeff41', '#ffff00', '#ffd740', '#ffab40', '#ff6e40'];

    /**
     * 在指定位置产生粒子爆炸特效
     * @param {number} x - 屏幕 X 坐标
     * @param {number} y - 屏幕 Y 坐标
     * @param {number} count - 粒子数量 (默认 30)
     */
    function createExplosion(x, y, count = 30) {
        for (let i = 0; i < count; i++) {
            createParticle(x, y);
        }
    }

    function createParticle(x, y) {
        const particle = document.createElement('div');
        document.body.appendChild(particle);

        // 随机大小
        const size = Math.random() * 5 + 5; // 5px ~ 10px
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];
        
        // 初始位置
        particle.style.position = 'fixed';
        particle.style.left = `${x}px`;
        particle.style.top = `${y}px`;
        particle.style.borderRadius = '50%'; // 圆形粒子
        particle.style.pointerEvents = 'none'; // 避免粒子挡住点击
        particle.style.zIndex = '9999'; // 确保在最上层
        
        // 随机速度 (向四周爆炸)
        const angle = Math.random() * Math.PI * 2;
        const velocity = Math.random() * 4 + 2; // 速度范围
        let vx = Math.cos(angle) * velocity;
        let vy = Math.sin(angle) * velocity;
        
        // 物理变量
        let opacity = 1;
        const gravity = 0.2; // 重力
        const friction = 0.98; // 空气阻力

        // 动画函数
        function update() {
            vx *= friction;
            vy *= friction;
            vy += gravity; // 加上重力，让粒子下落

            x += vx;
            y += vy;
            opacity -= 0.02; // 逐渐消失

            particle.style.left = `${x}px`;
            particle.style.top = `${y}px`;
            particle.style.opacity = opacity;
            particle.style.transform = `scale(${opacity})`; // 随透明度缩小

            if (opacity > 0) {
                requestAnimationFrame(update);
            } else {
                particle.remove(); // 消失后移除元素
            }
        }

        requestAnimationFrame(update);
    }

    // 暴露给全局对象
    window.createExplosion = createExplosion;

    // 默认监听点击事件
    document.addEventListener('click', function(e) {
        // 如果点击的是可编辑区域，可能由该区域自己的事件处理，这里可以选择是否重复触发
        // 这里为了简单，全局点击都触发
        createExplosion(e.clientX, e.clientY);
    });

})();