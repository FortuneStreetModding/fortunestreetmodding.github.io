import { RouteSectionProps, useParams } from '@solidjs/router';

export default function (props: RouteSectionProps) {
  const params = useParams();

  return (
    <div class="album">
      <div class="container">
        <div class="row">
          <div>User {/* @once */params.name}</div>
        </div>
      </div>
    </div>
  );
}
