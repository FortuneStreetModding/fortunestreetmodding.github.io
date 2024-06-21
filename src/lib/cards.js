var effectGroups = [
    "Buy Suit Yourself",
    "Buy stocks in district",
    "Buy unowned shop",
    "Cameo adventure",
    "Choose way to move",
    "Drop wallet",
    "Expand one shop",
    "Forced auction",
    "Forced buyout",
    "Free Suit Yourself",
    "Free stocks",
    "Free suit",
    "Get big commission",
    "Get gold x level",
    "Give everyone gold",
    "Give to last place",
    "Impromptu party",
    "Invest bank's money",
    "Invest capital",
    "Move forward",
    "Other players movement",
    "Pay assets tax",
    "Pay last place",
    "Play arcade games",
    "Price hike",
    "Random district shops drop",
    "Random district stocks decrease",
    "Random district stocks increase",
    "Receive most valuable stocks",
    "Receive gold x shops",
    "Receive half salary",
    "Receive stocks in random district",
    "Roll after shop price change",
    "Roll and expand shops",
    "Roll and get from 1st",
    "Roll and get from all",
    "Roll and get from bank",
    "Roll and move forward",
    "Roll random to close shops",
    "Roll random to expand shops",
    "Roll random to take or pay",
    "Roll random to warp",
    "Roll to get all suits",
    "Scramble",
    "Sell shop back",
    "Sell stocks",
    "Shop prices halve",
    "Shops expand in random district",
    "Stock rise",
    "Stocks dividend",
    "Sudden promotion",
    "Take gold from all",
    "Winner pays you",
    "Your shops drop",
    "Your shops grow",
    "Zoom to any",
    "Zoom to bank",
    "Zoom to non-venture"
];

export function check_cards() {
    console.log("Checking cards")
    const difficulty = document.getElementById("difficulty");
    for (let i = 0; i < 128; i++) {
        const card = document.getElementById("card" + i);
        if (!card) continue;
        card.style.display = "block";
        const cardEasy = card.getAttribute("data-easy") === "true";
        const cardStandard = card.getAttribute("data-standard") === "true";
        const cardSentiment = parseInt(card.getAttribute("data-effect-sentiment"));
        const cardPower = parseInt(card.getAttribute("data-effect-group-power"));
        const cardGroup = card.getAttribute("data-effect-group");
        // Check difficulty
        if (difficulty.value === "both" && (!cardEasy || !cardStandard)) {
            card.style.display = "none";
            continue;
        } else if (difficulty.value === "easy" && !cardEasy) {
            card.style.display = "none";
            continue;
        } else if (difficulty.value === "standard" && !cardStandard) {
            card.style.display = "none";
            continue;
        } else if (difficulty.value === "neither" && (cardEasy || cardStandard)) {
            card.style.display = "none";
            continue;
        }
        // Check sentiment
        if (!document.getElementById("effectSentimentPositive").checked && cardSentiment === 1) {
            card.style.display = "none";
            continue;
        } else if (!document.getElementById("effectSentimentNeutral").checked && cardSentiment === 0) {
            card.style.display = "none";
            continue;
        } else if (!document.getElementById("effectSentimentNegative").checked && cardSentiment === -1) {
            card.style.display = "none";
            continue;
        }
        // Check power
        let powerMin = parseInt(document.getElementById("effectGroupPowerMin").value);
        let powerMax = parseInt(document.getElementById("effectGroupPowerMax").value);
        if (powerMax < powerMin) {
            powerMax = powerMin;
            document.getElementById("effectGroupPowerMax").value = powerMin;
        }
        if (cardPower < powerMin || cardPower > powerMax) {
            card.style.display = "none";
            continue;
        }
        // Check effect group
        // TODO: Fix this
        for (let j = 0; j < effectGroups.length; j++) {
            if (cardGroup === effectGroups[j] && !document.getElementById(effectGroups[j]).checked) {
                card.style.display = "none";
                continue;
            }
        }
    }
}

export function hide_all_effect_groups() {
    console.log("Hiding all effect groups")
    for (let i = 0; i < effectGroups.length; i++) {
        document.getElementById(effectGroups[i]).checked = false;
    }
    check_cards();
}

export function show_all_effect_groups() {
    console.log("Showing all effect groups")
    for (let i = 0; i < effectGroups.length; i++) {
        document.getElementById(effectGroups[i]).checked = true;
    }
    check_cards();
}
