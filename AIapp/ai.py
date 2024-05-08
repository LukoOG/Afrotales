from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import sys
import time
import os
from openai import OpenAI

client = OpenAI(api_key= os.environ['API_KEY'])

def recognize_text_from_image(url):
    read_image_url = url
    subscription_key=os.environ['SUBSCRIPTION_KEY']
    endpoint="https://afrotale-vision.cognitiveservices.azure.com/"
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    read_response = computervision_client.read(read_image_url,  raw=True)
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
    text_list = []
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
             for line in text_result.lines:
                 text_list.append(line.text)
    return text_list
    


print("End of Computer Vision quickstart.")

#Function to filter user text
def filter_text(text):
    response = client.moderations.create(input=text)
    output = response.results[0]
    return output

# Function to get desription
def fetch_description(synopsis):
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages = [
            {'role': 'user', 'content': f"""generate a concise engaging, professional and educative description based on the African literature excerpt inputted.
        ###
        outline: At the gates, Biafran Soldiers were waving cars through. They looked distinguished in their khaki uniforms, boots shining, half of a yellow sun sewn or their sleeves. Ugwu wished he was one of them. Master waved and said, "Well done!"
        description: The Biafran Armed forces. They participated in the Nigeria-Biafran war, which was a civil war fought between Nigerian and the Replublic of Biafra. 
        In this scene the character Ugwu was near where the biafran troops were stationed and he wanted to be part of the war effort.
             
        ###
             
        outline: Captain Winterbottom had not known real sleep since the dry, cool harmattan wind stopped abruptly in December, and it was now in mid february. He had grown pale and thin, and in spite-of the heat, his feet often felt cold
        description: In the text, the harmattan's sudden cessation signifies a change in the climate, possibly indicating the transition to a warmer season. Captain Winterbottom's struggle to sleep and his physical deterioration despite the heat suggest 
        that the absence of the harmattan has affected him negatively, disrupting his accustomed environment and routine.
        
        ###
             
        outline: "It's rather silly how the Northerners will pay foreigners twice more than hire a Southerner. But there's quite a bit of money to be made there. Nigel's just rung to tell me about his friend, John, a ghastly Scot. Anyway, John's a charter pilot and has made a small fortune flying Igbo people to safety these past few days. He said hundreds were killed in Zaria alone."
        description: This excerpt highlights the socio-economic dynamics and the discrimination faced by Southerners in the job market: Northerners hired foreigners at higher wages rather than their Southern counterparts. Nigel's friend, John is involved in flying people to safety, highlighting the situaation's severity.
        
        ###
             
        outline:{synopsis}
        description:
        """
        }
        ],
        max_tokens=110
    )
    return response.choices[0].message.content

#shorten this thing
"""
             
        outline: Opokuya and Kubi lived on Sweet Breezes Hill, once the most prestigious colonial residential area. They resided in the same old colonial surveyor’s bungalow built in the 1930s, where Opokuya was acutely aware of the various spirits inhabiting the house. These spirits included that of the first surveyor, likely the one who selected the hill for occupation, and the English civil servants sent to administer the territories and civilize the natives. The natives, both along the Guinea coast and in the country's interior, were considered some of the rudest and most untameable within the British Empire, though the reason for this reputation remained unknown. Over time, a significant number of Englishmen had arrived, accompanied by their women.
        description: This passage provides a vivid depiction of the historical and colonial context surrounding Opokuya and Kubi's residence on Sweet Breezes Hill. The colonial surveyor's bungalow reflects the enduring colonial legacy, the house serving as a tangible reminder of the colonial era's architecture and influence. Opokuya's spiritual awareness adds an element of mysticism and cultural belief, highlighting the spiritual connection to the land and its history. Colonization is depicted to be superior and to have a paternalistic attitude towards indigenous populations. It also touches on the challenges faced by the colonial administration in dealing with the perceived "rudeness" and "untameable" nature of the local population, reflecting colonial stereotypes and prejudices. Overall, the passage offers a nuanced portrayal of the colonial legacy and its impact on African society and culture.
        
        ###
             
        outline: Despite stiff family opposition, he joined the surreptitious adventures of the student group, facing Bra Baba's disapproval and Auntie Bettie's warm but unknowing encouragement. However, when June 16th arrived and the bravery of the Soweto child became apparent to all families, his parents were shocked into a new understanding of their son. Bra Baba fell silent, recognizing his son's courage as that of a man, while Auntie Bettie praised the new generation.
        description: This excerpt encapsulates the tension between familial expectations and personal convictions within a socio-political context. The protagonist's decision to participate in student activism is met with resistance from Bra Baba, indicative of a generational and ideological divide within the family. Auntie Bettie's unwitting support symbolizes the inadvertent nurturing of the protagonist's courage, contrasting with Bra Baba's disapproval. However of events challenged the parent's perception of their son. Bra Baba's silence signifies a shift in his understanding of his son's bravery and agency, while Auntie Bettie's praise reflects a broader recognition of the his role societal change. The passage captures the complexities of familial dynamics amidst political turmoil and the transformative power of individual courage in challenging oppressive systems.
"""

# Function to fetch image prompt
def fetch_image_prompt(synopsis, option):
    messages = [
        {'role':'user', 'content':f"""
            Give a short description of an image which illustrates a/an {option} from 
         African literature excerpts using {synopsis} that can be fed into an image-generator
        """}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Adjust the engine according to your needs
        messages=messages,
        max_tokens=100
    )
    return response.choices[0].message.content

# Function to fetch image URL
def fetch_image_url(image_prompt):
    response = client.images.generate(
        prompt=f"{image_prompt}. There should be no text in this image.",
        n=1,
        size="256x256",
        quality='standard'
    )
    image_url = response.data[0].url
    return image_url