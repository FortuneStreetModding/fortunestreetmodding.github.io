//import createMonacoYamlEditor from '~/lib/monaco';
import { RouteSectionProps } from '@solidjs/router';

import mapDescriptorSchema from '../../schema/mapdescriptor.json';
import { createSignal, onCleanup, onMount } from 'solid-js';

export default function (props: RouteSectionProps) {
  const [editor, setEditor] = createSignal<any>();
  
  
  onMount(() => {
    // @ts-ignore
    const yamlModelUri = monaco.Uri.parse('http://fortunestreetmodding.github.io/schema/mapdescriptor.json#');
    const diagnosticsOptions = {
      enableSchemaRequest: true,
      hover: true,
      completion: true,
      validate: true,
      format: true,
      schemas: [
        {
          uri: 'http://fortunestreetmodding.github.io/schema/mapdescriptor.json',
          fileMatch: ['*'],
          schema: mapDescriptorSchema,
        }
      ],
    };
    
    // YAML specific API
    // @ts-ignore
    monacoYaml.setDiagnosticsOptions(diagnosticsOptions);
    
    const yaml = 'p1: \np2: \n';

    // @ts-ignore
    let model = monaco.editor.getModel(yamlModelUri);
    if (!model) {
      // @ts-ignore
      model = monaco.editor.createModel(yaml, 'yaml', yamlModelUri);
    }

    // @ts-ignore
    const editor = monaco.editor.create(document.getElementById('yaml-editor'), {
      automaticLayout: true,
      // @ts-ignore
      model: model,
      theme: "vs-dark",
      autoIndent: true,
      tabSize: 2
    });
    setEditor(editor);
  });

  onCleanup(() => {
    editor()?.dispose();
  });

  return (
    <>
      <select id="model">
        <option value="file:///.prettierrc.yaml">.prettierc.yaml</option>
        <option value="file:///person.yaml">person</option>
      </select>
      <div style="display: flex;">
        <div id="yaml-editor" style="width: 95vw; height: 95vh;"></div>
      </div>
      <script src="monaco-editor.js"></script>
    </>
  );
}
