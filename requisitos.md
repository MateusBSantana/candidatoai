Requisitos Funcionais (RF) — CandidatoIA

[RF 001] Leitura do perfil do candidato: O sistema poderá ler as informações do candidato, como: nome, contato, objetivo, formação, habilidades e projetos.

[RF 002] Leitura das informações da vaga: O sistema poderá ler as informações da vaga em questão, como: nome da vaga, endereço, descrição da vaga, requisitos, salário e benefícios.

[RF 003] Comparação entre habilidades do perfil e a vaga: O sistema poderá identificar quais informações do candidato e da vaga serão compatíveis.

[RF 004] Score de compatibilidade: O sistema poderá demonstrar um gráfico coluna, mostrando a porcentagem de quanto o candidato está apto à vaga.

[RF 005] Score de melhorias: O sistema poderá demonstrar um gráfico radar, mostrando quais habilidades o candidato tem e o que ele precisa melhorar.

Pendências

RF 001 vai precisar de campos extras (contato, endereço) que ainda não existem no perfil.json real
RF 002 descreve uma leitura estruturada por campos que ainda não existe no código (hoje é só texto corrido)
RF 005 depende de um requisito de armazenamento/histórico de vagas que ainda não foi escrito