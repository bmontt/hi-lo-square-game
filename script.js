let deck = [];  // Array to hold the deck of cards
let selectedCard = null;
let messageArea = document.getElementById('messageArea');
let cardArea = document.getElementById('cardArea');

function shuffleDeck() {
    const suits = ['hearts', 'diamonds', 'clubs', 'spades'];
    const ranks = ['02', '03', '04', '05', '06', '07', '08', '09', '10', 'J', 'Q', 'K', 'A'];
    deck = [];

    suits.forEach(suit => {
        ranks.forEach(rank => {
            deck.push({rank: rank, suit: suit});
        });
    });

    // Shuffle the deck
    deck.sort(() => Math.random() - 0.5);
    displayCard();
}

function displayCard() {
    if (deck.length > 0) {
        selectedCard = deck.pop();
        cardArea.innerHTML = `<div>${selectedCard.rank} of ${selectedCard.suit}</div>`;
    } else {
        messageArea.textContent = "No more cards!";
    }
}

function playTurn(guess) {
    if (!selectedCard) {
        messageArea.textContent = "No card selected!";
        return;
    }

    let nextCard = deck.length > 0 ? deck.pop() : null;
    if (!nextCard) {
        messageArea.textContent = "No more cards!";
        return;
    }

    cardArea.innerHTML = `<div>${nextCard.rank} of ${nextCard.suit}</div>`;

    // Compare ranks (you'll need to write a function to convert ranks to numerical values)
    if ((guess === 'higher' && nextCard.rank > selectedCard.rank) ||
        (guess === 'lower' && nextCard.rank < selectedCard.rank) ||
        (guess === 'post' && nextCard.rank === selectedCard.rank)) {
        messageArea.textContent = "Correct!";
    } else {
        messageArea.textContent = "Wrong!";
    }

    selectedCard = nextCard; // Update the selected card
}

function resetGame() {
    shuffleDeck();
    messageArea.textContent = "";
}

window.onload = resetGame;
