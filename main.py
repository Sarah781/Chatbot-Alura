import streamlit as st
import google.generativeai as genai


genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])


generation_config = {
    "candidate_count": 1,
    "temperature": 0.5,
}

safety_settings = {
  "HARASSMENT": "BLOCK_NONE",
  "HATE": "BLOCK_NONE",
  "SEXUAL": "BLOCK_NONE",
  "DANGEROUS": "BLOCK_NONE",
}

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)


def generate_enigma():
    enigma_model = model.generate_content(
        f"Gera um enigma curto sem dar a resposta. Onde a pessoa tentará adivinhar uma palavra correta de algum tema aleátorio"
    )
    answer_model = model.generate_content(
        f"Responda com uma unica palavra. Qual a palavra correta para resolver este enigma: {enigma_model.text}"
    )

    st.session_state["enigma"] = enigma_model.text.strip().lower()
    st.session_state["enigma_answer"] = answer_model.text.strip().lower()


def main():
    st.title("Enigmas com IA")
    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image("./img/Robo.png", width=200)

    if "enigma" not in st.session_state:
        generate_enigma()

    with col2:
        if st.button(label="Gerar enigma"):
            generate_enigma()

        with st.form("form", clear_on_submit=True):
            user_response = st.text_input(f"Responda ao enigma: {st.session_state['enigma']}", key="user_response")
            submit = st.form_submit_button(label="Enviar")

        if submit:
            # Verifica se a resposta está correta
            user_response = user_response.strip().lower()
            answer = st.session_state['enigma_answer']

            if answer.startswith(user_response):
                st.success("Parabéns! Você acertou!")
                st.balloons()
            else:
                st.error(f"Que pena, você errou! A resposta correta era: {answer}")


if __name__ == "__main__":
    main()
