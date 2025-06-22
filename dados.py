import pandas as pd

perguntas = [
    {
        "pergunta": "O que podemos fazer para reduzir a poluição dos oceanos?",
        "opcoes": [
            "Descartar resíduos corretamente",
            "Lavar carros na praia",
            "Jogar lixo no rio"
        ],
        "resposta": 0,
        "dificuldade": "fácil",
        "explicacao": "O descarte correto evita que resíduos cheguem aos oceanos, protegendo a vida marinha."
    },
    {
        "pergunta": "Qual é o tempo de decomposição de uma garrafa plástica?",
        "opcoes": [
            "1 ano",
            "100 anos",
            "450 anos"
        ],
        "resposta": 2,
        "dificuldade": "médio",
        "explicacao": "Garrafas plásticas podem levar até 450 anos para se decompor, poluindo o meio ambiente por séculos."
    },
    {
        "pergunta": "O que é sustentabilidade ambiental?",
        "opcoes": [
            "Explorar sem cuidado",
            "Poluir para produção",
            "Usar sem comprometer o futuro"
        ],
        "resposta": 2,
        "dificuldade": "fácil",
        "explicacao": "Sustentabilidade significa usar os recursos naturais de forma consciente, sem esgotá-los para as gerações futuras."
    },
    {
        "pergunta": "Qual desses materiais é reciclável?",
        "opcoes": [
            "Plástico",
            "Resíduos orgânicos",
            "Cerâmica"
        ],
        "resposta": 0,
        "dificuldade": "fácil",
        "explicacao": "O plástico é reciclável, enquanto resíduos orgânicos devem ser compostados e cerâmica não é reciclável."
    },
    {
        "pergunta": "O que é reciclagem?",
        "opcoes": [
            "Queimar resíduos",
            "Reutilizar materiais",
            "Enterrar no solo"
        ],
        "resposta": 1,
        "dificuldade": "fácil",
        "explicacao": "Reciclagem é o processo de transformar materiais usados em novos produtos, reduzindo o consumo de recursos naturais."
    },
    {
        "pergunta": "Qual é a maneira eficaz de economizar energia em casa?",
        "opcoes": [
            "Deixar as luzes ligadas",
            "Usar lâmpadas LED",
            "Usar aquecedores elétricos"
        ],
        "resposta": 1,
        "dificuldade": "fácil",
        "explicacao": "Lâmpadas LED consomem até 85% menos energia que lâmpadas incandescentes e duram muito mais."
    },
    {
        "pergunta": "Qual desses é um exemplo de reciclagem?",
        "opcoes": [
            "Transformar papel usado",
            "Jogar lixo no mar",
            "Queimar plásticos"
        ],
        "resposta": 0,
        "dificuldade": "fácil",
        "explicacao": "Transformar papel usado em novo papel é um exemplo clássico de reciclagem, fechando o ciclo de produção."
    },
    {
        "pergunta": "Qual é a prática mais eficiente para diminuir a quantidade de resíduos?",
        "opcoes": [
            "Reduzir o consumo",
            "Jogar tudo no mesmo lixo",
            "Comprar mais produtos plásticos"
        ],
        "resposta": 0,
        "dificuldade": "médio",
        "explicacao": "Reduzir o consumo é o primeiro passo da hierarquia dos resíduos: Reduzir > Reutilizar > Reciclar."
    },
    {
        "pergunta": "Qual é o principal benefício da reciclagem de alumínio?",
        "opcoes": [
            "Reduzir resíduos",
            "Economizar energia",
            "Menor custo de produção"
        ],
        "resposta": 1,
        "dificuldade": "difícil",
        "explicacao": "Reciclar alumínio economiza 95% da energia necessária para produzir alumínio novo a partir da bauxita."
    },
    {
        "pergunta": "O que é o efeito estufa?",
        "opcoes": [
            "Fertilizante natural",
            "Gases retendo calor",
            "Danos à camada de ozônio"
        ],
        "resposta": 1,
        "dificuldade": "médio",
        "explicacao": "O efeito estufa é o processo onde gases atmosféricos retêm parte do calor do Sol, mantendo a Terra aquecida."
    },
    {
        "pergunta": "Qual destes é um exemplo de energia renovável?",
        "opcoes": [
            "Petróleo",
            "Energia eólica",
            "Carvão mineral"
        ],
        "resposta": 1,
        "dificuldade": "fácil",
        "explicacao": "A energia eólica é renovável, enquanto petróleo e carvão são fontes não renováveis de energia."
    },
    {
        "pergunta": "O que significa a sigla '5Rs' da sustentabilidade?",
        "opcoes": [
            "Reduzir, Reutilizar, Reciclar, Repensar, Recusar",
            "Recolher, Reorganizar, Reparar, Reabastecer, Reconstruir",
            "Racionalizar, Reestruturar, Reaproximar, Reorientar, Reconfigurar"
        ],
        "resposta": 0,
        "dificuldade": "difícil",
        "explicacao": "Os 5Rs representam: Reduzir o consumo, Reutilizar produtos, Reciclar materiais, Repensar hábitos e Recusar produtos não sustentáveis."
    }
]

# Criar DataFrame
df = pd.DataFrame([{
    "Pergunta": p["pergunta"],
    "Opcao1": p["opcoes"][0],
    "Opcao2": p["opcoes"][1],
    "Opcao3": p["opcoes"][2],
    "Resposta": p["resposta"] + 1,  # +1 para corresponder aos botões (1, 2, 3)
    "Dificuldade": p["dificuldade"],
    "Explicacao": p["explicacao"]
} for p in perguntas])

# Exportar para Excel (opcional)
df.to_excel("perguntas.xlsx", index=False)

# Garantir que o df está disponível para importação
if __name__ == "__main__":
    print(df.head())
