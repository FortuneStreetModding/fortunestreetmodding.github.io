import { RouteSectionProps } from "@solidjs/router";
import { For, Show } from "solid-js";
import { getVentureCardsSync, getVentureCardEffectsSync } from "~/lib/loadyamlfiles";
import {
  check_cards,
  hide_all_effects,
  show_all_effects,
  reset_filters,
  check_selected_cards,
  deselect_all_cards,
  select_visible_cards,
  generate_yaml,
  copy_yaml_to_clipboard
} from "~/lib/cards";

export default function (props: RouteSectionProps) {
  const cards = getVentureCardsSync();
  const effects = getVentureCardEffectsSync();

  return (
  <div class="w3-card-4 w3-center w3-display-topmiddle w3-margin-bottom-16">
    <h1 class="w3-container w3-blue w3-padding-16">Venture Cards</h1>
    <div class="container">
      <div class="row row-cols-2 g-2">
        <div class="col-3">
          <div class="mb-3">
            <button class="btn btn-primary" onClick={() => deselect_all_cards()}>Deselect all</button> <button class="btn btn-primary" onClick={() => select_visible_cards()}>Select visible</button> <button class="btn btn-primary" onClick={() => reset_filters()}>Reset filters</button>
          </div>
        </div>
        <div class="col-9">
          <div class="mb-3">
            <label class="form-label" id="cardsSelected">64 cards selected</label> <button class="btn btn-primary" id="generateYaml" onClick={() => generate_yaml()}>Generate YAML (requires 64)</button>
          </div>
        </div>
      </div>
      <div class="row row-cols-2 g-2">
        <div class="col-3">
          <h2>Gamemode</h2>
          <div class="mb-3">
            <p>The game difficulty venture cards are found in by default.</p>
            <select class="form-select" id="difficulty" onChange={() => check_cards()}>
              <option value="any">Any</option>
              <option value="both">Both</option>
              <option value="easy">Easy</option>
              <option value="standard">Standard</option>
              <option value="neither">Neither</option>
            </select>
          </div>
          <h2>Grade</h2>
          <div class="mb-3">
            <input type="checkbox" class="btn-check-outlined" id="grade0" autocomplete="off" checked onChange={() => check_cards()}/>
            <label class="btn btn-primary" for="grade0">D</label>
            <input type="checkbox" class="btn-check-outlined" id="grade1" autocomplete="off" checked onChange={() => check_cards()}/>
            <label class="btn btn-primary" for="grade1">C</label>
            <input type="checkbox" class="btn-check-outlined" id="grade2" autocomplete="off" checked onChange={() => check_cards()}/>
            <label class="btn btn-primary" for="grade2">B</label>
            <input type="checkbox" class="btn-check-outlined" id="grade3" autocomplete="off" checked onChange={() => check_cards()}/>
            <label class="btn btn-primary" for="grade3">A</label>
            <input type="checkbox" class="btn-check-outlined" id="grade4" autocomplete="off" checked onChange={() => check_cards()}/>
            <label class="btn btn-primary" for="grade4">S</label>
          </div>
          <h2>Sentiment</h2>
          <div class="mb-3">
            <div class="form-check">
              <input type="checkbox" class="form-check-input" checked id="sentimentPositive" onChange={() => check_cards()}/>
              <label class="form-check-label" for="sentimentPositive">Positive</label>
            </div>
            <div class="form-check">
              <input type="checkbox" class="form-check-input" checked id="sentimentNeutral" onChange={() => check_cards()}/>
              <label class="form-check-label" for="sentimentNeutral">Neutral</label>
            </div>
            <div class="form-check">
              <input type="checkbox" class="form-check-input" checked id="sentimentNegative" onChange={() => check_cards()}/>
              <label class="form-check-label" for="sentimentNegative">Negative</label>
            </div>
          </div>
          <h2>Effects</h2>
          <div class="mb-3">
            <button type="button" class="btn btn-primary" id="effectsNone" onClick={() => hide_all_effects()}>None</button> <button type="button" class="btn btn-primary" id="effectsAll" onClick={() => show_all_effects()}>All</button>
          </div>
          <div class="mb-3">
            <For each={effects}>
            {(effect) => (
            <Show when={effect !== null}>
            <div class="form-check">
              {/* TODO: Fix these checkboxes not firing their onChange outputs */}
              <input type="checkbox" class="form-check-input" checked id={effect} onChange={() => check_cards()}/>
              <label class="form-check-label" for={effect}>{effect}</label>
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
            <div class="col" style="display: block;" id={"card" + (index() + 1).toString()} data-easy={card.defaultEasy} data-standard={card.defaultStandard} data-effect={card.effect} data-grade={card.grade} data-sentiment={card.sentiment}>
              <div class="card text-center">
                <div class="row row-cols-2 g-2">
                  <div class="col-4">
                    <p><strong>{index() + 1}</strong></p>
                  </div>
                  <div class="col-8">
                    <p><strong>{card.description}</strong></p>
                    <Show when={card.descriptionExtra !== null}>
                    <p>{card.descriptionExtra}</p>
                    </Show>
                    <Show when={card.defaultEasy}>
                    <p>Easy</p>
                    </Show>
                    <Show when={card.defaultStandard}>
                    <p>Standard</p>
                    </Show>
                    <Show when={card.effect !== null}>
                    <p>{card.effect} ({card.grade})</p>
                    </Show>
                    <input type="checkbox" id={"card" + (index() + 1).toString() + "selected"} checked={card.defaultStandard} onChange={() => check_selected_cards()}/>
                  </div>
                </div>
              </div>
            </div>
            )}
          </For>
          </div>
        </div>
      </div>
      <div class="row" style="display: none;" id="yaml">
        <div class="col">
          <div class="card">
            <h2>Generated YAML</h2>
            <p>Click the button below to copy the generated YAML to your clipboard, and paste it into your custom Fortune Street board's YAML file. Make sure that there is only one <code>ventureCards</code> property in your YAML.</p>
            <code><textarea class="form-control" id="generatedYaml" rows="10" readOnly></textarea></code>
            <button class="btn btn-primary" id="copyYaml" onClick={() => copy_yaml_to_clipboard()}>Copy to clipboard</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  );
}
