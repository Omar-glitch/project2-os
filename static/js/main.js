(function () {
  let filename = undefined;
  let loading = false;
  const form = document.getElementById('form');
  const inputFile = document.getElementById('file');
  const labelInput = document.getElementById('label_file');
  const description = document.getElementById('label_description');
  const sendButton = document.getElementById('sendButton');
  const portal = document.getElementById('portal');

  const createModal = ({ data, error }) => {
    let hasBeenAnError = error !== undefined;

    portal.innerHTML = `
      <div class='modal'>
        <div class='modal-container ${hasBeenAnError ? 'error' : 'sucess'}'>
          <h2>${hasBeenAnError ? 'ERROR' : data['algorithm']}</h2>
          <div class='modal-message'>
            ${error ? `<p>${error}</p>`
              : `
              <div>
                <b>Rendimiento:</b><p> ${data['performance']}</p>
              </div>
              <div>
                <b>Frecuencia:</b><p> ${data['frequency']}</p>
              </div>
              <div>
                <b>Fallos:</b><p> ${data['fails']}</p>
              </div>
              <div>
                <b>Referencias:</b><p> ${data['references']}</p>
              </div>
            `}
          </div>
          <button style='${hasBeenAnError && '--primary: red; --dark: red;'}'>Ok</button>
        </div>
      </div> 
    `

    const closeModal = () => {
      closeButton.removeEventListener('click', closeModal);
      window.removeEventListener('click', closeFromWindow)
      portal.innerHTML = '';
    }

    const closeFromWindow = (e) => {
      if (!modalContainer.contains(e.target)) closeModal();
    }

    const closeButton = portal.querySelector('button');
    const modalContainer = portal.querySelector('.modal-container')
    closeButton.addEventListener('click', closeModal);

    window.addEventListener('click', closeFromWindow)
  }

  form.addEventListener('submit', e => {
    e.preventDefault();
    if (loading) return;

    if (inputFile.files.length === 0) 
      return createModal({error : 'No has seleccionado un archivo.'})

    loading = true;
    sendButton.disabled = true;
    sendButton.innerText = 'Enviando...';
    const formdata = new FormData(form)
    fetch('/', {method: 'post', body: formdata})
      .then(res => res.json())
      .then(createModal)
      .catch(() => createModal({error : 'cannot fetch data, maybe server is not running'}))
      .finally(() => {
        loading = false;
        sendButton.disabled = false;
        sendButton.innerText = 'Enviar';
        inputFile.files = new DataTransfer().files;
        filename = undefined;
        description.innerText = 'Ingrese o arrastre su archivo';
      })
  })
  
  inputFile.addEventListener('change', e => {
    e.preventDefault()
    filename = inputFile.files[0]?.name;
    description.innerText = filename || 'Ingrese o arrastre su archivo';
  })  
  
  labelInput.addEventListener('dragover', e => {
    e.preventDefault();
    labelInput.style.color = 'var(--dark)'
  })
  
  labelInput.addEventListener('dragleave', () => {
    labelInput.style.color = 'currentColor'
  })
  
  labelInput.addEventListener('drop', e => {
    labelInput.style.color = 'currentColor'
    const file = e.dataTransfer.files[0];
    if (!file?.name.endsWith('.xlsx') && !file?.name.endsWith('.xls')) return;
    const dT = new DataTransfer();
    dT.items.add(file)
    inputFile.files = dT.files;
    filename = file?.name;
    description.innerText = filename || 'Ingrese o arrastre su archivo';
  })
  
  window.addEventListener('dragover', e => e.preventDefault(), false)
  window.addEventListener('drop', e => e.preventDefault(), false)
})()
