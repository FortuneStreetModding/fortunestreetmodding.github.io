export function check_cards() {
    const difficulty = document.getElementById("difficulty");
    for (let i = 1; i <= 128; i++) {
        const card = document.getElementById("card" + i.toString());
        const smallCard = document.getElementById("ventureCard-" + i.toString());
        if (!card) continue;
        card.style.display = "block";
        smallCard.style.visibility = "visible";
        const cardEasy = card.hasAttribute("data-easy");
        const cardStandard = card.hasAttribute("data-standard");
        const cardSentiment = parseInt(card.getAttribute("data-sentiment"));
        const cardGrade = parseInt(card.getAttribute("data-grade"));
        const cardType = card.getAttribute("data-type");
        const cardEffect = card.getAttribute("data-effect");
        // Check difficulty
        if (difficulty.value === "both" && (!cardEasy || !cardStandard)) {
            card.style.display = "none";
            smallCard.style.visibility = "hidden";
            continue;
        } else if (difficulty.value === "easy" && !cardEasy) {
            card.style.display = "none";
            smallCard.style.visibility = "hidden";
            continue;
        } else if (difficulty.value === "standard" && !cardStandard) {
            card.style.display = "none";
            smallCard.style.visibility = "hidden";
            continue;
        } else if (difficulty.value === "neither" && (cardEasy || cardStandard)) {
            card.style.display = "none";
            smallCard.style.visibility = "hidden";
            continue;
        }
        // Check sentiment
        if (!document.getElementById("sentimentPositive").checked && cardSentiment === 1) {
            card.style.display = "none";
            smallCard.style.visibility = "hidden";
            continue;
        } else if (!document.getElementById("sentimentNeutral").checked && cardSentiment === 0) {
            card.style.display = "none";
            smallCard.style.visibility = "hidden";
            continue;
        } else if (!document.getElementById("sentimentNegative").checked && cardSentiment === -1) {
            card.style.display = "none";
            smallCard.style.visibility = "hidden";
            continue;
        }
        // Check grade
        for (let j = 0; j <= 4; j++) {
            if (!document.getElementById("grade" + j.toString()).checked && cardGrade === j) {
                card.style.display = "none";
                smallCard.style.visibility = "hidden";
                break;
            }
        }
        // Check type
        if (document.getElementById("types").value !== "any" && cardType !== document.getElementById("types").value) {
            card.style.display = "none";
            smallCard.style.visibility = "hidden";
            continue;
        }
        // Check effect
        if (document.getElementById("effects").value !== "any" && cardEffect !== document.getElementById("effects").value) {
            card.style.display = "none";
            smallCard.style.visibility = "hidden";
            continue;
        }
    }
}

export function reset_filters() {
    document.getElementById("difficulty").value = "any";
    for (let j = 0; j <= 4; j++) {
        document.getElementById("grade" + j.toString()).checked = true;
    }
    document.getElementById("sentimentPositive").checked = true;
    document.getElementById("sentimentNeutral").checked = true;
    document.getElementById("sentimentNegative").checked = true;
    document.getElementById("types").value = "any";
    document.getElementById("effects").value = "any";
    check_cards();
}

export function reset_selected_cards() {
    for (let i = 1; i <= 128; i++) {
        const isStandard = document.getElementById("card" + i.toString()).hasAttribute("data-standard")
        document.getElementById("card" + i.toString() + "selected").checked = isStandard;
        document.getElementById(`ventureCardInput-${i}`).checked = isStandard;
    }
    check_selected_cards();
}

export function display_bigCards() {
    for (let i = 1; i <= 128; i++) {
        const bigCard = document.getElementById(`card${i}selected`)
        const smallCard = document.getElementById(`ventureCardInput-${i}`)
        bigCard.checked = smallCard.checked
    }
    document.getElementById('ventureCardsSmall').style.display = "none"
    document.getElementById('ventureCardsBig').style.display = ""
}

export function display_smallCards() {
    for (let i = 1; i <= 128; i++) {
        const bigCard = document.getElementById(`card${i}selected`)
        const smallCard = document.getElementById(`ventureCardInput-${i}`)
        smallCard.checked = bigCard.checked
    }
    document.getElementById('ventureCardsSmall').style.display = ""
    document.getElementById('ventureCardsBig').style.display = "none"
}

export function check_selected_cards() {
    document.getElementById("yaml").style.display = "none";
    let chosenCards = 0;
    const bigCards = document.getElementById("cardsDisplayBig").checked;
    if (bigCards) {
        for (let i = 1; i <= 128; i++) {
            if (document.getElementById("card" + i.toString() + "selected").checked) {
                chosenCards++;
                document.getElementById("card" + i.toString()).style.opacity = 1;
            } else {
                document.getElementById("card" + i.toString()).style.opacity = 0.625;
            }
        }
    } else {
        for (let i = 1; i <= 128; i++) {
            if (document.getElementById(`ventureCardInput-${i}`).checked) {
                chosenCards++;
            }
        }
    }
    document.getElementById("cardsSelected").textContent = chosenCards.toString() + " cards selected";
    if (chosenCards === 64) {
        document.getElementById("generateYaml").disabled = false;
    } else {
        document.getElementById("generateYaml").disabled = true;
    }
    return chosenCards === 64;
}

export function select_all_cards(select = true) {
    for (let i = 1; i <= 128; i++) {
        document.getElementById("card" + i.toString() + "selected").checked = select;
        document.getElementById(`ventureCardInput-${i}`).checked = select;
    }
    check_selected_cards();
}

export function select_visible_cards(select = true) {
    for (let i = 1; i <= 128; i++) {
        if (document.getElementById("card" + i.toString()).style.display === "block") {
            document.getElementById("card" + i.toString() + "selected").checked = select;
        }
        if (document.getElementById(`ventureCard-${i}`).style.visibility !== "hidden") {
            document.getElementById(`ventureCardInput-${i}`).checked = select;
        }
    }
    check_selected_cards();
}

export function generate_yaml() {
    if (check_selected_cards()) {
        let yaml_str = "ventureCards:";
        for (let i = 1; i <= 128; i++) {
            const card = document.getElementById("card" + i.toString());
            const description = card.getAttribute("data-description")
            let yaml_selected = "0";
            if (document.getElementById("card" + i.toString() + "selected").checked) {
                yaml_selected = "1";
            }
            // Add spaces in front of i to make it easier to read
            let i_str = i.toString();
            if (i < 100) {
                i_str = " " + i_str;
                if (i < 10) {
                    i_str = " " + i_str;
                }
            }
            yaml_str = yaml_str + "\n  - " + yaml_selected + "  # " + i_str + " " + description;
        }
        document.getElementById("generatedYaml").textContent = yaml_str;
        document.getElementById("yaml").style.display = "block";
        document.getElementById("yaml").scrollIntoView({behavior: "smooth"});
    }
}

export function copy_yaml_to_clipboard() {
    navigator.clipboard.writeText(document.getElementById("generatedYaml").textContent);
    document.getElementById("copyYaml").innerText = "Copied!";
}
