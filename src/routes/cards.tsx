import { RouteSectionProps } from '@solidjs/router';
import { For } from 'solid-js';
import { getVentureCardsSync } from '~/lib/loadyamlfiles';

export default function (props: RouteSectionProps) {
  const cards = getVentureCardsSync();
  console.log(cards[0]);

  return (
    <div class="w3-card-4 w3-center w3-display-topmiddle w3-margin-bottom-16">
      <h1 class="w3-container w3-blue w3-padding-16">Venture Cards</h1>
      <div class="container text-center">
        <div class="row row-cols-2 g-3">
          <For each={cards}> {(card, index) => (
          <div class="col">
            <p><strong>{index}:</strong> {JSON.stringify(card)}</p>
          </div>
          )} </For>
        </div>
      </div>
    </div>
  );
}
