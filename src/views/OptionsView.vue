<template>
  <main class="h-full w-screen flex items-center justify-center bg-white">
    <div class="w-full h-full">
      <div class="grid grid-cols-1 sm:grid-cols-5 gap-8 items-center h-full w-full">

        <!-- Imagem da capa com desfoque -->
        <div class="sm:col-span-2 flex justify-center sm:border-b-2 md:border-r-2 border-black sm:justify-start h-full">
          <img alt="casa" src="/public/casa.png" class="w-full h-full object-cover" />
        </div>

        <div class="sm:col-span-3">
          <div class="flex flex-col gap-4 px-2">
            <div >
              <span class="text-2xl font-spartan font-600">
                O que deseja modificar?
              </span>
            </div>
            <fieldset aria-label="Opções de modificação">
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
            </fieldset>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>