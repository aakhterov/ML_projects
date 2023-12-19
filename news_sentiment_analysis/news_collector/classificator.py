import requests
import os


class Classificator:

    def __init__(self):
        self.API_token = os.environ["API_TOKEN"]
        self.API_url = "https://api-inference.huggingface.co/models/aav-ds/news_sentiment_model"
        # self.API_url = "https://b7e5c7608b45f6b9b8f9a76e97d30042.m.pipedream.net"

    def __query(self, payload):
        headers = {"Authorization": f"Bearer {self.API_token}"}
        is_success = False
        while not is_success:
            response = requests.post(self.API_url, headers=headers, json=payload)
            if response.status_code == 503:
                payload["options"] = {"wait_for_model": True}
            else:
                is_success = True
        return response.json()

    def predict(self, text):
        res = self.__query({"inputs": text})
        #[[{'label': 'Anti-Israel', 'score': 0.9998886585235596}, {'label': 'Pro-Israel', 'score': 0.00011135219392599538}]]
        output = res[0][0]['score'] if res[0][0]['label'] == 'Pro-Israel' else res[0][1]['score']
        return output


if __name__ == "__main__":
    cl = Classificator()
    post = '''
    Earlier this morning, an official for UNRWA - the UN's agency for Palestinian refugees - spoke to the BBC from Rafah in south Gaza. He described a "desperate situation" for locals.
Tom White told BBC Radio 4's Today programme that a ceasefire was crucial. "Here in Rafah we have hundreds of thousands of people who are living in the open," he explained. "There is a lack of water. Everyone in the street is asking for flour to feed their children.
"Our shelters have well over 7,000 people. There are hundreds using the one toilet for example.
"If the bombs aren't going to kill them, it is the disease, or for those living out on the streets, it'll be the exposure."
Describing his trip to a UN distribution centre in Rafah on Friday, White said: "All you could hear was air strikes going into the city." He also told the BBC a guesthouse he shared with colleagues was hit last night.
    '''
    res = cl.predict(post)
    print(res)



