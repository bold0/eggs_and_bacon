# eggs_and_bacon

1 - content.html = Conteúdo da msg em HTML.
2 - subject.txt = Subject!
3 - accounts - Pasta onde ficarão as contas. Cada arquivo refere-se à um provedor diferente.
  Esquema: o nome do arquivo é a configuração do servidor SMTP.
            <smtp.server.com> <465> <ssl/no_ssl> <starttls/no_starttls>
  Conteúdo: Dentro do arquivo devem ficar as contas/senhas no formato: login@server.com\tpassword (com um TAB \t no meio).
  
4 - attachments - Pasta onde devem ficar os anexos a serem enviados.
5 - recipients - mailing list. Podem ser vários arquivos ou um só. O que importa é: um e-mail por linha.
6 - config.py - Configurações!
