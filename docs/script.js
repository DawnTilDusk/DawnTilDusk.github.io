document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("toggleProgressBtn");
    const contentWrapper = document.getElementById("progressContentWrapper");
    let isExpanded = false; // 初始状态：收回

  // 点击按钮切换状态
    toggleBtn.addEventListener("click", () => {
    isExpanded = !isExpanded;

    // 控制内容显示/隐藏
    if (isExpanded) {
        contentWrapper.classList.add("show");
        toggleBtn.classList.add("expanded"); // 按钮添加展开类（箭头旋转）
    } 
    else {
        contentWrapper.classList.remove("show");
        toggleBtn.classList.remove("expanded"); // 移除展开类（箭头复位）
    }
    });
});
            
            
            
            
            const progressSectionsContainer = document.getElementById("progressSectionContainer");
            const progressContent = document.getElementById("progressContent");
            const addProgressBtn = document.getElementById("addProgressBtn");
            const progress = {};
            const STORAGE_KEY = "dawn_til_dusk_progress";

            // Load data on startup
            loadFromLocalStorage();

            function saveToLocalStorage() {
                const tasks = [];
                const sections = progressSectionsContainer.querySelectorAll(".progress-section");
                sections.forEach(section => {
                    const nameKey = section.dataset.nameKey;
                    const name = section.querySelector(".name").textContent;
                    const value = progress[nameKey];
                    tasks.push({ name, value });
                });
                localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks));
            }

            function loadFromLocalStorage() {
                const data = localStorage.getItem(STORAGE_KEY);
                if (data) {
                    try {
                        const tasks = JSON.parse(data);
                        tasks.forEach(task => {
                            addProgress(task.name, task.value, false);
                        });
                    } catch (e) {
                        console.error("Failed to load progress:", e);
                    }
                }
            }

 /*           increaseBtn.addEventListener("click", (nameKey) => {
                progress[nameKey] += 1;
                updateProgress(nameKey);
            });

            decreaseBtn.addEventListener("click", (nameKey) => {
                progress[nameKey] -= 1;
                updateProgress(nameKey);
            });*/

            function updateProgress(progressSection, nameKey) {
                const progressBar = progressSection.querySelector(".progress-bar");
                const progressText = progressSection.querySelector(".progress-text");   

                progressBar.style.width = progress[nameKey] + "%";
                progressText.textContent = progress[nameKey] + "%";

                if (progress[nameKey] <= 0) {
                    progressText.classList.add('fixed-center');
                    progressText.classList.add('col0');
                }

                else if (progress[nameKey] > 100) {
                    progressText.classList.add('fixed-center');
                    progressText.classList.add('col1');
                }

                else {
                    progressText.classList.remove('fixed-center');
                    progressText.classList.remove('col0');
                    progressText.classList.remove('col1');
                }
            }

            function addProgress(name, value = 0, save = true){                  
                const progressSection = document.createElement("div");
                progressSection.className = "progress-section";

                // 验证输入
                if (!name.trim()) {
                    alert("请输入有效的任务名称！");
                    return;
                }

                // 标准化任务名（避免重复）
                const nameKey = name.toLowerCase().replace(/\s+/g, '');
                if (progress[nameKey] !== undefined) {
                    alert(`"${name}" 已存在，请输入其他任务！`);
                    return;
                }
                
                progress[nameKey] = value;
                progressSection.dataset.nameKey = nameKey;

                progressSection.innerHTML = `  
                    <div class="progress-controls">
                        <span class="name">${name}</span>
                        <button class="btn add-btn btn-hover" data-action="increase">+</button>
                        <button class="btn sub-btn btn-hover" data-action="decrease">-</button>
                        <button class="btn reset-btn btn-hover" data-action="reset">重置</button>
                        <button class="btn remove-btn btn-hover" data-action="remove">删除</button>
                    </div>

                    <div class="progress-container">
                        <div class="progress-bar">
                            <div class="progress-text">0%</div>
                        </div>
                    </div>                    
                `;
                progressSectionContainer.appendChild(progressSection);
                updateProgress(progressSection, nameKey); // Ensure styling is correct
                if (save) {
                    saveToLocalStorage();
                }
            }    

            progressSectionsContainer.addEventListener('click', (e) => {
                const progressSection = e.target.closest('.progress-section');
                if (!progressSection) return;

                const action = e.target.dataset.action;
                const nameKey = progressSection.dataset.nameKey;

                switch (action) {
                    case "increase":
                        progress[nameKey] += 1;
                        break;
                    case "decrease":                        
                        progress[nameKey] -= 1;
                        break;                    
                    case "remove":
                        progressSectionsContainer.removeChild(progressSection);
                        delete progress[nameKey];
                        break;
                    case "reset":
                        progress[nameKey] = 0;
                        break;
                }   
                if (action !== "remove") {
                    updateProgress(progressSection, nameKey);
                }
                saveToLocalStorage();
            });

            progressContent.addEventListener("keypress", (e) => {
                if (e.key === "Enter") {
                    addProgress(progressContent.value.trim());
                    progressContent.value = "";
                }
            });
                
            addProgressBtn.addEventListener("click", () => {
                addProgress(progressContent.value.trim());
                progressContent.value = "";
            });