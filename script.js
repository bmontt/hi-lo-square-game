let deck = [];  // Array to hold the deck of cards
let selectedCard = null;
let deckImage = document.getElementById('deckImage');
let deckCount = 52;
let cardArea = document.getElementById('cardArea');
let cardCountArea = document.getElementById('cardCount');
let messageArea = document.getElementById('messageArea');
function shuffleDeck() {
    const suits = ['hearts', 'diamonds', 'clubs', 'spades'];
    const ranks = ['02', '03', '04', '05', '06', '07', '08', '09', '10', 'J', 'Q', 'K', 'A'];
    deck = suits.flatMap(suit => ranks.map(rank => ({rank, suit})));
    deck = deck.sort(() => 0.5 - Math.random());
    updateDeckCount();
    populateCardGrid();
}

function populateCardGrid() {
    const cardGrid = document.getElementById('cardGrid');
    cardGrid.innerHTML = '';
    deck.slice(0, 9).forEach(card => {  // Only take the first 9 cards for the grid
        let cardElement = document.createElement('div');
        cardElement.className = 'card';
        cardElement.style.backgroundImage = `url(assets/images/card_${card.suit}_${card.rank}.png)`;  // Default to card back image
        cardElement.onclick = () => selectCard(card, cardElement);
        cardGrid.appendChild(cardElement);
    });
}

function selectCard(card, cardElement) {
    // Deselect any previously selected card
    if (selectedCard) {
        selectedCard.element.classList.remove('selected'); // Assuming 'selected' class will highlight the card
    }
    
    // Update the selected card
    selectedCard = { ...card, element: cardElement };
    cardElement.classList.add('selected');
    messageArea.textContent = `Selected ${card.rank} of ${card.suit}`;
}

function toggleCard(cardElement) {
    cardElement.classList.toggle('is-flipped');
}

function displayCard(card) {
    const imagePath = `assets/images/card_${card.suit}_${card.rank}.png`;
    deckImage.src = imagePath;
}

function updateDeckCount() {
    deckCount.textContent = deck.length;
}

function disableGameControls(disable) {
    document.querySelectorAll("button").forEach(button => {
        button.disabled = disable;
    });
}

function rankToInt(rank) {
    const rankValues = {
        '02': 2, '03': 3, '04': 4, '05': 5, '06': 6, '07': 7, '08': 8, '09': 9, '10': 10,
        'J': 11, 'Q': 12, 'K': 13, 'A': 14
    };
    return rankValues[rank];
}

function playTurn(guess) {
    checkEndCond();
    if (!selectedCard) {
        messageArea.textContent = "No card selected!";
        return;
    }
    let nextCard = deck.pop();
    displayCard(nextCard);
    updateDeckCount();

    let chosenRank = rankToInt(selectedCard.rank);
    let nextRank = rankToInt(nextCard.rank);
    
    if ((guess === 'higher' && nextRank > chosenRank) ||
        (guess === 'lower' && nextRank < chosenRank) ||
        (guess === 'post' && nextRank === chosenRank)) {
        messageArea.textContent = "Correct! Next card was " + nextRank + " of " + nextCard.suit;
        // playSound('correctSound'); // Assuming you have a correct sound
        selectedCard.element.classList.remove('selected'); // Deselect the card visually
    } else {
        messageArea.textContent = "Wrong! Next card was " + nextRank + " of " + nextCard.suit;
        // playSound('wrongSound'); // Assuming you have a wrong sound
        selectedCard.element.classList.add('wrong'); // Optionally mark the wrong choice
    }

    selectedCard = null;
}

function checkEndCond() {
    // loss cond
    if (flippedPiles >= 9) {
        messageArea.textContent = "Game Over. Better luck next time!";
    }
    // win cond
    if (deck.length === 0) { 
        messageArea.textContent = "You Win! No more cards left.";
        disableGameControls(true);
    }
}


function playSound(soundId) {
    const sound = document.getElementById(soundId);
    if (sound) {
        sound.play();
    }
}

function resetGame() {
    shuffleDeck();
    messageArea.textContent = "";
    disableGameControls(false);
    selectedCard = null;
}

window.onload = resetGame;