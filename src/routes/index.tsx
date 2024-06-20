import { RouteSectionProps } from '@solidjs/router';

export default function (props: RouteSectionProps) {
  return (
    <section class="jumbotron">
      <div class="container">
        <div class="card mx-auto" style="max-width:50rem">
          <div class="card-header">Custom Street World Tour</div>
          <img src="/images/CustomStreetWorldTourTitle.webp" class="card-img-top" />
          <div class="card-body">
            <p class="card-text">A custom map pack containing over 135 new boards by our community.</p>
            <p class="card-text">
              <a href="https://github.com/FortuneStreetModding/CustomStreetWorldTour#readme" class="btn btn-primary my-2" download="setup.bat">
                Download
              </a>
            </p>
            <p></p>
          </div>
        </div>
        <div class="card mx-auto" style="max-width:50rem">
          <div class="card-header">HQ Texture Pack</div>
          <img src="/images/FortuneStreetHQ.webp" class="card-img-top" />
          <div class="card-body">
            <p class="card-text">
              A WIP texture pack containing many HD textures for Boom Street and Fortune Street. Compatible with the base game and Custom Street World Tour.
            </p>
            <p class="card-text">
              <a
                href="https://github.com/FortuneStreetModding/fortunestreetmodding.github.io/blob/main/Fortune%20Street%20HD%20Textures%20Readme.md"
                class="btn btn-primary my-2"
                download="setup.bat"
              >
                Download
              </a>
            </p>
            <p></p>
          </div>
        </div>
        <div class="card mx-auto" style="max-width:50rem">
          <div class="card-header">Gecko Codes</div>
          <div class="card-body">
            <p class="card-text">
              A collection of Gecko Codes sourced from around the internet and our community. Includes a 60fps code and a code to speed up the game for much
              quicker matches.
            </p>
            <p class="card-text">
              <a href="https://github.com/FortuneStreetModding/Gecko-Codes" class="btn btn-primary my-2" download="setup.bat">
                Download
              </a>
            </p>
            <p></p>
          </div>
        </div>
      </div>
    </section>
  );
}
