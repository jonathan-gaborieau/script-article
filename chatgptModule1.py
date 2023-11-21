import openai
import time
openai.api_key = "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"

def launch_gpt(phrase):
    prompt = f""+phrase+""
    print("LANCEMENTGPT ")

    MAX_ATTEMPTS = 3
    DELAY_BETWEEN_ATTEMPTS = 5  # Secondes

    for attempt in range(MAX_ATTEMPTS):
        print("LANCEUR BOUCLE")
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4", #gpt-3.5-turbo 
                messages=[{"role": "assistant", "content": prompt}]
            )
            break  # Si l'opération réussit, sortez de la boucle
        except openai.error.OpenAIError as e:
            if "timeout" in str(e).lower() and attempt < MAX_ATTEMPTS - 1:
                # Si c'est une erreur de timeout et que ce n'est pas la dernière tentative, attendez un peu et essayez à nouveau
                time.sleep(DELAY_BETWEEN_ATTEMPTS)
                print("RELANCE ")
                continue
            else:
                # Sinon, lever l'exception ou la gérer comme vous le souhaitez
                print("ERROR")
                print(e)
                continue

        print("C'EST PARTIE")
    return completion['choices'][0]['message']['content']