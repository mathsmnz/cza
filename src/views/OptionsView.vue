<template>
  <main class="h-full w-full flex items-center justify-center bg-white">
    <div class="w-full h-full">
      <div class="grid grid-cols-1 sm:grid-cols-5 gap-8 items-center h-full w-full">

        <!-- Imagem da capa com desfoque -->
        <div
          class="sm:col-span-2 flex justify-center sm:border-b-2 md:border-r-2 border-black sm:justify-start h-full w-full">
          <img alt="casa" src="/public/casa.png" class="w-full h-full object-cover" />
        </div>

        <div class="sm:col-span-3 w-fit">
          <div class="flex flex-col gap-4 px-2">
            <div>
              <span class="text-2xl">
                O que deseja modificar?
              </span>
            </div>
            <div class="flex bg-gray-100 border-black border-2 p-4">
              <form id="myForm" class="flex flex-col p-4 gap-2" action="editor" method="get">
                <div>
                  <label>
                    <input type="radio" name="opcao" value="opcao"
                      onclick="enableCheckboxes('opcao1'); clearSelection()">
                    <span class="font-semibold"> Aumentar sala/cozinha</span>
                  </label>
                  <div class="flex flex-col px-4 gap-1" id="checkboxes1">
                    <label>
                      <input type="checkbox" name="modelo1_a" value="modelo1_a"> Para a frente</label>
                    <label>
                      <input type="checkbox" name="modelo1_b" value="modelo1_b"> Para a frente e lado</label>
                    <label>
                      <input type="checkbox" name="modelo1_c" value="modelo1_c"> Para o lado</label>
                    <label>
                      <input type="checkbox" name="modelo1_d" value="modelo1_d"> Acrescentar área de serviço</label>
                  </div>
                </div>

                <div>
                  <label>
                    <input type="radio" name="opcao" value="opcao"
                      onclick="enableCheckboxes('opcao2'); clearSelection()">
                    <span class="font-semibold"> Acrescentar cômodo para os fundos</span>
                  </label>
                  <div class="flex flex-col px-4 gap-1" id="checkboxes2">
                    <label>
                      <input type="checkbox" name="modelo2_a" value="modelo2_a"> Acesso independente
                    </label>
                    <label>
                      <input type="checkbox" name="modelo2_b" value="modelo2_b"> Acrescentar banheiro
                    </label>
                  </div>
                </div>

                <div>
                  <label>
                    <input type="radio" name="opcao" value="opcao">
                    <span class="font-semibold"> Acrescentar cômodo para a frente</span>
                  </label>
                  <div class="flex flex-col px-4 gap-1" id="checkboxes3">
                    <label>
                      <input type="checkbox" name="modelo3_a" value="modelo3_a"> Acesso independente
                    </label>
                    <label>
                      <input type="checkbox" name="modelo3_b" value="modelo3_b"> Acrescentar área de serviço
                    </label>
                  </div>
                </div>

                <div>
                  <label>
                    <input type="radio" name="opcao" value="opcao"
                      onclick="enableCheckboxes('opcao4'); clearSelection()">
                      <span class="font-semibold"> Acrescentar Pavimento</span>
                  </label>
                  <div class="flex flex-col px-4 gap-1" id="checkboxes4">
                    <label>
                      <input type="checkbox" name="modelo4" value="modelo4"> Acrescentar banheiro</label>
                  </div>
                </div>
                <input type="submit" class="btn btnform" value="Editar">
              </form>
            </div>
            <!-- <fieldset aria-label="Opções de modificação">
            <div class="rounded-md border-r-2 border-black">
              <div class="flex gap-2">
                <div class="">
                  <input id="op0" name="opcao-0" type="radio" aria-describedby="opcao-0-descricao" class="">
                </div>
                <div class="flex flex-col">
                  <label for="op0" class="font-semibold">Separar cozinha da sala de estar </label>
                  <span id="op0" class=" italic font-light">Descrição dessa opt</span>
                </div>
              </div>
              <div class="flex gap-2">
                <div class="">
                  <input id="op0" name="opcao-0" type="radio" aria-describedby="opcao-0-descricao" class="">
                </div>
                <div class="flex flex-col">
                  <label for="op0" class="font-semibold">Expandir cozinha/sala de estar para frente </label>
                  <span id="op0" class=" italic font-light">Descrição dessa opt</span>
                </div>
              </div>
              <div class="flex gap-2">
                <div class="">
                  <input id="op0" name="opcao-0" type="radio" aria-describedby="opcao-0-descricao" class="">
                </div>
                <div class="flex flex-col">
                  <label for="op0" class="font-semibold">Expandir cozinha/sala de estar para o lado </label>
                  <span id="op0" class=" italic font-light">Descrição dessa opt</span>
                </div>
              </div>
              <div class="flex gap-2">
                <div class="">
                  <input id="op0" name="opcao-0" type="radio" aria-describedby="opcao-0-descricao" class="">
                </div>
                <div class="flex flex-col">
                  <label for="op0" class="font-semibold">Expandir cozinha/sala de estar para frente e o lado </label>
                  <span id="op0" class=" italic font-light">Descrição dessa opt</span>
                </div>
              </div>
              <div class="flex gap-2">
                <div class="">
                  <input id="op0" name="opcao-0" type="radio" aria-describedby="opcao-0-descricao" class="">
                </div>
                <div class="flex flex-col">
                  <label for="op0" class="font-semibold">Adicionar uma sala na frente </label>
                  <span id="op0" class=" italic font-light">Descrição dessa opt</span>
                </div>
              </div>
              <div class="flex gap-2">
                <div class="">
                  <input id="op0" name="opcao-0" type="radio" aria-describedby="opcao-0-descricao" class="">
                </div>
                <div class="flex flex-col">
                  <label for="op0" class="font-semibold">Adicionar uma sala na parte de trás </label>
                  <span id="op0" class=" italic font-light">Descrição dessa opt</span>
                </div>
              </div>
              <div class="flex gap-2">
                <div class="">
                  <input id="op0" name="opcao-0" type="radio" aria-describedby="opcao-0-descricao" class="">
                </div>
                <div class="flex flex-col">
                  <label for="op0" class="font-semibold">Adicionar uma lavanderia </label>
                  <span id="op0" class=" italic font-light">Descrição dessa opt</span>
                </div>
              </div>
            </div>
          </fieldset> -->
          </div>
        </div>
      </div>
    </div>
  </main>
</template>