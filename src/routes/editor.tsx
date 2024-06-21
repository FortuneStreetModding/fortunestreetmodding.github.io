//import createMonacoYamlEditor from '~/lib/monaco';
import { RouteSectionProps } from '@solidjs/router';

import mapDescriptorSchema from '../../schema/mapdescriptor.json';
import { createSignal, onCleanup, onMount } from 'solid-js';
import "./editor.css"
import { getYamlStr } from '~/lib/loadyamlfiles';

export default function (props: RouteSectionProps) {
  const [editor, setEditor] = createSignal<any>();
  const [presetEl, setPresetEl] = createSignal<HTMLSelectElement>();
  
  // const templateMininmal = getYamlStr("./Board_Template_minimal_version.yaml");
  // const templateDefaultLoaded = getYamlStr("./Board_Template_minimal_version.yaml");
  // const templateDefault = getYamlStr("./Board_Template_minimal_version.yaml");
  // const templateFull ='singleQuote: true\nproseWrap: always\nsemi: yes\n';
  // const templateMininmal = getYamlStr("./_maps/AcademyCity/academycity.yaml");
  // const templateDefault = getYamlStr("./_maps/AcademyCity/academycity.yaml");
  // const templateFull = getYamlStr("./_maps/AcademyCity/academycity.yaml");
  const templateMininmal = getYamlStr("./Board_Template_minimal_version.yaml");
  const templateDefault = getYamlStr("./Board_Template_simplified_version.yaml");
  const templateFull = getYamlStr("./Board_Template_multilingual_support.yaml");
  
  onMount(() => {
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

    const content = getYamlStr("./Board_Template_multilingual_support.yaml");

    
    // Setup minimal model
    // @ts-ignore
    const yamlMinimalUri = monaco.Uri.parse('file:///minimal.yaml');
    // @ts-ignore
    let mininmalModel = monaco.editor.getModel(yamlMinimalUri);
    if (!mininmalModel) {
      // @ts-ignore
      mininmalModel = monaco.editor.createModel(templateMininmal, 'yaml', yamlMinimalUri);
    }
    // Setup default model
    // @ts-ignore
    const yamlDefaultUri = monaco.Uri.parse('file:///default.yaml');
    // @ts-ignore
    let defaultModel = monaco.editor.getModel(yamlDefaultUri);
    if (!defaultModel) {
      // @ts-ignore
      defaultModel = monaco.editor.createModel(templateDefault, 'yaml', yamlDefaultUri);
    }
    // Setup full model
    // @ts-ignore
    const yamlFullUri = monaco.Uri.parse('file:///full.yaml');
    // @ts-ignore
    let fullModel = monaco.editor.getModel(yamlFullUri);
    if (!fullModel) {
      // @ts-ignore
      fullModel = monaco.editor.createModel(templateFull, 'yaml', yamlFullUri);
    }

    // @ts-ignore
    const editor = monaco.editor.create(document.getElementById('yaml-editor'), {
      automaticLayout: true,
      // @ts-ignore
      model: defaultModel,
      theme: "vs-dark",
      autoIndent: true,
      tabSize: 2,
      formatOnType: true
    });

    // @ts-ignore
    monaco.editor.onDidChangeMarkers(([resource]) => {
      const problems = document.getElementById('problems')!
      // @ts-ignore
      const markers = monaco.editor.getModelMarkers({ resource })
      while (problems.lastChild) {
        problems.lastChild.remove()
      }
      for (const marker of markers) {
        // marker.severity 1 : hint
        if (marker.severity === 1) {
          continue
        }
        const wrapper = document.createElement('div')
        wrapper.setAttribute('role', 'button')
        const codicon = document.createElement('div')
        const text = document.createElement('div')
        wrapper.classList.add('problem')
        // marker.severity 4 : warning
        codicon.classList.add(
          'codicon',
          marker.severity === 4 ? 'codicon-warning' : 'codicon-error'
        )
        text.classList.add('problem-text')
        text.textContent = marker.message
        wrapper.append(codicon, text)
        wrapper.addEventListener('click', () => {
          editor.setPosition({ lineNumber: marker.startLineNumber, column: marker.startColumn })
          editor.focus()
        })
        problems.append(wrapper)
      }
    })


    setEditor(editor);
  });

  onCleanup(() => {
    editor()?.dispose();
  });

  const changeHandler = (e: any) => {
    // @ts-ignore
    const myModal = new bootstrap.Modal(document.getElementById('exampleModal'))
  }

  const confirm = (e: any) => {
    editor()?.getModel().setValue(presetEl()?.value);
  }

  return (
    <>
      <div class="row p-3" style="max-width: 600px">
        <label for="preset" class="col-sm-2 col-form-label">Preset</label>
        <div class="col-sm-10">
          <select class="form-select" ref={setPresetEl} onChange={changeHandler}>
            <option value="file:///minimal.yaml">minimal</option>
            <option value="file:///default.yaml" selected>default</option>
            <option value="file:///full.yaml">full</option>
          </select>
        </div>
      </div>
      <div style="flex: 1;">
        <div id="yaml-editor" style="width: 100%; height: 100%;"></div>
      </div>
      <div style="height: 300px; overflow:scroll; ">
        <div id="problems" style="width: 100%; height: 100%;"></div>
      </div>
      <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h1 class="modal-title fs-5" id="exampleModalLabel">Modal title</h1>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              ...
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="button" class="btn btn-primary" onClick={confirm}>Save changes</button>
            </div>
          </div>
        </div>
      </div>
      <script src="monaco-editor.js"></script>
    </>
  );
}
