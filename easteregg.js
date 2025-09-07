document.addEventListener("DOMContentLoaded", () => {
    // 获取003的元素
    const easterEgg = document.getElementById("easterEgg");
    
    // 腾讯视频链接（替换为实际获取的带参数链接）
    const videoUrl = "https://v.qq.com/txp/iframe/player.html?vid=s3233ejju5y&auto=1&mute=1";
    
    // 点击事件
    easterEgg.addEventListener("click", (e) => {
        e.preventDefault(); // 阻止默认跳转行为
        
        // 打开新窗口播放视频
        const videoWindow = window.open(videoUrl, "_blank", "width=1024,height=768");
        
        // 尝试自动全屏（需等待视频加载，且受所有浏览器支持）
        setTimeout(() => {
            // 调用视频窗口的全屏API（需视频播放器支持）
            if (videoWindow && videoWindow.document) {
                const videoElement = videoWindow.document.querySelector("video");
                if (videoElement) {
                    // 尝试全屏（需用户交互触发，部分浏览器可能限制）
                    videoElement.requestFullscreen().catch((err) => {
                        console.log("全屏请求可能被浏览器阻止：", err);
                    });
                }
            }
        }, 2000); // 延迟2秒，确保视频加载完成
    });
});