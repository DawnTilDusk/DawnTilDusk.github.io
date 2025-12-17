(function() {
    // 默认配置
    const defaultConfig = {
        leftClick: true,
        rightClick: true,
        typing: true
    };

    // 从 localStorage 读取配置，如果没有则使用默认值
    let config = JSON.parse(localStorage.getItem('particleEffectsConfig')) || defaultConfig;

    // 颜色库（糖果色）
    const colors = ['#ff5252', '#ff4081', '#e040fb', '#7c4dff', '#536dfe', '#448aff', '#40c4ff', '#18ffff', '#64ffda', '#69f0ae', '#b2ff59', '#eeff41', '#ffff00', '#ffd740', '#ffab40', '#ff6e40'];

    /**
     * 保存配置到 localStorage
     */
    function saveConfig() {
        localStorage.setItem('particleEffectsConfig', JSON.stringify(config));
    }

    /**
     * 更新配置
     * @param {string} key - 配置项名称 (leftClick, rightClick, typing)
     * @param {boolean} value - 启用或禁用
     */
    function setConfig(key, value) {
        if (key in config) {
            config[key] = value;
            saveConfig();
        }
    }

    /**
     * 获取当前配置
     * @returns {object}
     */
    function getConfig() {
        return { ...config };
    }

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

    // --- 事件监听 ---

    // 1. 左键点击特效
    document.addEventListener('click', function(e) {
        if (config.leftClick) {
            createExplosion(e.clientX, e.clientY, 30);
        }
    });

    // 2. 右键点击特效
    document.addEventListener('contextmenu', function(e) {
        if (config.rightClick) {
            // 注意：不阻止默认菜单，只添加特效。如果需要阻止，可以加 e.preventDefault()
            createExplosion(e.clientX, e.clientY, 30);
        }
    });

    // 3. 打字特效 (Input 事件)
    // 辅助函数：尝试获取输入框中光标的像素坐标
    // 这是一个简化版本，对于 textarea 和 input 不一定完全精准，但比默认右侧好
    function getCursorXY(input, selectionPoint) {
        const {
            offsetLeft: inputX,
            offsetTop: inputY,
        } = input;
        
        // 创建一个镜像 div 来模拟输入框内容
        const div = document.createElement('div');
        
        // 复制输入框样式
        const copyStyle = getComputedStyle(input);
        for (const prop of copyStyle) {
            div.style[prop] = copyStyle[prop];
        }
        
        // 关键样式重写
        div.style.position = 'absolute';
        div.style.top = '0px';
        div.style.left = '0px';
        div.style.visibility = 'hidden';
        div.style.whiteSpace = 'pre-wrap';
        
        // 复制内容直到光标位置
        const swap = '.';
        const inputValue = input.tagName === 'INPUT' ? input.value.replace(/ /g, swap) : input.value;
        const textContent = inputValue.substr(0, selectionPoint);
        div.textContent = textContent;
        
        // 插入标记点
        const span = document.createElement('span');
        span.textContent = '|';
        div.appendChild(span);
        
        document.body.appendChild(div);
        
        const { offsetLeft: spanX, offsetTop: spanY } = span;
        const rect = input.getBoundingClientRect();

        document.body.removeChild(div);
        
        // 计算最终坐标 (相对于视口)
        // 注意：这种方法对于 input type="text" 的横向滚动支持有限，但对于简单情况够用
        // 更稳妥的 fallback 依然是元素边缘
        
        return {
            x: rect.left + spanX - input.scrollLeft,
            y: rect.top + spanY - input.scrollTop + rect.height / 2 // 垂直居中稍微好点
        };
    }

    document.addEventListener('input', function(e) {
        if (!config.typing) return;

        let x, y;
        
        // 情况 A: ContentEditable 元素 (如我们的测试页)
        // 这里的 Selection API 是准确的
        if (e.target.isContentEditable) {
            const selection = window.getSelection();
            if (selection.rangeCount > 0) {
                const range = selection.getRangeAt(0);
                const rects = range.getClientRects();
                const rect = rects.length > 0 ? rects[0] : null;
                if (rect) {
                    x = rect.left;
                    y = rect.top + rect.height / 2;
                }
            }
        }
        
        // 情况 B: Input / Textarea 元素
        // 使用 Fallback：在元素右侧边缘，稍微往里一点
        if (x === undefined && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) {
             const targetRect = e.target.getBoundingClientRect();
             
             // 策略：始终在输入框的“当前内容末尾”或者“右侧内边距”处
             // 简单起见，我们在输入框的右边缘 (减去一点 padding) 垂直居中位置
             // 这样看起来像是从输入框里“喷”出来的
             x = targetRect.right - 10; 
             y = targetRect.top + targetRect.height / 2;
        }

        if (x !== undefined && y !== undefined) {
            createExplosion(x, y, 10); // 打字粒子少一点
        }
    }, true); // 使用捕获阶段，确保尽可能早地捕获

    // 暴露给全局对象
    window.ParticleEffects = {
        createExplosion: createExplosion,
        setConfig: setConfig,
        getConfig: getConfig
    };

})();