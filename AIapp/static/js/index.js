const setupInputContainer = document.getElementById('setup-input-container')
const movieBossText = document.getElementById('movie-boss-text')
const setupChoice = document.getElementById('setup-choice')
// const setupFileInput = document.getElementById('file-input')

var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

const checkfile = (e) => {
  var fileType = e["type"];
  var validImageTypes = ["image/jpg", "image/jpeg", "image/png"];
  if (!validImageTypes.includes(fileType)) {
      return false
  } else {
    return true
  }
}

document.getElementById('setup-image').addEventListener('change', (e) =>{
  let file = e.target.files[0]
  if(file){
    let text = `"${file.name}"`
    document.getElementById('file-input').innerText = text
  }
  else{
    console.log('no file')
  }
}
)

document.getElementById("send-btn").addEventListener("click", () => {
  const setupImage = document.getElementById('setup-image')
  const img = setupImage.files[0]
  const choice = setupChoice.value
  if ((img) && checkfile(img)) {
    let formData = new  FormData()
    formData.append('image', img)
    formData.append('option', choice)
    setupInputContainer.innerHTML = `<img src='/static/img/loading.svg' class='loading' id='loading' >`
    movieBossText.innerText = `Ok, just wait a second while my digital brain digests that...`
    fetchImage(formData)
  } else {
    movieBossText.innerText = 'Please upload an image'
  }
})

let url =`https://${window.azureWebsiteHostname}/upload_image/`
console.log(url)

async function fetchImage(file) {
  console.log('fetching')
  let res = await fetch(
    url,{
        'method':'POST',
        'headers':{
          'X-CSRFToken':csrftoken,
        },
        'body': file      
    }
)
  const data = await res.json()
  console.log(data)

  const words = data.description.split(' ');
  movieBossText.innerText = ''
  
  let index = 0;
  const interval = setInterval(() => {
      let description = words[index]
      movieBossText.innerText += ` ${description}`; //most disturbing code ever
      index++;
      if (index >= words.length) {
          clearInterval(interval);
      }
      window.scrollTo(0, document.body.scrollHeight);
  }, 100); 
  
  document.getElementById('output-img-container').innerHTML = `<img src="${data.image}">`
  setupInputContainer.innerHTML= ``
}