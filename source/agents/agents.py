import autogen
from agents import agents_config
from agents.instruments import FileAgentInstruments
from modules import orchestrator

# ------------------------ PROMPTS ------------------------


USER_PROXY_PROMPT = "Un administrateur humain"
INSPECTOR_PROMPT = """
    Tu es un inspecteur de l'enseignement spécialisé en mathématique. Ta tâche est d'extraire une liste concise de pré-requis et objectifs pour un sous-chapitre spécifique du programme de maths de seconde générale.
    Pour chaque sous-item du sous-chapitre demandé, identifie et liste:
    - Prérequis : Concepts ou compétences essentiels nécessaires avant de commencer cet item du sous-chapitre.
    - Objectifs : Buts d'apprentissage et compétences clés que les élèves devraient atteindre à la fin de cet item du sous-chapitre.
    - Structure : Une structure de contenu pour le sous-item du sous-chapitre à destination d'un professeur qui rédigera le contenu du cours.
    
    Utilise les détails du sous-chapitre et spécifications fournies pour t'aider dans cette tâche. Le cours ne doit pas contenir d'exercices.
    
    Envoie ta réponse au rédacteur. 
    """
WRITER_PROMPT = """
    Tu es un expert en enseignement des mathématiques pour la classe de seconde générale. Ta tâche est de générer du contenu en Markdown pour un sous-chapitre spécifique du programme de mathématoque en seconde. 
    Tu dois toujours respecter la structure fournie par l'inspecteur. Si besoin, tu peux inclure du LaTeX dans un code block. Le contenu généré doit être de grande qualité et organisé autour des concepts suivants:
    - Définitions: Définissent clairement un concept mathématique. Utilisent une formulation stricte pour éviter toute ambiguïté.
    - Propriétés: Énoncent des caractéristiques universelles du concept défini.Peuvent être admises (sans preuve) ou prouvées.
    - Exemples: Illustrations concrètes de la définition ou de la propriété. Doivent être choisis pour leur clarté et représentativité.
    - Remarques: Apportent contexte, clarification ou nuances supplémentaires.Sont pertinentes et enrichissent la compréhension du concept.
    """


# ------------------------ BUILD TEAMS ------------------------
def build_course_generation_team(instruments: FileAgentInstruments):
    """
    Build a team of agents that can generate a raw math course in markdown.
    """

    # create a set of agents with specific roles
    # admin user proxy agent - takes in the prompt and manages the group chat
    user_proxy = autogen.UserProxyAgent(
        name="Admin",
        system_message=USER_PROXY_PROMPT,
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    # inspector - generates sub-chapter specs for the writer
    inspector = autogen.AssistantAgent(
        name="Inspecteur",
        llm_config=agents_config.base_config,
        system_message=INSPECTOR_PROMPT,
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    # writer - generates raw course content based on the inspector's guidelines
    writer = autogen.AssistantAgent(
        name="Rédacteur",
        llm_config=agents_config.base_config,
        system_message=WRITER_PROMPT,
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    return [
        user_proxy,
        inspector,
        writer,
    ]


# ------------------------ ORCHESTRATION ------------------------


def build_team_orchestrator(
    team: str,
    agent_instruments: FileAgentInstruments,
    validate_results: callable = None,
) -> orchestrator.Orchestrator:
    """
    Based on a team name, build a team of agents and return an orchestrator
    """
    if team == "course_generation":
        return orchestrator.Orchestrator(
            name="course_generation_team",
            agents=build_course_generation_team(agent_instruments),
            instruments=agent_instruments,
            validate_results_func=validate_results,
        )
    raise Exception("Unknown team: " + team)
