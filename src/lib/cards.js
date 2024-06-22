// TODO: Reassign effects and grades
const effects = [
    "Buy Suit Yourself",  // 2
    "Buy stocks",  // 3
    "Buy shop",  // 6 - Grades finalised
    "Cameo adventure",  // 3 - Grades finalised
    "Choose way to move",  // 2 - Grades finalised
    "Expand one shop",  // 4
    "Get commission",  // 2 - Grades finalised
    "Get gold from 1st",  // 4
    "Get gold from all",  // 3
    "Get gold x level",  // 3
    "Get gold x shops",  // 4
    "Get stocks",  // 3
    "Get suits",  // 9 - Consider re-assigning amongst "Buy Suit Yourself"
    "Give gold to all",  // 2
    "Give gold to last",  // 3
    "Go to square",  // 7 - Grades finalised
    "Income tax",  // 3
    "Invest capital",  // 4 - Grades finalised
    "Move forward",  // 3
    "Other players movement",  // 3
    "Play arcade games",  // 3 - Grades finalised
    "Shop prices change",  // 3
    "Random district shops drop",  // 2
    "Random stock price change",  // 5 - Grades finalised
    "Roll after shop price change",  // 4
    "Roll and expand shops",  // 1
    "Roll and get from bank",  // 2
    "Roll and move forward",  // 4
    "Roll random to close shops",  // 1
    "Roll random to expand shops",  // 2
    "Roll random to take or pay",  // 1
    "Roll random to warp",  // 3
    "Salary bonus",  // 2 - Grades finalised
    "Scramble",  // 2
    "Sell shop back",  // 7 - Grades finalised
    "Sell stocks",  // 2
    "Shops expand in random district",  // 4
    "Stock rise",  // 1
    "Stocks dividend",  // 2
    "Your shops change value",  // 4
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
            // Add spaces in front of i to make it easier to read
            let i_string = i.toString();
            if (i < 100) {
                i_string = " " + i_string;
                if (i < 10) {
                    i_string = " " + i_string;
                }
            }
            yaml_string = yaml_string + "\n  - " + yaml_selected + "  # " + i_string;
        }
        document.getElementById("generatedYaml").textContent = yaml_string;
        document.getElementById("yaml").style.display = "block";
        document.getElementById("yaml").scrollIntoView({behavior: "smooth"});
    }
}

export function copy_yaml_to_clipboard() {
    console.log("Copying YAML to clipboard")
    navigator.clipboard.writeText(document.getElementById("generatedYaml").textContent);
    document.getElementById("copyYaml").innerText = "Copied!";
}
