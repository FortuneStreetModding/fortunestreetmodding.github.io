import { RouteSectionProps, redirect } from '@solidjs/router';

export default function (props: RouteSectionProps) {
  redirect(`/boards/${props.data}`);
}
