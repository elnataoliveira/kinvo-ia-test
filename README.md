
1. Minerar 5 notícias sobre ações da B3. Importante salvar para ser usadas no processamento de linguagem natural(PNL) posteriormente. 
	 - https://financenews.com.br/feed/
	 - https://www.ultimoinstante.com.br/feed/

2. Extrair as entidades das 5 notícias mineradas anteriormente(entity recognition).

Criar uma api com dois end-points para:

	- minerar e salvar as noticías;
		http://localhost:<port>/crawl
	- extrair as entidades das notícias mineradas(entity recognition);
		http://localhost:<port>/extract

