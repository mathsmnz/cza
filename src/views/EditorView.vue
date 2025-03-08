<script>
import { ref, onMounted } from "vue";
import * as WEBIFC from "web-ifc";
import * as THREE from "three";
import * as OBC from "@thatopen/components";
import * as OBCF from "@thatopen/components-front";

export default {
  setup() {
    const container = ref(null); // Container for the Three.js renderer
    const fragments = ref(null); // Initialize fragments as a ref
    let model = null;
    let world = null;
    const components = new OBC.Components();
    const highlighter = components.get(OBCF.Highlighter);
    let fileName = "";
    const plans = ref(null);
    const culler = ref(null);
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    let modelItems = [];
    let classifier = null;
    let grid = null;

    // Setup world (scene, camera, renderer, etc.)
    const setupWorld = async () => {
      if (!container.value) {
        console.error("Container element is not available!");
        return;
      }

      const worlds = components.get(OBC.Worlds);

      // Create a new world and assign it to the world variable
      world = worlds.create(OBC.SimpleScene, OBC.OrthoPerspectiveCamera, OBCF.PostproductionRenderer);

      world.scene = new OBC.SimpleScene(components);
      world.renderer = new OBCF.PostproductionRenderer(components, container.value); // Ensure container is passed
      world.camera = new OBC.OrthoPerspectiveCamera(components);

      world.renderer.postproduction.enabled = true;
      world.renderer.postproduction.customEffects.outlineEnabled = true;

      components.init();

      await world.camera.controls.setLookAt(12, 6, 8, 0, 0, -10);

      world.scene.setup();
      world.scene.three.background = new THREE.Color(0xFFFFFF);
    };

    const captureScreenshot = async () => {
      if (!world || !world.renderer || !container.value) return;
      // Esconde o grid antes da captura
      if (grid) grid.three.visible = false;

      let activePlan = plans.value.current;
      console.log(activePlan);
      if (!activePlan) {
        activePlan = plans.value.list[0];
        console.warn("Nenhuma planta ativa para captura.");
      }

      console.log(activePlan)

      // Ajusta a câmera para maximizar o zoom no plano ativo
      await fitToPlanView();

      // Pequeno delay para garantir que a cena seja atualizada antes da captura
      await new Promise(resolve => setTimeout(resolve, 500));

      // Renderiza a cena
      world.renderer.three.render(world.scene.three, world.camera.three);

      // Captura a imagem
      const screenshot = container.value.querySelector('canvas').toDataURL('image/png');
      const link = document.createElement('a');
      link.href = screenshot;
      const screenshotName = fileName.split(".")[0];
      link.download = `${screenshotName}.png`;
      link.click();

      // Restaura a visibilidade do grid após a captura
      if (grid) grid.three.visible = true;
    };

    // Função que ajusta o zoom no plano antes da captura
    const fitToPlanView = async (offset = .2) => {

      const boundingBox = model.boundingBox;
      const center = new THREE.Vector3();
      boundingBox.getCenter(center);

      const size = new THREE.Vector3();
      boundingBox.getSize(size);

      const maxDim = Math.max(size.x, size.y, size.z);

      const sidebarWidth = document.getElementById("menuLateral")?.offsetWidth || 0;
      const viewportWidth = window.innerWidth - sidebarWidth;
      const scaleFactor = viewportWidth / window.innerWidth;

      const box = new THREE.Box3(
        new THREE.Vector3(-maxDim, -maxDim, -maxDim),
        new THREE.Vector3(maxDim, maxDim, maxDim)
      );
      const sceneSize = new THREE.Vector3();
      box.getSize(sceneSize);
      const sceneCenter = new THREE.Vector3();
      box.getCenter(sceneCenter);

      // Calculate offset for centering considering sidebar width
      const xOffset = (sidebarWidth / window.innerWidth) * sceneSize.x;
      sceneCenter.x += (xOffset / 2.0); // Shift center to compensate for sidebar

      const radius = Math.max(sceneSize.x, sceneSize.y, sceneSize.z) * offset * scaleFactor;
      const sphere = new THREE.Sphere(sceneCenter, radius);

      await world.camera.controls.fitToSphere(sphere, false);

      // Garante que a câmera está olhando para o modelo
      world.camera.three.lookAt(sceneCenter);
    };

    // Setup grid
    const setupGrid = (world) => {
      const grids = components.get(OBC.Grids);
      grid = grids.create(world);

      grid.three.position.y -= 1.5;
      grid.config.color.setHex(0x000000);

      world.renderer.postproduction.customEffects.excludedMeshes.push(grid.three);
    };

    const setupBoundingBox = (modelToFit) => {
      const fragmentBox = components.get(OBC.BoundingBoxer);

      if (modelToFit) {
        fragmentBox.add(modelToFit);

        // Obter o mesh da caixa delimitadora
        const bboxMesh = fragmentBox.getMesh();

        // Garantir que a bounding box seja computada corretamente
        bboxMesh.geometry.computeBoundingBox();
        const boundingBox = bboxMesh.geometry.boundingBox;

        // Calcular o centro e o tamanho da caixa delimitadora
        const center = new THREE.Vector3();
        boundingBox.getCenter(center);

        const size = new THREE.Vector3();
        boundingBox.getSize(size);

        model.boundingBox = boundingBox;

        // Calcular a distância ideal da câmera para enquadrar o modelo
        const fov = world.camera.three.fov * (Math.PI / 180); // Converter FOV para radianos
        const maxDim = Math.max(size.x, size.y, size.z);
        let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2));

        cameraZ *= 1.1; // Fator de segurança

        // Definir a posição da câmera e direcioná-la ao centro do modelo
        world.camera.three.position.set(center.x, center.y, cameraZ);
        world.camera.three.lookAt(center);

        // Ajustar os controles da câmera
        if (world.camera.controls) {
          world.camera.controls.target = [center.x, center.y, center.z];
          world.camera.controls.position = [center.x, center.y, cameraZ];
        }

        fragmentBox.reset(); // Limpar o BoundingBoxer após o uso
      }
    };

    const planManager = async () => {
      plans.value = components.get(OBCF.Plans);
      plans.value.world = world;
      await plans.value.generate(model);

      const cullers = components.get(OBC.Cullers);
      culler.value = cullers.create(world);
      for (const fragment of model.items) {
        culler.value.add(fragment.mesh);
      }

      culler.value.needsUpdate = true;

      world.camera.controls.addEventListener("sleep", () => {
        culler.value.needsUpdate = true;
      });

      classifier = components.get(OBC.Classifier);
      const edges = components.get(OBCF.ClipEdges);

      classifier.byModel(model.uuid, model);
      classifier.byEntity(model);

      modelItems = classifier.find({ models: [model.uuid] });

      const thickItems = classifier.find({
        entities: ["IFCWALLSTANDARDCASE", "IFCWALL"],
      });

      const thinItems = classifier.find({
        entities: ["IFCDOOR", "IFCWINDOW", "IFCPLATE", "IFCMEMBER"],
      });

      const grayFill = new THREE.MeshBasicMaterial({ color: "gray", side: 2 });
      const blackLine = new THREE.LineBasicMaterial({ color: "black" });
      const blackOutline = new THREE.MeshBasicMaterial({
        color: "black",
        opacity: 0.5,
        side: 2,
        transparent: true,
      });

      edges.styles.create(
        "thick",
        new Set(),
        world,
        blackLine,
        grayFill,
        blackOutline,
      );

      const frag = fragments.value;

      for (const fragID in thickItems) {
        const foundFrag = frag.list.get(fragID);
        if (!foundFrag) continue;
        const { mesh } = foundFrag;
        edges.styles.list.thick.fragments[fragID] = new Set(thickItems[fragID]);
        edges.styles.list.thick.meshes.add(mesh);
      }

      edges.styles.create("thin", new Set(), world);

      for (const fragID in thinItems) {
        const foundFrag = frag.list.get(fragID);
        if (!foundFrag) continue;
        const { mesh } = foundFrag;
        edges.styles.list.thin.fragments[fragID] = new Set(thinItems[fragID]);
        edges.styles.list.thin.meshes.add(mesh);
      }

      await edges.update(true);
    }
    // Load the IFC model
    const loadIfcModel = async (url) => {
      const fragmentIfcLoader = components.get(OBC.IfcLoader);
      await fragmentIfcLoader.setup();

      const excludedCats = [
        WEBIFC.IFCTENDONANCHOR,
        WEBIFC.IFCREINFORCINGBAR,
        WEBIFC.IFCREINFORCINGELEMENT,
      ];

      for (const cat of excludedCats) {
        fragmentIfcLoader.settings.excludedCategories.add(cat);
      }

      fragmentIfcLoader.settings.webIfc.COORDINATE_TO_ORIGIN = true;

      const file = await fetch(url);
      const data = await file.arrayBuffer();
      const buffer = new Uint8Array(data);

      const loadedModel = await fragmentIfcLoader.load(buffer);
      loadedModel.name = "example";

      return loadedModel; // Return loaded model
    };

    // Setup the entire scene
    const setupScene = async () => {
      await setupWorld(); // Initialize world
      if (!world) return; // Ensure world is valid before proceeding

      setupGrid(world); // Setup grid in the scene

      // Load and add the IFC model to the scene
      const url = "https://raw.githubusercontent.com/mathsmnz/cza/refs/heads/main/public/base.ifc";
      model = await loadIfcModel(url); // Store the loaded model
      world.scene.three.add(model); // Add model to the scene
      fileName = "EXAMPLE"

      highlighter.setup({ world });
      highlighter.zoomToSelection = true;

      // Initialize fragments after the scene is set up
      fragments.value = components.get(OBC.FragmentsManager); // Correctly assign fragments

      await planManager();
      setupBoundingBox(model);
    };

    // Load IFC model from file input
    const loadIFC = async () => {
      const fileInput = document.createElement('input');
      fileInput.type = 'file';
      fileInput.accept = '.ifc';
      fileInput.onchange = async (e) => {
        const file = e.target.files[0];
        const data = await file.arrayBuffer();
        const buffer = new Uint8Array(data);

        if (!world) {
          console.error("World is not initialized.");
          return;
        }

        // Limpar memória do modelo anterior
        if (model) {
          world.scene.three.remove(model); // Remover da cena

          // Percorrer os meshes do modelo e liberar recursos
          model.traverse((child) => {
            if (child.isMesh) {
              child.geometry.dispose(); // Libera a geometria
              if (child.material) {
                if (Array.isArray(child.material)) {
                  child.material.forEach((m) => m.dispose());
                } else {
                  child.material.dispose(); // Libera o material
                }
              }
            }
          });
          model = null; // Limpar referência do modelo
        }

        // Limpar componentes anteriores
        if (plans.value) {
          plans.value.dispose();
          plans.value = null;
        }

        if (culler.value) {
          culler.value = null;
        }

        if (fragments.value) {
          fragments.value.dispose(); // Liberar memória dos fragmentos
          fragments.value = null;
        }

        // Limpar o cache do WebGL
        world.renderer.three.clear();
        world.renderer.three.dispose();

        // Carregar o novo modelo IFC
        const fragmentIfcLoader = components.get(OBC.IfcLoader);
        model = await fragmentIfcLoader.load(buffer); // Atualiza o modelo

        model.name = file.name;
        fileName = file.name;
        world.scene.three.add(model); // Adicionar o novo modelo à cena

        // Inicializar fragmentos após a configuração da cena
        fragments.value = components.get(OBC.FragmentsManager);
        await planManager();

      };
      fileInput.click();
    };

    // Save .frag and properties.json
    const saveFile = () => {
      const downloadLink = document.createElement('a');
      if (!fragments.value.groups.size) {
        return;
      }
      const group = Array.from(fragments.value.groups.values())[0];
      const data = fragments.value.export(group);
      //const name = fileName.split('.')[1];

      const properties = group.getLocalProperties();
      if (properties) {
        const newFile = new File([JSON.stringify(properties)], `${fileName}.json`);
        downloadLink.href = URL.createObjectURL(newFile);
        downloadLink.download = newFile.name;
        downloadLink.click();
      }

      const newFile = new File([new Blob([data])], `${fileName}.frag`);
      downloadLink.href = URL.createObjectURL(newFile);
      downloadLink.download = newFile.name;
      downloadLink.click();

    }

    const activatePlan = (plan) => {
      world.renderer.postproduction.customEffects.minGloss = 0.1;
      highlighter.backupColor = new THREE.Color("white");
      world.scene.three.background = new THREE.Color("white");
      const plansComponent = world.components.get(OBCF.Plans);
      plansComponent.goTo(plan.id);
      console.log(world.camera);
      culler.value.needsUpdate = true;
    };

    const exitPlanView = () => {
      world.renderer.postproduction.customEffects.minGloss = 0.0;
      highlighter.backupColor = null;
      highlighter.clear();
      classifier.resetColor(classifier.find({ models: [model.uuid] }));
      world.scene.three.background = new THREE.Color("white");
      const plansComponent = world.components.get(OBCF.Plans);
      plansComponent.exitPlanView();
      culler.value.needsUpdate = true;
    };

    onMounted(() => {
      if (container.value) {
        setupScene(); // Initialize scene after mounting
      } else {
        console.error("Container element not found when mounted.");
      }
    });

    return { container, loadIFC, saveFile, activatePlan, exitPlanView, plans, captureScreenshot }; // Expose loadIFC to the template
  },
};
</script>

<template>
  <div class="bg-gray-900 text-white h-full w-full relative">
    <!-- Viewer Container -->
    <div ref="container" class="fixed h-full w-full z-0"></div>

    <!-- Menu Lateral -->
    <div id="menuLateral" class="relative top-0 left-0 w-72 h-full bg-gray-800 p-4 shadow-lg overflow-y-auto z-10">
      <!-- Botões de Controle -->
      <button @click="loadIFC" class="w-full text-left bg-blue-500 text-white p-2 rounded shadow hover:bg-blue-600">
        Carregar Novo IFC
      </button>
      <button @click="saveFile"
        class="w-full text-left bg-green-500 text-white p-2 mt-4 rounded shadow hover:bg-green-600">
        Salvar IFC
      </button>
      <button @click="captureScreenshot"
        class="w-full text-left bg-purple-500 text-white p-2 mt-4 rounded shadow hover:bg-purple-600">
        Capturar Tela
      </button>

      <!-- Instrução -->
      <div class="text-center mt-6 px-4">
        <p class="text-gray-300 text-sm">
          Carregue um arquivo IFC para visualizar o modelo 3D.
        </p>
      </div>

      <!-- Seção de Planos -->
      <h2 class="text-lg font-semibold mt-6 mb-2 text-gray-100">Planos</h2>

      <div v-if="!plans || !plans.list.length" class="text-gray-400">
        Carregando planos...
      </div>

      <div v-else class="space-y-2">
        <button v-for="plan in plans.list" :key="plan.id"
          class="w-full text-left bg-gray-700 p-2 rounded shadow hover:bg-gray-600" @click="activatePlan(plan)">
          {{ plan.name }}
        </button>
        <button class="w-full text-left bg-red-500 text-white p-2 mt-4 rounded shadow hover:bg-red-600"
          @click="exitPlanView">
          Sair
        </button>
      </div>
    </div>
  </div>
</template>


<style scoped></style>
