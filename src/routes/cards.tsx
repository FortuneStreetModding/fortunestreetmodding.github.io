import { RouteSectionProps } from "@solidjs/router";
import { For, Show } from "solid-js";
import { getVentureCardGroupsSync, getVentureCardsSync } from "~/lib/loadyamlfiles";
import { check_cards, hide_all_effect_groups, show_all_effect_groups } from "~/lib/cards";

export default function (props: RouteSectionProps) {
  const cards = getVentureCardsSync();
  const effectGroups = getVentureCardGroupsSync();

  return (
  <div class="w3-card-4 w3-center w3-display-topmiddle w3-margin-bottom-16">
    <h1 class="w3-container w3-blue w3-padding-16">Venture Cards</h1>
    <div class="container">
      <div class="row row-cols-2 g-2">
        <div class="col-3">
          <h2>Default Difficulty</h2>
           <div class="mb-3">
              <select class="form-select" id="difficulty" onChange={() => check_cards()}>
                <option value="any">Any</option>
                <option value="both">Both</option>
                <option value="easy">Easy</option>
                <option value="standard">Standard</option>
                <option value="neither">Neither</option>
              </select>
           </div>
          <h2>Sentiment</h2>
          <div class="mb-3">
            <div class="form-check">
              <input type="checkbox" class="form-check-input" checked id="effectSentimentPositive" onChange={() => check_cards()}/>
              <label class="form-check-label" for="effectSentimentPositive">Positive</label>
            </div>
            <div class="form-check">
              <input type="checkbox" class="form-check-input" checked id="effectSentimentNeutral" onChange={() => check_cards()}/>
              <label class="form-check-label" for="effectSentimentNeutral">Neutral</label>
            </div>
            <div class="form-check">
              <input type="checkbox" class="form-check-input" checked id="effectSentimentNegative" onChange={() => check_cards()}/>
              <label class="form-check-label" for="effectSentimentNegative">Negative</label>
            </div>
          </div>
          <h2>Power</h2>
          <div class="mb-3">
            <label for="effectGroupPowerMin" class="form-label">Minimum</label>
            <input type="range" class="form-range" min="0" max="3" value="0" id="effectGroupPowerMin" onChange={() => check_cards()}/>
            <label for="effectGroupPowerMax" class="form-label">Maximum</label>
            <input type="range" class="form-range" min="0" max="3" value="3" id="effectGroupPowerMax" onChange={() => check_cards()}/>
          </div>
          <h2>Groups</h2>
          <div class="mb-3">
            <button type="button" class="btn btn-primary" id="effectGroupNone" onClick={() => hide_all_effect_groups()}>None</button> <button type="button" class="btn btn-primary" id="effectGroupAll" onClick={() => show_all_effect_groups()}>All</button>
          </div>
          <div class="mb-3">
            <For each={effectGroups}>
            {(effectGroup) => (
            <Show when={effectGroup !== null}>
            <div class="form-check">
              <input type="checkbox" class="form-check-input" checked id={effectGroup} onChange={() => check_cards()}/>
              <label class="form-check-label" for={effectGroup}>{effectGroup}</label>
            </div>
            </Show>
            )}
            </For>
          </div>
        </div>
        <div class="col-9">
          <div class="row row-cols-2 g-2">
            <For each={cards}>
            {(card, index) => (
            <div class="col" id={"card" + index()} data-easy={card.defaultEasy} data-standard={card.defaultStandard} data-effect-group={card.effectGroup} data-effect-group-power={card.effectGroupPower} data-effect-sentiment={card.effectSentiment}>
              <div class="card text-center">
                <div class="row row-cols-2 g-2">
                  <div class="col-4">
                    <p><strong>{index() + 1}</strong></p>
                  </div>
                  <div class="col-8">
                    <p><strong>{card.description}</strong></p>
                    <Show when={card.defaultEasy}>
                    <p>Easy</p>
                    </Show>
                    <Show when={card.defaultStandard}>
                    <p>Standard</p>
                    </Show>
                    <Show when={card.effectGroup !== null}>
                    <p>{card.effectGroup} ({card.effectGroupPower})</p>
                    </Show>
                    <input type="checkbox"/>
                  </div>
                </div>
              </div>
            </div>
            )}
          </For>
          </div>
        </div>
      </div>
    </div>
  </div>
  );
}
