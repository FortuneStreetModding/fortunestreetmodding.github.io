import { RouteSectionProps } from '@solidjs/router';
import { For, Match, Show, Switch } from 'solid-js';
import { getBoardsSync } from '~/lib/loadyamlfiles';
import "./boards.css"

export default function (props: RouteSectionProps) {
  const boards = getBoardsSync();
  const boardsList = Object.values(boards);

  return (
    <div class="album">
      <div class="container">
        <div class="row">
          <For each={/*@once*/ boardsList}>
            {(board, boardIndex) => (
              <>
              <div class="col mb-4 mapCard">
                <div class="card h-100">
                  <div class="relative-container">
                    <For each={board.frbFiles}>
                      {(item, index) => (
                        <div>
                          <input class={`btn-check state-${index()}`} type="radio" name={`state-${board.slug}`} id={`state-${index()}-${board.slug}`} autocomplete="off" checked={index()==0}/>
                          <label class={`btn btn-primary btn-state-tiny state-${index()}`} for={`state-${index()}-${board.slug}`}>{index()+1}</label>
                        </div>
                      )}
                    </For>
                    <a class="map-state" href={`/boards/${board.slug}`}>
                      <For each={board.frbFiles}>
                        {(item, index) => (
                          <img class={`card-img-top mapCard-image-board state-${index()}`} src={board.imageUrls[index()]} loading="lazy"></img>
                        )}
                      </For>
                    </a>
                    <img class="card-img-top mapCard-image-background" src={board.imageUrls[0]} loading="lazy"></img>
                    <div class="card-body">
                      Name and Stuff
                    </div>
                    <div class="card-footer text-muted"></div>
                    <div class="card-footer text-muted"></div>
                  </div>
                </div>
              </div>
              <Show when={boardIndex() > 0 && boardIndex() % 3 == 2}>
                <div class="w-100"></div>
              </Show>
              </>
            )}
          </For>
          <Switch>
            <Match when={boardsList.length > 0 && boardsList.length % 3 == 0}>
            <div class="w-100"></div>
            </Match>
            <Match when={boardsList.length > 0 && boardsList.length % 3 == 1}>
            <div class="col mapCard"></div>
            <div class="col mapCard"></div>
            </Match>
            <Match when={boardsList.length > 0 && boardsList.length % 3 == 2}>
            <div class="col mapCard"></div>
            </Match>
          </Switch>
        </div>
      </div>
    </div>
  );
}
