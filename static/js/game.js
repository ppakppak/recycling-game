let score = 0;
let attempts = 0;
let currentItem = null;

// 서버 없이 동작하도록 수정된 버전
const ITEMS = [
    {name: '신문지', type: '종이'},
    {name: '페트병', type: '플라스틱'},
    {name: '비닐봉지', type: '비닐'},
    // ... 나머지 아이템들
];

let currentItems = [...ITEMS];  // 아이템 복사

async function getNewItem() {
    if (currentItems.length === 0) {
        currentItems = [...ITEMS];  // 아이템 리스트 리셋
    }
    const randomIndex = Math.floor(Math.random() * currentItems.length);
    const item = currentItems[randomIndex];
    currentItems.splice(randomIndex, 1);
    return item;
}

async function displayNewItem() {
    const item = await getNewItem();
    if (item.name === null) {
        endGame();
        return;
    }
    
    currentItem = item;
    document.getElementById('currentItem').textContent = item.name;
}

function updateScore() {
    document.getElementById('score').textContent = score;
}

function showMessage(msg) {
    document.getElementById('message').textContent = msg;
}

function endGame() {
    const message = score >= 10 
        ? "당신은 분리수거 고수!😎 앞으로도 환경을 위해 열심히 분리수거 해주세요😊"
        : "당신은 분리수거 허수ㅡㅡ 올바른 분리수거 방법을 배워보세요😎";
    showMessage(message);
    
    document.querySelectorAll('.bin').forEach(bin => {
        bin.style.pointerEvents = 'none';
    });
}

document.querySelectorAll('.bin').forEach(bin => {
    bin.addEventListener('click', async () => {
        if (!currentItem) return;
        
        attempts++;
        const selectedType = bin.dataset.type;
        
        if (selectedType === currentItem.type) {
            score++;
            updateScore();
            showMessage(`정확히 분리수거되었습니다! '${currentItem.name}'가 ${currentItem.type}로 분리되었습니다.`);
        } else {
            showMessage(`잘못된 분리수거! '${currentItem.name}'는 ${currentItem.type}입니다.`);
        }
        
        if (attempts >= 15) {
            endGame();
        } else {
            await displayNewItem();
        }
    });
});

// 게임 시작
displayNewItem(); 