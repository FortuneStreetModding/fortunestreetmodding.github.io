const effects = [
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
    for (let i = 1; i <= 128; i++) {
        const card = document.getElementById("card" + i.toString());
        if (!card) continue;
        card.style.display = "block";
        const cardEasy = card.getAttribute("data-easy") === "true";
        const cardStandard = card.getAttribute("data-standard") === "true";
        const cardSentiment = parseInt(card.getAttribute("data-sentiment"));
        const cardGrade = parseInt(card.getAttribute("data-grade"));
        const cardEffect = card.getAttribute("data-effect");
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
        if (!document.getElementById("sentimentPositive").checked && cardSentiment === 1) {
            card.style.display = "none";
            continue;
        } else if (!document.getElementById("sentimentNeutral").checked && cardSentiment === 0) {
            card.style.display = "none";
            continue;
        } else if (!document.getElementById("sentimentNegative").checked && cardSentiment === -1) {
            card.style.display = "none";
            continue;
        }
        // Check grade
        for (let j = 0; j <= 4; j++) {
            if (!document.getElementById("grade" + j.toString()).checked && cardGrade === j) {
                card.style.display = "none";
                break;
            }
        }
        // Check effect
        for (let j = 0; j < effects.length; j++) {
            if (cardEffect === effects[j] && !document.getElementById(effects[j]).checked) {
                card.style.display = "none";
                continue;
            }
        }
    }
}

export function hide_all_effects() {
    console.log("Hiding all effects")
    for (let i = 0; i < effects.length; i++) {
        document.getElementById(effects[i]).checked = false;
    }
    check_cards();
}

export function show_all_effects() {
    console.log("Showing all effects")
    for (let i = 0; i < effects.length; i++) {
        document.getElementById(effects[i]).checked = true;
    }
    check_cards();
}

export function reset_filters() {
    console.log("Resetting filters")
    document.getElementById("difficulty").value = "any";
    for (let j = 0; j <= 4; j++) {
        document.getElementById("grade" + j.toString()).checked = true;
    }
    document.getElementById("sentimentPositive").checked = true;
    document.getElementById("sentimentNeutral").checked = true;
    document.getElementById("sentimentNegative").checked = true;
    show_all_effects();
}

export function check_selected_cards() {
    console.log("Checking selected cards")
    document.getElementById("yaml").style.display = "none";
    let chosenCards = 0;
    for (let i = 1; i <= 128; i++) {
        if (document.getElementById("card" + i.toString() + "selected").checked) {
            chosenCards++;
        }
    }
    document.getElementById("cardsSelected").textContent = chosenCards.toString() + " cards selected";
    if (chosenCards === 64) {
        console.log("Correct number of cards chosen");
        // Enable button with ID generateYaml
        document.getElementById("generateYaml").disabled = false;
    } else {
        // Disable button with ID generateYaml
        document.getElementById("generateYaml").disabled = true;
    }
    return chosenCards === 64;
}

export function deselect_all_cards() {
    console.log("Deselecting all cards")
    for (let i = 1; i <= 128; i++) {
        document.getElementById("card" + i.toString() + "selected").checked = false;
    }
    check_selected_cards();
}

export function select_visible_cards() {
    console.log("Selecting visible cards")
    for (let i = 1; i <= 128; i++) {
        console.log(i, document.getElementById("card" + i.toString()).style.display);
        if (document.getElementById("card" + i.toString()).style.display === "block") {
            document.getElementById("card" + i.toString() + "selected").checked = true;
        }
    }
    check_selected_cards();
}

export function generate_yaml() {
    if (check_selected_cards()) {
        console.log("Generating YAML")
        let yaml_string = "ventureCards:";
        for (let i = 1; i <= 128; i++) {
            let yaml_selected = "0";
            if (document.getElementById("card" + i.toString() + "selected").checked) {
                yaml_selected = "1";
            }
            yaml_string = yaml_string + "\n  - " + yaml_selected + "  # " + i;
        }
        document.getElementById("generatedYaml").textContent = yaml_string;
        document.getElementById("yaml").style.display = "block";
    }
}

export function copy_yaml_to_clipboard() {
    console.log("Copying YAML to clipboard")
    navigator.clipboard.writeText(document.getElementById("generatedYaml").textContent);
    document.getElementById("copyYaml").innerText = "Copied!";
}
