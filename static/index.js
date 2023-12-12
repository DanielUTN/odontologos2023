const btnsConfirm = document.querySelectorAll("#btnConfirm")

if (btnsConfirm.length) {
  for (const btn of btnsConfirm) {
    btn.addEventListener("click", e => {
      resp = confirm("Esta opción no tiene marcha atrás. ¿Confirma?")
      if (!resp) e.preventDefault()
    })
  }
}
