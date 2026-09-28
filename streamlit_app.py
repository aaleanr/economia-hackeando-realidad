import streamlit as st

st.set_page_config(
    page_title="Economía: Hackeando la realidad",
    page_icon="⚡",
    layout="centered",
)

st.markdown("""
<style>
    .block-container {
        max-width: 850px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    .brand {
        color: #0f766e;
        font-size: 0.85rem;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .hero-title {
        font-size: clamp(2.3rem, 7vw, 4.5rem);
        line-height: 0.98;
        font-weight: 800;
        margin: 0.5rem 0 1rem 0;
    }

    .mission {
        background: #e8f3f0;
        padding: 1rem 1.2rem;
        border-radius: 14px;
        margin: 1.2rem 0;
    }

    .metric-card {
        border: 1px solid #d9dfdc;
        border-radius: 12px;
        padding: 0.8rem;
        text-align: center;
    }

    .metric-name {
        font-size: 0.75rem;
        color: #65716c;
    }

    .metric-value {
        font-size: 1.4rem;
        font-weight: 800;
    }

    div.stButton > button {
        min-height: 55px;
        border-radius: 12px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# DATA
# ---------------------------------------------------------

ROUNDS = [
    {
        "title": "Vivienda",
        "question": "La ciudad necesita vivienda asequible. ¿Qué haces?",
        "choices": [
            (
                "🏘️ Construir en las afueras",
                "Es más barato, pero aumenta los desplazamientos.",
                [-2, 2, 0, -1, 2],
            ),
            (
                "🏙️ Construir cerca del centro",
                "Es más costoso, pero reduce los tiempos de viaje.",
                [1, 0, 1, 1, -2],
            ),
            (
                "📈 Dejar que el mercado decida",
                "Hay menos gasto público, pero aumenta la presión sobre los precios.",
                [0, -1, -1, 0, 2],
            ),
        ],
    },
    {
        "title": "Transporte",
        "question": "La congestión está aumentando. ¿Dónde pones el dinero?",
        "choices": [
            (
                "🛣️ Ampliar las vías",
                "Facilita el tráfico inicialmente.",
                [1, 1, -1, -2, -3],
            ),
            (
                "🚌 Fortalecer el transporte público",
                "Reduce la congestión y conecta a más personas.",
                [1, 2, 2, 1, -1],
            ),
            (
                "⏸️ No intervenir",
                "Ahorras recursos hoy.",
                [0, -1, -2, 0, 3],
            ),
        ],
    },
    {
        "title": "Impuestos",
        "question": "Necesitas financiar servicios públicos. ¿Qué haces?",
        "choices": [
            (
                "💸 Bajar impuestos",
                "Puede estimular la actividad privada, pero reduce los ingresos públicos.",
                [2, 0, -2, -1, 2],
            ),
            (
                "⚖️ Mantenerlos y mejorar el gasto",
                "Buscas mayor eficiencia del presupuesto.",
                [1, 1, 2, 2, -1],
            ),
            (
                "🏛️ Subir impuestos",
                "Obtienes más recursos para servicios públicos.",
                [-1, -1, 3, 1, -3],
            ),
        ],
    },
    {
        "title": "Energía",
        "question": "La ciudad debe elegir su estrategia energética.",
        "choices": [
            (
                "⚡ Elegir la opción más barata",
                "Reduce los costos ahora.",
                [2, 1, -2, 0, 2],
            ),
            (
                "🌱 Invertir en renovables",
                "Mayor costo inicial, menor contaminación futura.",
                [0, 0, 2, 3, -2],
            ),
            (
                "🔌 Mezclar tecnologías",
                "Diversificas riesgos y costos.",
                [1, 1, 1, 2, -1],
            ),
        ],
    },
    {
        "title": "Educación",
        "question": "Tienes recursos para una última gran inversión.",
        "choices": [
            (
                "🎓 Educación básica",
                "Aumenta las oportunidades de una gran parte de la población.",
                [1, 2, 3, 1, -2],
            ),
            (
                "🧠 Formación especializada",
                "Impulsa sectores de alta productividad.",
                [3, 1, 0, 1, -1],
            ),
            (
                "💰 No invertir ahora",
                "Conservas el presupuesto.",
                [0, -2, -3, 0, 3],
            ),
        ],
    },
]


METRICS = [
    ("📈", "Crecimiento"),
    ("👷", "Empleo"),
    ("⚖️", "Igualdad"),
    ("🌱", "Ambiente"),
    ("😊", "Bienestar"),
]


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "started" not in st.session_state:
    st.session_state.started = False

if "round" not in st.session_state:
    st.session_state.round = 0

if "budget" not in st.session_state:
    st.session_state.budget = 10

if "metric_values" not in st.session_state:
    st.session_state.metric_values = [50, 50, 50, 50, 50]

# NEW: stores previous states so the user can go back
if "history" not in st.session_state:
    st.session_state.history = []


def reset_game():
    st.session_state.started = True
    st.session_state.round = 0
    st.session_state.budget = 10
    st.session_state.metric_values = [50, 50, 50, 50, 50]

    # Clear previous decisions
    st.session_state.history = []


def choose(option):
    # Save the current state BEFORE making the decision.
    # This allows the user to undo the decision later.
    st.session_state.history.append(
        {
            "round": st.session_state.round,
            "budget": st.session_state.budget,
            "metric_values": st.session_state.metric_values.copy(),
        }
    )

    effects = ROUNDS[st.session_state.round]["choices"][option][2]

    st.session_state.metric_values = [
        max(0, min(100, value + effect))
        for value, effect in zip(
            st.session_state.metric_values,
            effects,
        )
    ]

    if option == 1:
        st.session_state.budget -= 2
    else:
        st.session_state.budget -= 1

    st.session_state.round += 1


# NEW: restore the previous state
def go_back():
    if not st.session_state.history:
        return

    previous = st.session_state.history.pop()

    st.session_state.round = previous["round"]
    st.session_state.budget = previous["budget"]
    st.session_state.metric_values = previous["metric_values"]


def show_metrics():
    columns = st.columns(5)

    for col, (icon, name), value in zip(
        columns,
        METRICS,
        st.session_state.metric_values,
    ):
        with col:
            st.metric(
                label=f"{icon} {name}",
                value=value,
            )


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="brand">UTB · EXPERIENCIA INTERACTIVA</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-title">Economía:<br>Hackeando la realidad</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# INTRO
# ---------------------------------------------------------

if not st.session_state.started:

    st.write(
        "Una misión para descubrir que la economía no consiste "
        "solamente en números: consiste en tomar decisiones cuando "
        "los recursos son limitados y las consecuencias importan."
    )

    st.markdown(
        """
        <div class="mission">
        <strong>🏙️ Tu misión</strong><br><br>
        Bienvenido a Ciudad Nova. Tienes recursos limitados y una
        ciudad llena de problemas. Durante cinco decisiones tendrás
        que elegir qué hacer.
        <br><br>
        <strong>Objetivo:</strong> mejorar el bienestar de la ciudad
        sin destruir las condiciones que lo hacen posible.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "💡 No busques «la respuesta correcta». "
        "Busca entender las consecuencias de cada decisión."
    )

    if st.button(
        "🚀 Empezar la misión",
        type="primary",
        use_container_width=True,
    ):
        reset_game()
        st.rerun()

    st.caption(
        "Puedes jugar individualmente o ponerte de acuerdo con tu grupo."
    )


# ---------------------------------------------------------
# GAME
# ---------------------------------------------------------

elif st.session_state.round < len(ROUNDS):

    current = ROUNDS[st.session_state.round]

    col1, col2 = st.columns([4, 1])

    with col1:
        st.caption(
            f"DECISIÓN {st.session_state.round + 1} DE {len(ROUNDS)} "
            f"· {current['title'].upper()}"
        )

    with col2:
        st.metric(
            "💰 Presupuesto",
            st.session_state.budget,
        )

    st.header(current["question"])

    st.write(
        "Elige una opción. Después verás cómo cambia la ciudad."
    )

    for i, (title, description, _) in enumerate(current["choices"]):

        if st.button(
            title,
            key=f"choice_{st.session_state.round}_{i}",
            use_container_width=True,
        ):
            choose(i)
            st.rerun()

        st.caption(description)

    # NEW: Back button
    if st.session_state.history:

        st.divider()

        if st.button(
            "← Cambiar mi decisión anterior",
            use_container_width=True,
        ):
            go_back()
            st.rerun()

    st.divider()

    st.caption("ESTADO ACTUAL DE LA CIUDAD")

    show_metrics()

    st.caption(
        "Observa los intercambios: mejorar un indicador puede "
        "empeorar otro."
    )


# ---------------------------------------------------------
# RESULTS
# ---------------------------------------------------------

else:

    st.success("🎉 MISIÓN COMPLETADA")

    st.header("Acabas de hacer economía.")

    st.write(
        "No existía una decisión perfecta. Cada elección implicó "
        "**costos de oportunidad**, afectó a distintos grupos y "
        "produjo consecuencias que no eran completamente visibles "
        "al principio."
    )

    st.subheader("Así quedó Ciudad Nova")

    show_metrics()

    st.markdown(
        """
        <div class="mission">
        <strong>⚡ El verdadero hack</strong><br><br>
        Los economistas utilizan <strong>modelos, datos, incentivos
        y evidencia</strong> para entender esas consecuencias antes
        de tomar decisiones.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("### ¿Y ahora qué?")

    st.write(
        "Esto es solo una pequeña muestra de lo que puede hacer "
        "un economista: convertir preguntas sobre la realidad en "
        "problemas que podemos analizar con datos."
    )

    if st.button(
        "🔄 Jugar otra vez",
        use_container_width=True,
    ):
        reset_game()
        st.rerun()

    st.caption(
        "Economía · Universidad Tecnológica de Bolívar"
    )
