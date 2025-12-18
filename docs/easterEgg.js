// 腾讯视频链接（替换为实际获取的带参数链接）
const videoUrl = "https://v.qq.com/txp/iframe/player.html?vid=s3233ejju5y&auto=1&mute=1";

// 暴露全局触发函数，供 Gameroom 等其他页面调用
window.triggerEasterEgg = function() {
    // 打开新窗口播放视频
    const videoWindow = window.open(videoUrl, "_blank", "width=1024,height=768");
    
    if (!videoWindow) {
        alert("弹窗被拦截！请在浏览器地址栏允许本站弹出窗口。");
        return;
    }

    // 尝试自动全屏（需等待视频加载，且受所有浏览器支持）
    setTimeout(() => {
        // 调用视频窗口的全屏API（需视频播放器支持）
        if (videoWindow && videoWindow.document) {
            try {
                const videoElement = videoWindow.document.querySelector("video");
                if (videoElement) {
                    // 尝试全屏（需用户交互触发，部分浏览器可能限制）
                    videoElement.requestFullscreen().catch((err) => {
                        console.log("全屏请求可能被浏览器阻止：", err);
                    });
                }
            } catch (e) {
                // 跨域或其他安全限制可能导致无法访问 videoWindow.document
                console.log("无法自动全屏：", e);
            }
        }
    }, 2000); // 延迟2秒，确保视频加载完成
};

document.addEventListener("DOMContentLoaded", () => {
    // 获取003的元素 (导航栏上的彩蛋链接)
    const easterEgg = document.getElementById("easterEgg");
    
    if (easterEgg) {
        // 点击事件
        easterEgg.addEventListener("click", (e) => {
    //        const target = e.target;
    //        target.style.display = "none"; // 隐藏元素
            e.preventDefault(); // 阻止默认跳转行为
            
            // 调用封装好的函数
            window.triggerEasterEgg();
        });
    }
});