import { useLocation } from "@solidjs/router";

export default function Component() {
  const location = useLocation();

  return (
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="/"><img src="/favicon.ico" alt="Fortune Street Modding" width="24" height="24" class="d-inline-block align-text-top" /> Fortune Street Modding</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link active" classList={{ active: location.pathname === "/" }} href="/">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" classList={{ active: location.pathname === "/boards" }} href="/boards">Boards</a>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Tools
              </a>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" classList={{ active: location.pathname === "/calculator" }} href="/calculator">Address Calculator</a></li>
                <li><a class="dropdown-item" classList={{ active: location.pathname === "/simulator" }} href="/simulator">District Simulator</a></li>
                <li><a class="dropdown-item" classList={{ active: location.pathname === "/cards" }} href="/simulator">Venture Cards</a></li>
              </ul>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="https://discord.gg/DE9Hn7T">Discord</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="https://github.com/FortuneStreetModding">Github</a>
            </li>
          </ul>
          <form class="d-flex" role="search">
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search"/>
            <button class="btn btn-outline-success" type="submit">Search Maps</button>
          </form>
        </div>
      </div>
    </nav>
  );
}
