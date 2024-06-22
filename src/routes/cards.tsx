import { RouteSectionProps } from '@solidjs/router';
import { For, Show, createResource } from 'solid-js';
import { getVentureCards, getVentureCardEffects } from '~/lib/loadyamlfiles';
import slug from 'slug';
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
} from '~/lib/cards';

function sentiment_to_div_class(sentiment: number) {
  let classes = "card text-center";
  if (sentiment === 1) {
    classes += " bg-success";
  } else if (sentiment === 0) {
    classes += " bg-secondary";
  } else if (sentiment === -1) {
    classes += " bg-danger";
  }
  return classes;
}

export default function (props: RouteSectionProps) {
  const [cards] = createResource(getVentureCards);
  const [effects] = createResource(getVentureCardEffects);

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
            <p>The game difficulty cards are in by default. If you are using defaults, you don't need to include <code>ventureCards</code> in your board's YAML.</p>
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
            <p>Card grades are assigned by the Fortune Street modding community based on their power among cards with similar effects.</p>
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
            <For each={effects()}>
            {(effect) => (
            <Show when={effect !== null}>
            <div class="form-check">
              {/* TODO: Fix these checkboxes not firing their onChange outputs */}
              <input type="checkbox" class="form-check-input" checked id={slug(effect!)} onChange={() => check_cards()}/>
              <label class="form-check-label" for={slug(effect!)}>{effect}</label>
            </div>
            </Show>
            )}
            </For>
          </div>
        </div>
        <div class="col-9">
          <div class="row row-cols-2 g-2">
            <For each={cards()}>
            {(card, index) => (
            <div class="col" style="display: block;" id={"card" + (index() + 1).toString()} data-easy={card.defaultEasy} data-standard={card.defaultStandard} data-effect={slug(card.effect)} data-grade={card.grade} data-sentiment={card.sentiment}>
              <div class={sentiment_to_div_class(card.sentiment)} style="height: 100%;">
                <div class="row row-cols-2 g-2">
                  <div class="col-4">
                    <header><p>Card No. {index() + 1}</p></header>
                    <figure><img src={"/images/card_" + (index() + 1).toString() + ".webp"} alt={"Venture Card " + (index() + 1).toString()} style="max-width: 100%; height: auto;"/></figure>
                    <footer><p><strong>
                      <Show when={card.grade === 0}>D</Show>
                      <Show when={card.grade === 1}>C</Show>
                      <Show when={card.grade === 2}>B</Show>
                      <Show when={card.grade === 3}>A</Show>
                      <Show when={card.grade === 4}>S</Show>
                    </strong></p></footer>
                  </div>
                  <div class="col-8">
                    <input type="checkbox" id={"card" + (index() + 1).toString() + "selected"} checked={card.defaultStandard} onChange={() => check_selected_cards()}/>
                    <p><strong>{card.description}</strong></p>
                    <Show when={card.descriptionExtra !== null}>
                    <p>{card.descriptionExtra}</p>
                    </Show>
                    <p>
                      <Show when={card.defaultEasy}>
                      Easy
                      </Show>
                      <Show when={card.defaultEasy && card.defaultStandard}>
                      /
                      </Show>
                      <Show when={card.defaultStandard}>
                      Standard
                      </Show>
                    </p>
                    <Show when={card.effect !== null}>
                    <p>{card.effect}</p>
                    </Show>
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
