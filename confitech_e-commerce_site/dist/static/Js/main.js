async function loadPartials() {
  const partials = ["header.hbs"];

  let promises = partials.reduce((acc, partialName) => {
    let response = fetch(`/static/partials/${partialName}`).then((response) =>
      response.text()
    );
    acc.push(response);
    return acc;
  }, []);

  let partialsContent = await Promise.all(promises);

  let partialsMap = {};

  partials.forEach((partial, idx) => {
    partialsMap[partial] = partialsContent[idx];
  });

  return partialsMap;
}

async function renderPartials(params) {
  let partials = await loadPartials();
  console.log(partials);
  const template = Handlebars.compile(partials["header.hbs"]);
  const rTemplate = template({ name: "Nils" });

//   document.addEventListener("DOMContentLoaded", function () {
    let mainDiv = document.getElementById("karis");
    mainDiv.innerHTML = rTemplate
//   });
}

renderPartials();
