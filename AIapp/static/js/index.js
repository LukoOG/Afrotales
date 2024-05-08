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

async function fetchImage(file) {
  console.log('fetching')
  let res = await fetch(
    'http://localhost:8000/upload_image/',{
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

// async function fetchBotReply(outline) {
//   const response = await oPenai.createCompletion({
//     model: 'gpt-3.5-turbo-instruct',
//     prompt: `
//       Generate an enthusiastic response to the given outline.
//       ###
//       outline: Temi and I used to argue with other people about how children are the worst kind of pollution, that really if we wanted to help the planet we should kill half of the population, then ourselves, and use the remains as compost for planting trees.
//       response: This sounds fascinating! I'm eager to illustrate this unique perspective, especially the part about environmental impact and population control!
//       ###
//       outline: Ugwu stood by the door, waiting. Sunlight streamed in through the windows, and from time to time a gentle breeze lifted the curtains.
//       response: What an evocative scene! I'm already envisioning the sunlight dancing through the curtains. Count me in to illustrate this moment!
//       ###
//       outline: ${outline}
//       response: Wow, that's intriguing! I can't wait to bring this to life through illustration!
//       `,
//     max_tokens: 60 
//   })
//   movieBossText.innerText = response.data.choices[0].text.trim()
//   console.log(response) 
// }

// async function fetchSynopsis(outline) {
//   const response = await oPenai.createCompletion({
//     model: 'gpt-3.5-turbo-instruct',
//     prompt: `Generate an engaging, professional and educative analysis based on an african literature excerpt
//     ###
//     outline: At the gates, Biafran soldiers were waving cars through. They
//     looked distinguished in their khaki uniforms, boots shining, half of a
//     yellow sun sewn on their sleeves. Ugwu wished he was one of them.
//     Master waved and said, "Well done!"
//     synopsis:The Biafran Armed Forces (BAF) were the military of the Nigerian secessionist state of Biafra, which existed from 1967 until 1970. They participated in the Nigerian–Biafran War or the Biafran War, whicg was a civil war fought between Nigeria and the Republic of Biafra, a secessionist state which had declared its independence from Nigeria in 1967. It seems one of the characters named Ugwu really wanted to be part of them and fight alongside them against the Nigerian forces.
//     ###
//     outline: ${outline}
//     synopsis: 
//     `,
//     max_tokens: 700
//   }) 
//   const synopsis = response.data.choices[0].text.trim()
//   document.getElementById('output-text').innerText = synopsis
//   fetchImagePromt(synopsis)
// }

// async function fetchImagePromt(synopsis){
//   const response = await oPenai.createCompletion({
//     model: 'gpt-3.5-turbo-instruct',
//     prompt: `Give a short description of an image which illustrates events, characters or objects from african literature excerpts.
//     ###
//     excerpt: "But there was no such doubt anywhere about his skin. It
//     was smooth and black, and not a layer of fat between that skin and his flesh.
//     His teeth, which he occasionally, deliberately and fashionably discoloured by
//     chewing kola, were beautifully even and white. He wore kohl around his
//     eyes, moved like a panther, and was very good looking."
//     synopsis: ${synopsis}
//     character: A fine looking man
//     image description: A handsome african black man with beautiful white teeth, he wears kohl around his eyes and runs as fast as a panther.
//     `,
//     temperature: 0.8,
//     max_tokens: 100
//   })
//   fetchImageUrl(response.data.choices[0].text.trim())
// }

// async function fetchImageUrl(imagePrompt){
//   const response = await oPenai.createImage({
//     prompt: `${imagePrompt}. There should be no text in this image.`,
//     n: 1,
//     size: '256x256',
//     response_format: 'b64_json' 
//   })
//   document.getElementById('output-img-container').innerHTML = `<img src="data:image/png;base64,${response.data.data[0].b64_json}">`
//   setupInputContainer.innerHTML = `<button id="view-pitch-btn" class="view-pitch-btn">View Pitch</button>`
//   document.getElementById('view-pitch-btn').addEventListener('click', ()=>{
//     document.getElementById('setup-container').style.display = 'none'
//     document.getElementById('output-container').style.display = 'flex'
//     movieBossText.innerText = `This idea is so good I'm jealous! It's gonna make you rich for sure! Remember, I want 10% 💰`
//   })
// }